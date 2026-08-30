# Static data an SPA ships is not protected by its route guard

An Angular (or React, or any SPA) app that reads its data from files under `public/` serves those files
as **static assets**. `authGuard` runs in the browser, on the router, after the bundle has already
loaded. It decides whether a *view* renders. It has no bearing on whether `GET /data/journey.json`
returns 200 to anyone who types that URL.

Proven on `src/bico-dashboard` (2026-08-01): every route sat behind `authGuard`, the login worked, and
`https://<host>/data/journey.json` returned the full file, with real client correspondence and billing
rates in it, to an unauthenticated browser.

## Check it in one command

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://<host>/data/<file>.json
```

Run this against any deployed SPA that has a `public/data/`, `assets/data/`, or similar folder. A 200
means the file is world-readable. Do this **before** claiming an app is protected: the guard's existence
in the source is not evidence about the file.

While you are there, enumerate what is actually in those files. "It is just dashboard data" is worth one
minute of reading: the bico-dashboard set turned out to hold client correspondence, invoice figures and
billing rates.

## The two fixes that do not work

**HTTP basic auth at the edge breaks the app.** The SPA fetches those same files itself, from its own
code, with no credentials attached. Adding `basic_auth` (Caddy) or `auth_basic` (nginx) to the `/data/`
path makes the browser 401 the app's own `fetch()`. The user is logged in, the page renders, and every
panel is empty. You cannot gate with basic auth a path the application reads programmatically.

**Caddy cannot validate the app's token.** The `caddy:2-alpine` image ships no JWT module, so
`caddy-jwt`/`caddy-security` would mean building a custom Caddy image. The edge has no way to check the
MSAL access token the SPA holds.

## The real fix

Serve the data from an **authenticated API endpoint** instead of as a static file: the SPA already sends
its bearer token on API calls, and the API can authorize per user. Anything genuinely confidential
belongs behind that, not in `public/`.

Treat everything below as a stopgap for when the data is only moderately sensitive and rebuilding it as
an API is not warranted yet.

## The non-breaking edge mitigation (obscurity-grade, be honest about it)

Browsers send `Sec-Fetch-Dest` and `Sec-Fetch-Site` on every request and scripts cannot forge them.
A `fetch()` from the app's own origin carries `Sec-Fetch-Dest: empty` and `Sec-Fetch-Site: same-origin`.
Pasting the URL into the address bar carries `Sec-Fetch-Dest: document`. Serving 404 to everything but
the former blocks URL sharing, accidental discovery, search indexing and casual snooping, while the app
keeps working untouched.

nginx, verified in a running container:

```nginx
location ^~ /data/ {
    if ($http_sec_fetch_dest != "empty") { return 404; }
    if ($http_sec_fetch_site != "same-origin") { return 404; }
    add_header X-Robots-Tag "noindex, nofollow, noarchive" always;
    add_header Cache-Control "no-store" always;
}
```

`^~` matters: it stops nginx from falling through to the regex `location ~* \.(js|css|...)$` block that
usually sits above and would otherwise win and serve the file with a 30-day cache.

Caddy equivalent, when nginx is not the server for that path:

```caddyfile
@dataDirect {
    path /data/*
    not header Sec-Fetch-Dest empty
}
respond @dataDirect 404
```

Measured behaviour of the nginx block:

| Request | Result |
| --- | --- |
| URL pasted into the address bar | 404 |
| The SPA's own `fetch()` | 200 |
| `curl` with no `Sec-Fetch-*` headers | 404 |
| Cross-site request (`Sec-Fetch-Site: cross-site`) | 404 |
| Normal app load | unchanged |

**State the limitation whenever you ship this.** `curl -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Site: same-origin'`
still gets the file. This is obscurity, not authentication: it defeats a link being forwarded, a crawler,
and an idle look around, and it defeats nothing that is actually trying. Say so in the report and in a
comment next to the config, so nobody later mistakes it for access control.

`no-store` plus `X-Robots-Tag` are part of the fix, not decoration: without them a shared CDN or a
search engine can retain and republish a copy that the header check never sees.

## Rule of thumb

Ask of every file under `public/`: **is this fine on a billboard?** If not, it is not a static asset.
The guard on the route that displays it does not change the answer.
