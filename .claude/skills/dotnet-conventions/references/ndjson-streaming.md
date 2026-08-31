## When to use

Streaming pipeline progress to a client as newline-delimited JSON, with a correlated trace that a
streaming controller can tap without threading callbacks through every service method.

## Pipeline Observability and NDJSON Streaming

- **Correlated trace pattern** — use a static `AsyncLocal<string?>` correlation id
  (`NewCorrelation`/`EnsureCorrelation`) and a `Write(pipeline, stage, props)` method that appends
  one JSON line to `logs/<pipeline>-pipeline.jsonl`. Schema: `{ts, correlationId, pipeline, stage,
  ...props}`. A second `AsyncLocal<Action<string,string,string>?>` subscriber
  (`SetSubscriber`/`ClearSubscriber`) lets a streaming controller tap every event without modifying
  service code.
- **NDJSON streaming endpoint** — set `Response.ContentType = "application/x-ndjson"`, create a
  `Channel<T>`, install the trace subscriber to feed it, then run the pipeline and channel draining
  concurrently. Emit typed lines, e.g. `{"type":"stage",...}`, `{"type":"cost",...}`,
  `{"type":"result",...}`. Always clear the subscriber in a `finally` block.
- **Input validation before fan-out** — when a pipeline stage fans out over a batch of structured
  identifiers (any format with a checksum or fixed shape), validate each one with private static
  helpers before entering the fan-out, and emit a `recognize-reject` trace stage for every dropped
  identifier. Don't let a malformed identifier reach downstream calls only to fail there.
- **AI cost capture** — read the usage/cost field your AI provider's response exposes (treat it as
  null when the field is absent, e.g. a model that doesn't report cost); emit it via the trace
  writer, e.g. `Write("ai", "ai-usage", new { Kind = "chat", ... })`. Other generation kinds (image,
  video) use their own `Kind` value with a per-unit cost config key as a fallback when the provider
  doesn't report cost directly.

## Worked example (one shipped pipeline)

The shape above came out of a product-resolution pipeline; its concrete choices are worth copying:

- `Services/PipelineTrace.cs` holds the static `AsyncLocal<string?>` correlation id
  (`NewCorrelation`/`EnsureCorrelation`), the `Write(pipeline, stage, props)` writer appending to
  `logs/<pipeline>-pipeline.jsonl`, and the `SetSubscriber`/`ClearSubscriber` pair.
- `Controllers/ResolveController.cs` exposes `POST /resolve/photo/stream`: it sets
  `Response.ContentType = "application/x-ndjson"`, installs the subscriber into a `Channel<T>`, runs
  resolution and channel draining concurrently, and clears the subscriber in `finally`.
- Identifier validation before fan-out: EAN-13/EAN-8 (Luhn checksum, rejecting all-equal digits,
  sequential runs and long zero-runs) and PZN are validated by private static helpers before the
  product-lookup fan-out, with a `recognize-reject` trace stage per dropped identifier. When the
  vision step signals `IsBackLabel=true`, the endpoint returns `back-label-only` instead of fanning
  out at all.
- Cost capture reads `usage.estimated_cost` from DeepInfra responses (absent for DeepSeek, treated as
  null) and emits `Kind = "chat"`; image and video generation emit `Kind = "image"` / `Kind = "video"`
  with the config keys `Images:CostPerImage` and `Videos:CostPerSecond` as fallbacks.
