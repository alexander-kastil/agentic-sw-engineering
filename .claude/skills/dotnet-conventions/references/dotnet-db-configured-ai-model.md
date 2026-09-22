# Calling a DB-Configured AI Model for Customer-Facing Copy

Reference for endpoints that call an OpenAI-compatible chat-completions API whose provider, key and
parameters are **rows in the application's own database**, not `appsettings.json`, and that use the
completion to draft text a human will send to a real customer. This differs from `dotnet-maf.md`
(Azure AI Foundry agents): here the model is one of several customer-managed OpenAI-compatible
providers (DeepSeek, DeepInfra, ...) selected at runtime from an `AiModel` table that an admin
maintains through the app's own UI.

The shapes below are extracted from a working implementation; keep the structure and swap the entity
and DTO names for the ones in your project.

## Model selection: the DB is the source of truth, not config

The admin maintains multiple `AiModel` rows and flags exactly one `IsDefault = 1`. The service reads
that row per call, with no cached client and no `IOptions<T>`:

```csharp
var model = await db.AiModels.AsNoTracking().SingleOrDefaultAsync(m => m.IsDefault, ct);
if (model is null || string.IsNullOrWhiteSpace(model.ApiKey) || string.IsNullOrWhiteSpace(model.BaseUrl))
    throw new SuggestionUnavailableException(NoDefaultModelDetail);
```

Every field on that row is a per-model setting the request must honour, not a fallback to a global
default: `Provider` (log/telemetry label), `BaseUrl` (see normalisation below), `ApiKey` (bearer
token), `ModelName` (the `model` field in the chat-completions payload), `Temperature`, `MaxTokens`,
`TopP`. Pass the numeric ones straight through:

```csharp
var payload = new ChatCompletionRequest
{
    Model = model.ModelName,
    Messages = [new ChatMessage("system", systemPrompt), new ChatMessage("user", userPrompt)],
    Temperature = model.Temperature,
    MaxTokens = model.MaxTokens,
    TopP = model.TopP
};
```

`MaxTokens`/`TopP` are `int?`/`decimal?` on the DTO with
`[JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]`: an unset admin field must not
serialize as `null` into a provider that rejects the key outright rather than treating it as "use the
provider default".

## BaseUrl normalisation

Admins type `BaseUrl` by hand from each provider's docs, so the same tenant legitimately has
`https://api.deepseek.com`, `https://api.deepinfra.com/v1`, and `https://api.deepinfra.com/v1/openai`,
with or without a trailing slash. A naive `$"{baseUrl}/v1/chat/completions"` produces
`https://api.deepinfra.com/v1/v1/chat/completions` for the second provider and
`https://api.deepseek.com/chat/completions` (wrong, missing `/v1`) for the first. Normalise to exactly
one `/v1/chat/completions` by trimming, then only appending `/v1` if it is not already the last
segment:

```csharp
internal static string BuildChatCompletionsUrl(string baseUrl)
{
    var trimmed = baseUrl.Trim().TrimEnd('/');
    if (!trimmed.EndsWith("/v1", StringComparison.OrdinalIgnoreCase))
        trimmed += "/v1";
    return $"{trimmed}/chat/completions";
}
```

This does not fully solve `.../v1/openai` (that provider's own `/v1` alias is a third shape some
providers ship), so treat this as "normalise the two common shapes", not "handles every provider
forever": check the concrete `BaseUrl` values in the `AiModels` table before trusting a new provider
against it, and extend the helper's unit tests rather than special-casing it inline in the call site.

## Failure shape: everything collapses to one 503

No default model, a missing key, a provider HTTP error, a timeout, and an unparsable completion body
are five different causes that must all surface as the same `503` `ProblemDetails`, with `detail` set
to one complete sentence in the product's own language that the UI prints verbatim (never the
provider's raw error, the API key, or a stack trace):

```csharp
public class SuggestionUnavailableException(string detail) : Exception(detail);

private const string NoDefaultModelDetail =
    "Kein Standard-KI-Modell konfiguriert. Bitte in der Verwaltung ein Modell als Standard festlegen.";

private const string ProviderUnavailableDetail =
    "Der KI-Dienst ist aktuell nicht erreichbar. Bitte versuche es später erneut oder schreibe die Antwort manuell.";
```

Point the "no default model" sentence at the exact admin screen that fixes it: this error is a
configuration state, not a fault, and the recipient is the one person who can resolve it in one click.

Every failure path logs the real detail server-side, then throws the exception carrying only the safe
sentence:

```csharp
catch (HttpRequestException ex)
{
    logger.LogError(ex, "AI suggestion call to {Provider} failed for model {ModelName}", model.Provider, model.Name);
    throw new SuggestionUnavailableException(ProviderUnavailableDetail);
}
```

The controller maps the exception to the response, and nothing else:

```csharp
catch (SuggestionUnavailableException ex)
{
    return Problem(detail: ex.Message, statusCode: StatusCodes.Status503ServiceUnavailable);
}
```

A non-success HTTP status from the provider also logs the response body (for diagnosis) but never
forwards it into `detail`:

```csharp
if (!response.IsSuccessStatusCode)
{
    var errorBody = await response.Content.ReadAsStringAsync(ct);
    logger.LogError(
        "AI provider {Provider} returned {StatusCode} (model {ModelName}) after {ElapsedMs}ms: {Body}",
        model.Provider, (int)response.StatusCode, model.Name, elapsedMs, errorBody);
    throw new SuggestionUnavailableException(ProviderUnavailableDetail);
}
```

## Timeout and cancellation

Layer a fixed request timeout on top of the caller's own cancellation token with a linked CTS, and
distinguish "we timed out" from "the caller cancelled" so only the former gets classified as a
provider failure:

```csharp
private static readonly TimeSpan RequestTimeout = TimeSpan.FromSeconds(30);

using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(ct);
timeoutCts.CancelAfter(RequestTimeout);

try
{
    response = await client.SendAsync(request, timeoutCts.Token);
}
catch (OperationCanceledException) when (!ct.IsCancellationRequested)
{
    logger.LogError(
        "AI suggestion call to {Provider} timed out after {Timeout}s for model {ModelName}",
        model.Provider, RequestTimeout.TotalSeconds, model.Name);
    throw new SuggestionUnavailableException(ProviderUnavailableDetail);
}
```

The `when (!ct.IsCancellationRequested)` guard matters: if the *caller's* token fired (the user
navigated away), that is a normal ASP.NET Core request-abort, not a provider outage, so do not classify
it as a 503.

## Deterministic parsing with a defensive fallback

Ask the model for a fixed two-part shape in the system prompt, and never trust it fully at parse time:

```
Betreff: <hier der Betreff>
---
<hier der vollständige Antworttext mit Zeilenumbrüchen>
```

Parse it defensively: strip markdown code fences first (some providers wrap output in ` ``` ` even
when told not to), then look for the subject prefix and the `---` separator, falling back to the
caller's own subject and treating the whole text as the body when the model does not comply:

```csharp
internal static (string Subject, string Body) ParseResponse(string raw, string fallbackSubject)
{
    var text = StripCodeFences(raw).Trim();
    var lines = text.Replace("\r\n", "\n").Split('\n');

    string? subject = null;
    var bodyStartIndex = 0;

    if (lines.Length > 0 && lines[0].StartsWith("Betreff:", StringComparison.OrdinalIgnoreCase))
    {
        subject = lines[0]["Betreff:".Length..].Trim();
        bodyStartIndex = 1;
        if (lines.Length > 1 && lines[1].Trim() == "---")
            bodyStartIndex = 2;
    }

    var body = string.Join("\n", lines.Skip(bodyStartIndex)).Trim();

    if (string.IsNullOrWhiteSpace(subject))
        subject = string.IsNullOrWhiteSpace(fallbackSubject) ? DefaultSubject : fallbackSubject;
    if (string.IsNullOrWhiteSpace(body))
        body = text;

    return (subject, body);
}
```

Finally, truncate to the DTO's hard limit: the client renders this into a fixed-size textarea, and a
provider that ignores `max_tokens` must not blow past what the UI can hold.

```csharp
private const int MaxBodyLength = 4000;

internal static string TruncateBody(string body) =>
    body.Length <= MaxBodyLength ? body : body[..MaxBodyLength];
```

## Prompt rules for customer-facing copy

This is the part most likely to go wrong quietly, because a hallucination that happens to be correct
(or plausible) passes every code review and every test. Keep all five rules below when building a
similar feature: dropping any one of them reintroduces the failure it exists to prevent.

**Ground every hard fact in the prompt, or the model will invent it.** One implementation omitted the
business's street address from the prompt and the model filled it in from general knowledge. It happened
to be correct, which is worse than an obvious error, because nothing caught it in review. Anything
concrete (an address, a price, a date, a person's name) that the model states without it being supplied
in the prompt is a hallucination regardless of whether it turns out true. Put every hard fact the model
is allowed to state directly in the system prompt:

```
Du bist die Textassistenz für <Firmenname> in <Ort> (<Strasse, PLZ Ort>).
```

Where those facts already live in the database or a settings screen, read them from there per call
rather than hardcoding them into the prompt string, so the prompt cannot drift from the business's
actual data.

**Missing facts become explicit placeholders, never invented values.** When a concrete detail is not in
the prompt data, instruct the model to emit a bracketed placeholder instead of guessing, so it is
visibly incomplete in the UI rather than silently wrong:

```
Fehlt eine konkrete Angabe (z. B. ein genauer Termin, ein Preis oder ein Name), lass an dieser Stelle
einen Platzhalter in eckigen Klammern stehen, z. B. [BITTE TERMIN EINTRAGEN] oder
[BITTE PREIS EINTRAGEN]. Erfinde niemals selbst einen plausiblen Wert.
```

**Encode house style in the system prompt, because no human reviews every generation.** The operator
reads the draft and may send it with light edits or none at all, so style rules that live only in a
style guide never reach the output. One implementation's first generation shipped en dashes despite a
standing house rule against them, so the fix was to spell the rule out explicitly, including the literal
characters to avoid:

```
Immer Deutsch, immer in der informellen Du-Form. Kein Markdown (keine Sternchen, keine Listen mit
Bindestrichen), keine Emojis. Keine Gedankenstriche als Satzzeichen (weder - noch – noch —). Nutze
stattdessen Komma, Doppelpunkt, Strichpunkt oder Klammern.
```

**Feed the full conversation and the human's in-progress draft, and instruct the model to build on the
draft, not replace it.** The user prompt carries the inbound message, every prior reply in chronological
order, and whatever the operator has already typed in the textarea. The system prompt makes the priority
explicit: an existing draft's facts and intent win over anything the model would otherwise produce:

```
Wird im Nutzer-Prompt ein "Aktueller Entwurf" mitgegeben und ist dieser nicht leer, baue direkt darauf
auf: übernimm Absicht, alle genannten Fakten sowie alle konkreten Termine oder Preise aus dem Entwurf
unverändert und formuliere daraus eine vollständige, gut geschriebene Antwort. Verwirf den Entwurf
niemals.
```

**Model an on/off enrichment as an additive instruction layered on the chosen intent, not as another
enum member.** A flag such as "also include the offering and pricing" belongs on the request as a
`bool`, not as an extra member of the intent enum, because it composes with any of the real intents
(confirm, propose an alternative, decline) rather than replacing one:

```csharp
// An additive toggle, not another intent: it can be layered onto any of the actions above
// (for example "decline, and send the pricing information anyway").
private static string DescribeIncludeInfo(bool includeInfo) => includeInfo
    ? "Baue zusätzlich einen kurzen, natürlich in den Text eingewobenen Abschnitt zu Angebot, ..."
    : "Erwähne Angebot, Zeiten oder Preise in dieser Antwort nicht von dir aus.";
```

Had that flag been a fourth intent value, "decline and also send pricing" would need its own enum
member, and every future combination would double the enum. A `bool` (or a short list of independent
booleans) that the prompt-builder composes onto whichever intent was chosen keeps the combinations
linear instead of multiplicative. The same trap appears in the UI: controls that look alike in a
mockup are not necessarily the same kind of thing, and one that changes the meaning of the others is a
flag, not another action.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
| --- | --- | --- |
| Reading provider/key/model from `appsettings.json` | Tenants swap providers and rotate keys via the admin UI, not a redeploy | Read the `IsDefault` `AiModel` row per call |
| `$"{baseUrl}/v1/chat/completions"` with no normalisation | Breaks for any `BaseUrl` that already ends in `/v1` | Trim trailing slash, append `/v1` only if not already present |
| Returning `errorBody`/`ex.Message`/a provider status text in `Problem(detail: ...)` | Leaks provider internals (and risks leaking the key from a request-echo error) to the browser | Log the real detail; throw a canned safe sentence |
| Trusting `ct` alone for the outbound HTTP call | A slow or hanging provider blocks the request indefinitely if the client's own token never fires | Layer `CancellationTokenSource.CreateLinkedTokenSource(ct)` + `CancelAfter(fixedTimeout)` |
| Assuming the model always returns the requested `Betreff: / --- / body` shape | Providers occasionally ignore format instructions or wrap output in code fences | Strip fences, parse defensively, fall back to the caller's subject and the raw text as body |
| Letting the model state a fact (address, price, date) that was not supplied in the prompt | A correct-by-luck hallucination passes review; an incorrect one reaches a customer | Put every fact the model may state in the prompt; require bracketed placeholders otherwise |
| Adding a togglable enrichment as a new intent enum value | Multiplies the enum with every future toggle and intent combination | Model it as an additive instruction (bool) layered on the chosen intent |
