# REST Client Files

Reference for `.http` request files used with the VS Code REST Client extension or JetBrains Rider.

## Rules

- Naming convention: `test-{resource}.http` at the project root (e.g., `test-persons.http`).
- Always update the `.http` file when adding or changing any endpoint.

## File Format

```http
@base = http://localhost:5122/api

### Get all persons
GET {{base}}/persons

### Get person by id
GET {{base}}/persons/1

### Create person
POST {{base}}/persons
Content-Type: application/json

{
  "name": "Example Item",
  "year": 2024
}

### Update person
PUT {{base}}/persons/1
Content-Type: application/json

{
  "name": "Example Item",
  "year": 2025
}

### Delete person
DELETE {{base}}/persons/1
```

## Conventions

| Element | Convention |
|---|---|
| Base variable | `@base = http://localhost:5122/api` |
| Request separator | `###` followed by a description comment |
| JSON body | Always include `Content-Type: application/json` for POST/PUT |
| File location | Project root alongside the `.csproj` file |
