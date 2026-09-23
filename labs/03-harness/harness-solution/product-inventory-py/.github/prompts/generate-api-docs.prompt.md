---
description: 'Generate API documentation for the active router file'
agent: 'agent'
tools: ['search', 'read']
---
# Generate API Documentation

Analyze the router in ${file} and generate comprehensive API documentation.

For each endpoint in the router:
1. List the HTTP method and route.
2. Describe the purpose of the endpoint.
3. Document the request parameters, body, and query string inputs.
4. Document the possible response status codes and their meanings.
5. Provide an example request and response in JSON format.

Format the output as a Markdown document suitable for a developer wiki.
