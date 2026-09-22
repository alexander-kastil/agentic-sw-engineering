---
name: 'API Controller Standards'
description: 'Coding standards for ASP.NET Core API controllers'
applyTo: '**/Controllers/**/*.cs'
---
# API Controller Standards

- Inherit from ControllerBase and apply the [ApiController] attribute.
- Use attribute routing with [Route("api/[controller]")] on the class.
- Keep controller methods thin: delegate business logic to service classes.
- Use action-specific attributes: [HttpGet], [HttpPost], [HttpPut], [HttpDelete].
- Return IActionResult or ActionResult<T> from all action methods.
- Include [ProducesResponseType] attributes to document response types.
- Validate model state using data annotations on request DTOs.
- Inject services through the constructor, not directly in action methods.
