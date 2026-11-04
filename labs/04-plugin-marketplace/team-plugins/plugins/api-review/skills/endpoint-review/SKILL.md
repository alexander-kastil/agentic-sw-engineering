---
name: endpoint-review
description: "Review HTTP endpoints (ASP.NET Core controllers, minimal APIs, Express or FastAPI routes) against the team's API guidelines. Use when the user asks to review an API, an endpoint, a controller or a route."
---

# Endpoint review

Check every endpoint in the files the user names against these rules:

1. The HTTP method matches the operation: `GET` reads, `POST` creates, `PUT` replaces, `PATCH` updates part of a resource, `DELETE` removes.
2. Routes use plural nouns and no verbs, for example `/orders/{id}`.
3. A missing resource returns `404`, invalid input returns `400` with a problem details body.
4. List endpoints accept paging parameters and never return an unbounded collection.
5. Input is validated before it reaches the data layer.

Report one table with the columns Endpoint, Rule, Finding and Fix. Report only violations; say "No findings" when there are none.
