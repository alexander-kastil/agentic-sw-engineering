# ASP.NET Core Controller Patterns

Reference for `[ApiController]` classes, CRUD actions, and `Program.cs` wiring.

## Rules

- All endpoints use explicit `[ApiController]` classes in `Controllers/`.
- Never use inline lambdas in `Program.cs`.
- Never use `MapGroup` extension methods.
- Use primary constructor injection — never a constructor body with `this.field = field` assignments.

## Controller Structure

```csharp
namespace my_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ItemsController(AppDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetAll() =>
        Ok(await db.Items.AsNoTracking().ToListAsync());

    [HttpGet("{id:int}")]
    public async Task<IActionResult> GetById(int id)
    {
        var item = await db.Items.FindAsync(id);
        return item is null ? NotFound() : Ok(item);
    }

    [HttpPost]
    public async Task<IActionResult> Create(Item item)
    {
        db.Items.Add(item);
        await db.SaveChangesAsync();
        return CreatedAtAction(nameof(GetById), new { id = item.Id }, item);
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Delete(int id)
    {
        var item = await db.Items.FindAsync(id);
        if (item is null) return NotFound();
        db.Items.Remove(item);
        await db.SaveChangesAsync();
        return NoContent();
    }
}
```

## Return Types

| Scenario | Return |
|---|---|
| Success with body | `Ok(payload)` |
| Resource not found | `NotFound()` |
| Resource created | `CreatedAtAction(nameof(GetById), new { id }, resource)` |
| Delete success | `NoContent()` |

## Program.cs Registration

```csharp
builder.Services.AddControllers();

// ...

app.MapControllers();
```

Never call `AddControllers()` more than once. If auth is enabled, apply authorization at `MapControllers()`:

```csharp
app.MapControllers().RequireAuthorization();
```

## A public address is derived, never stored, and resolves on the id

A `Link` column holding `/capabilities/{slug}/` is a rename waiting to break: the slug moves, the
column does not, and nothing errors. Two rules remove the whole class of bug.

**Derive the address on read** from the immutable key plus the current slug, and stop reading the
stored column:

```csharp
private static string ItemLink(int id, string slug) => $"/capabilities/{id}-{slug}/";
```

Apply it on *every* read path in the same pass: the list projection, the detail, the sibling refs
and the admin DTO. One projection left on `Link = i.Link` is a surface that disagrees with the rest,
and it will be the one nobody looks at. EF cannot always translate the interpolation inside a
`.Select()`, so project the id and slug and fill the link after materialization.

**Resolve on the leading id and ignore the rest of the key**, so every address ever minted for that
row keeps working and a rename needs no redirect:

```csharp
var dash = key.IndexOf('-');
var head = dash < 0 ? key : key[..dash];

var published = db.Items.Where(i => i.IsPublished);
var item = int.TryParse(head, out var id)
    ? await published.FirstOrDefaultAsync(i => i.Id == id)
    : await published.FirstOrDefaultAsync(i => i.Slug == key);   // pre-scheme addresses
```

Build the branch as two `FirstOrDefaultAsync` calls over a shared query rather than one predicate
with a captured bool ternary, which EF may refuse to translate.

**The test that asserted the stored value will now fail, and that failure is the feature.** Fix it
by computing the expectation from the response (`$"/capabilities/{fetched.Id}-{slug}/"`) while
leaving the request payload sending the old literal, so the test proves the API returns something
different from what was sent. Rewriting the expectation to whatever the code now returns turns a
real assertion into an echo.

Leaving the write path (`item.Link = req.Link`) in place makes the column write-only. That is a
deliberate, temporary state at best: either drop the field from the save request and the admin form,
or say plainly that it is ignored.
