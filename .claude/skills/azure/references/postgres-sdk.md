# SDK snippets: connect with a token from app code

Condensed from the plugin skills **azure-identity-py**, **azure-identity-ts**, **azure-postgres-ts**, **azure-resource-manager-postgresql-dotnet**. Full patterns (async, sovereign clouds, device code flow, connection pooling, transactions, server creation, HA, backups, replicas) live in those plugin skills if installed.

## Shared credential rules (all languages)

- `DefaultAzureCredential` for code that runs both locally (CLI) and in Azure (managed identity).
- Never hardcode credentials: environment variables or managed identity only.
- Prefer managed identity in production; no secrets to manage.
- `ChainedTokenCredential` when a custom credential order / fallback is needed.
- Set `AZURE_CLIENT_ID` for user-assigned managed identities; use a user-assigned identity for multi-tenant scenarios.
- Token refresh is handled by the SDK. Entra ID tokens expire after ~1 hour.
- Exclude unused credentials to speed up authentication.

## Python (azure-identity)

```bash
pip install azure-identity
```

```python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
```

Python-specific: close async credentials explicitly or use context managers.

## TypeScript: credential (azure-identity)

```
npm install @azure/identity
```

```typescript
import { DefaultAzureCredential } from "@azure/identity";
const credential = new DefaultAzureCredential();
```

## TypeScript: PostgreSQL data plane (pg)

```
npm install pg @azure/identity
npm install -D @types/pg
```

```typescript
import { Pool } from "pg";
const pool = new Pool({ host: process.env.AZURE_POSTGRESQL_HOST, database: process.env.AZURE_POSTGRESQL_DATABASE, port: 5432, ssl: { rejectUnauthorized: true } });
```

- Connection pools in production, always.
- Parameterized queries; never concatenate user input.
- Always close connections: try/finally or pools.
- SSL required for Azure: `ssl: { rejectUnauthorized: true }`.
- Set connection timeouts to avoid hanging on network issues.
- Transactions for multi-statement operations.
- Monitor pool metrics: `totalCount`, `idleCount`, `waitingCount`.
- Graceful shutdown: call `pool.end()` on termination.
- Type query results with TypeScript generics.

## .NET: PostgreSQL management plane (Azure.ResourceManager.PostgreSql)

```
dotnet add package Azure.ResourceManager.PostgreSql
dotnet add package Azure.Identity
```

```csharp
using Azure.ResourceManager;
using Azure.Identity;
var armClient = new ArmClient(new DefaultAzureCredential());
```

- Flexible Server only; Single Server is deprecated.
- Zone-redundant HA for production workloads.
- `DefaultAzureCredential` over connection strings.
- Configure Entra ID auth; more secure than SQL auth alone. Enable both auth methods for flexibility.
- Backup retention 7-35 days based on compliance.
- Private endpoints for secure network access.
- Tune server parameters to the workload; read replicas for read-heavy workloads.
- Stop dev/test servers when idle to save cost.

See also [postgres-passwordless.md](postgres-passwordless.md), [postgres-permissions.md](postgres-permissions.md), [postgres-troubleshooting.md](postgres-troubleshooting.md).
