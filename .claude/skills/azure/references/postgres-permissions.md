# Grant and template PostgreSQL permissions for Entra principals

Copy-paste SQL for Entra-mapped roles on Azure Database for PostgreSQL Flexible Server. Run the role functions connected as an Entra admin. Setup flow: [postgres-passwordless.md](postgres-passwordless.md).

Quote every role name: `"<role-name>"`. Role name = the UPN (`user@domain.com`) or a custom role name; group names with spaces must be quoted too.

## Create roles

```sql
SELECT * FROM pgaadauth_create_principal('user@domain.com', false, false);
```

Arguments: `roleName` (must match the Entra principal name exactly), `isAdmin` (true = `azure_pg_admin` member), `isMfa` (true = require MFA claim in token).

```sql
SELECT * FROM pgaadauth_create_principal('admin@domain.com', true, false);
```

By object ID (more reliable for managed identities, service principals, groups):

```sql
SELECT * FROM pgaadauth_create_principal_with_oid(
  'my-custom-role-name',
  'abc12345-1234-1234-1234-123456789012',
  'service',
  false,
  false
);
```

Positional args: roleName (any name you choose), objectId (Entra object ID GUID), objectType, isAdmin, isMfa.

Object types: `'user'` = Entra users incl. guests; `'group'` = Entra groups; `'service'` = service principals and managed identities.

## List roles

```sql
SELECT * FROM pgaadauth_list_principals(false);
SELECT * FROM pgaadauth_list_principals(true);
```

`false` = all Entra-mapped roles, `true` = admin roles only. Returns: rolename, principalType, objectId, tenantId, isMfa, isAdmin.

## Map an existing role to Entra (SECURITY LABEL)

```sql
SECURITY LABEL for "pgaadauth" on role "existing_role" 
  is 'aadauth,oid=<object-id>,type=user';

SECURITY LABEL for "pgaadauth" on role "existing_admin" 
  is 'aadauth,oid=<object-id>,type=user,admin';

SECURITY LABEL for "pgaadauth" on role "existing_group_role" 
  is 'aadauth,oid=<group-object-id>,type=group';

SECURITY LABEL for "pgaadauth" on role "existing_app_role" 
  is 'aadauth,oid=<service-principal-object-id>,type=service';
```

## Manual group sync

Only if group sync is enabled:

```sql
SELECT * FROM pgaadauth_sync_roles_for_group_members();
```

## Permission levels

### Read-only

SELECT on all tables in `public`.

```sql
GRANT CONNECT ON DATABASE <database> TO "<role-name>";
GRANT USAGE ON SCHEMA public TO "<role-name>";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "<role-name>";
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO "<role-name>";

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "<role-name>";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO "<role-name>";
```

The `ALTER DEFAULT PRIVILEGES` lines cover future tables/sequences; plain GRANTs do not.

### Read-write

```sql
GRANT CONNECT ON DATABASE <database> TO "<role-name>";
GRANT USAGE ON SCHEMA public TO "<role-name>";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "<role-name>";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO "<role-name>";

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "<role-name>";
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
  GRANT USAGE, SELECT ON SEQUENCES TO "<role-name>";
```

### Full admin

Includes creating objects.

```sql
GRANT ALL PRIVILEGES ON DATABASE <database> TO "<role-name>";
GRANT ALL PRIVILEGES ON SCHEMA public TO "<role-name>";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "<role-name>";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "<role-name>";
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO "<role-name>";

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "<role-name>";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "<role-name>";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO "<role-name>";

GRANT azure_pg_admin TO "<role-name>";
```

`azure_pg_admin` is the Azure PostgreSQL admin group role.

### Application-specific (named tables only)

```sql
GRANT CONNECT ON DATABASE <database> TO "<role-name>";
GRANT USAGE ON SCHEMA public TO "<role-name>";

GRANT SELECT, INSERT, UPDATE ON <table1> TO "<role-name>";
GRANT SELECT, INSERT, UPDATE, DELETE ON <table2> TO "<role-name>";
GRANT SELECT ON <readonly_table> TO "<role-name>";

GRANT USAGE, SELECT ON <table1>_id_seq TO "<role-name>";
GRANT USAGE, SELECT ON <table2>_id_seq TO "<role-name>";
```

### Schema-specific (multi-tenant / multi-schema)

```sql
GRANT CONNECT ON DATABASE <database> TO "<role-name>";
GRANT USAGE ON SCHEMA <schema-name> TO "<role-name>";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA <schema-name> TO "<role-name>";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA <schema-name> TO "<role-name>";

ALTER DEFAULT PRIVILEGES IN SCHEMA <schema-name> 
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "<role-name>";
ALTER DEFAULT PRIVILEGES IN SCHEMA <schema-name> 
  GRANT USAGE, SELECT ON SEQUENCES TO "<role-name>";
```

## Quick copy templates

User `developer@company.com`:

```sql
GRANT CONNECT ON DATABASE mydb TO "developer@company.com";
GRANT USAGE ON SCHEMA public TO "developer@company.com";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "developer@company.com";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "developer@company.com";
```

```sql
GRANT CONNECT ON DATABASE mydb TO "developer@company.com";
GRANT USAGE ON SCHEMA public TO "developer@company.com";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "developer@company.com";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "developer@company.com";
```

Managed identity `my-app-identity` (read-write, typical for apps):

```sql
GRANT CONNECT ON DATABASE mydb TO "my-app-identity";
GRANT USAGE ON SCHEMA public TO "my-app-identity";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "my-app-identity";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO "my-app-identity";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "my-app-identity";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO "my-app-identity";
```

Group `Database Readers` (names with spaces must be quoted):

```sql
GRANT CONNECT ON DATABASE mydb TO "Database Readers";
GRANT USAGE ON SCHEMA public TO "Database Readers";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "Database Readers";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "Database Readers";
```

## Revoke

```sql
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM "<role-name>";
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM "<role-name>";
REVOKE USAGE ON SCHEMA public FROM "<role-name>";
REVOKE CONNECT ON DATABASE <database> FROM "<role-name>";

ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM "<role-name>";
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON SEQUENCES FROM "<role-name>";
```

## Drop role

Revoke first, then drop:

```sql
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM "<role-name>";
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM "<role-name>";
REVOKE ALL PRIVILEGES ON DATABASE <database> FROM "<role-name>";
REVOKE USAGE ON SCHEMA public FROM "<role-name>";

DROP ROLE "<role-name>";
```

For groups with sync enabled, do NOT delete the group role. Disable login instead:

```sql
ALTER ROLE "Group Name" NOLOGIN;
```

## Check existing permissions

```sql
\du

SELECT 
  grantee,
  table_schema,
  table_name,
  privilege_type
FROM information_schema.role_table_grants 
WHERE grantee = '<role-name>';

SELECT datname, datacl FROM pg_database WHERE datname = '<database>';

SELECT nspname, nspacl FROM pg_namespace WHERE nspname = 'public';

SELECT * FROM pgaadauth_list_principals(false);
```

## Siblings

- [postgres-passwordless.md](postgres-passwordless.md) - Entra auth setup, patterns, helper scripts
- [postgres-group-sync.md](postgres-group-sync.md) - group sync configuration
- [postgres-troubleshooting.md](postgres-troubleshooting.md) - `permission denied`, `role does not exist`, token failures
