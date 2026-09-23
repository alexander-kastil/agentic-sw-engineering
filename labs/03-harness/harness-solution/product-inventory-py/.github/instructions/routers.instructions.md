---
name: 'API Router Standards'
description: 'Coding standards for FastAPI routers'
applyTo: '**/routers/**/*.py'
---
# API Router Standards

- Create one APIRouter per resource with a prefix such as prefix="/api/products".
- Keep route functions thin: delegate business logic to service classes.
- Use method-specific decorators: @router.get, @router.post, @router.put, @router.delete.
- Declare response_model and status_code on every route.
- Validate request bodies with Pydantic models; never read the raw request body.
- Inject services and the current user through Depends, never instantiate them inside a route.
