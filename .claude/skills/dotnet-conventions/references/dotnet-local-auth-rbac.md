# Local Auth + DB RBAC (dual-auth alongside MSAL)

Pattern for apps that pair Entra ID (MSAL) sign-in with a parallel local username/password login backed by database RBAC. Use when a project needs both a browser-facing MSAL flow and a programmatic or admin login that does not require Entra.

## Architecture

- **Local login**: `POST /api/auth/login` (AuthController) verifies the password with `BCrypt.Net.BCrypt.Verify` against a `UserCredentials` row, then a `LocalTokenService` issues an HS256 JWT with `auth_type: local` and one `permission` claim per permission.
- **RBAC tables**: `Users` (identity), `UserCredentials` (BCrypt hash, work factor 11), `UserRoles`, `Roles`, `RolePermissions`, `Permissions`.
- **Admin rule (local)**: a local user holding the `Administrator` role gets its permission list replaced with `["*"]` in both the login response/JWT and `/api/auth/me`, plus `isAdmin: true` in `/me`. The DB itself stores named permissions, not a literal `*`.
- **Server policy**: `AdminPolicy.IsAdmin` accepts Entra principals via an `AdminEmails` config list (or the `"*"` wildcard entry) and local principals via a `permission` claim with value `*`. The `AdminOnly` authorization policy calls this for both auth types.
- **UI contract (critical)**: the frontend computes `isAdmin` purely as `permissions.includes('*')`; it does not read an `isAdmin` field. The API must therefore put `*` into the permissions array, not only set a boolean.

## Multiple Authentication Schemes

When running both MSAL JWT and a local JWT scheme, register them as separate named schemes and add a policy scheme to pick between them:

```csharp
builder.Services.AddAuthentication(options =>
{
    options.DefaultScheme = "Smart";
    options.DefaultChallengeScheme = "Smart";
})
.AddPolicyScheme("Smart", "Smart", options =>
{
    options.ForwardDefaultSelector = ctx =>
    {
        var auth = ctx.Request.Headers.Authorization.ToString();
        if (auth.StartsWith("Bearer "))
        {
            // local tokens carry auth_type=local in header or are distinguishable by issuer
            // simplest: try local scheme first, fall back to Entra
            return "Local";
        }
        return JwtBearerDefaults.AuthenticationScheme;
    };
})
.AddMicrosoftIdentityWebApi(
    builder.Configuration.GetSection("AzureAd"),
    jwtBearerScheme: JwtBearerDefaults.AuthenticationScheme)
.EnableTokenAcquisitionToCallDownstreamApi()
.AddInMemoryTokenCaches()
;

builder.Services.AddAuthentication()
    .AddJwtBearer("Local", options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = builder.Configuration["Auth:LocalJwt:Issuer"],
            ValidateAudience = true,
            ValidAudience = builder.Configuration["Auth:LocalJwt:Audience"],
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Auth:LocalJwt:SigningKey"]!))
        };
    });
```

If MSAL is gated behind `Auth:Enabled`, keep the policy scheme conditional on that flag so the local scheme can stand alone when Entra is off.

## LocalTokenService

Issue a JWT with one `permission` claim per permission. Replace all permissions with `*` for Administrator users before minting the token:

```csharp
public class LocalTokenService(IConfiguration config)
{
    public string Issue(User user, IEnumerable<string> permissions)
    {
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new(ClaimTypes.Name, user.Name),
            new("auth_type", "local")
        };

        foreach (var p in permissions)
            claims.Add(new Claim("permission", p));

        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(config["Auth:LocalJwt:SigningKey"]!));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: config["Auth:LocalJwt:Issuer"],
            audience: config["Auth:LocalJwt:Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddDays(7),
            signingCredentials: creds);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

## Login Endpoint

```csharp
[HttpPost("login")]
[AllowAnonymous]
public async Task<IActionResult> Login(LoginRequest req)
{
    var credential = await db.UserCredentials
        .AsNoTracking()
        .Include(c => c.User)
            .ThenInclude(u => u.UserRoles)
                .ThenInclude(ur => ur.Role)
                    .ThenInclude(r => r.RolePermissions)
                        .ThenInclude(rp => rp.Permission)
        .FirstOrDefaultAsync(c => c.Username == req.Username && c.Active);

    if (credential is null || !BCrypt.Net.BCrypt.Verify(req.Password, credential.PasswordHash))
        return Unauthorized();

    var isAdmin = credential.User.UserRoles.Any(ur => ur.Role.Name == "Administrator");
    var permissions = isAdmin
        ? ["*"]
        : credential.User.UserRoles
            .SelectMany(ur => ur.Role.RolePermissions)
            .Select(rp => rp.Permission.InternalName)
            .Distinct()
            .ToList();

    var token = tokenService.Issue(credential.User, permissions);
    return Ok(new { token, permissions, isAdmin });
}
```

## Me Endpoint

The `/api/auth/me` endpoint must derive `isAdmin` from roles, not hardcode it:

```csharp
[HttpGet("me")]
public async Task<IActionResult> Me()
{
    var authType = User.FindFirstValue("auth_type");

    if (authType == "local")
    {
        var userId = int.Parse(User.FindFirstValue(ClaimTypes.NameIdentifier)!);
        var user = await db.Users
            .AsNoTracking()
            .Include(u => u.UserRoles).ThenInclude(ur => ur.Role)
                .ThenInclude(r => r.RolePermissions).ThenInclude(rp => rp.Permission)
            .FirstOrDefaultAsync(u => u.Id == userId);

        if (user is null) return Unauthorized();

        var isAdmin = user.UserRoles.Any(ur => ur.Role.Name == "Administrator");
        var permissions = isAdmin
            ? new List<string> { "*" }
            : user.UserRoles
                .SelectMany(ur => ur.Role.RolePermissions)
                .Select(rp => rp.Permission.InternalName)
                .Distinct()
                .ToList();

        return Ok(new { user.Name, permissions, isAdmin });
    }

    // Entra path — derive from AdminEmails config or DB RBAC
    // ...
}
```

## Seeding Local Users

When `Auth:Enabled` is `true`, the user-management endpoints require a bearer token, so seed via direct DB insert instead of the API.

Generate BCrypt hashes with a small helper tool (e.g., a console app using `BCrypt.Net.BCrypt.HashPassword(password, 11)`) so they match the API's `Verify` call exactly.

Rows needed:
- `Users` (name, active)
- `UserCredentials` (username, BCrypt hash at work factor 11, active)
- `UserRoles` (one row per role)

Verify end to end: `POST /api/auth/login` should return a JWT containing `"permission": "*"` for admins; `GET /api/auth/me` with that token should report `isAdmin: true`.

## appsettings — Local JWT Section

```json
"Auth": {
  "Enabled": true,
  "LocalJwt": {
    "Issuer": "your-app",
    "Audience": "your-app",
    "SigningKey": "<min-32-char-secret>"
  },
  "AdminEmails": ["admin@example.com"]
}
```

On Azure App Service, set these via double-underscore env vars:

```bash
az webapp config appsettings set -g <rg> -n <app> --settings \
  "Auth__LocalJwt__SigningKey=<secret>"
```

The App Service must have the `SigningKey` set or every local-JWT request returns 503/401.

## Pitfalls (each one was observed)

1. **Stripping `*` in the permission pipeline** (login response, token service, `/me`) silently makes local admins impossible while unit tests still pass. Check every place permissions are projected.
2. **Hardcoding `isAdmin: false` for `auth_type: local` in `/me`** breaks the admin UI at runtime only; derive it from roles.
3. **Editing the auth controller under a running `dotnet watch`** is a structural (rude) edit: hot reload fails with `TypeLoadException` and the API serves that exception for every request until the watch is manually restarted. Verify with a live request after the change.
4. **E2E tests written against the broken behavior** can pass by asserting the bug ("admin redirects away") as expected. Tests must encode the requirement, not the current output.
5. **Missing `SigningKey` on App Service** causes the API to fail at startup or return 401/503 for all requests. Always provision this setting before first deploy.
