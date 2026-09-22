## When to use

Encrypting individual columns (a password, a token, a bank detail) in SQL Server from .NET, when the
plaintext must be recoverable **from the database alone**: attach the file to a fresh instance, supply
a passphrase, paste one statement, read the value. No application, no key vault, no certificate.

Triggers: "encrypt a field in the db", "column encryption", "DbEncrypted", "ENCRYPTBYPASSPHRASE",
"DECRYPTBYPASSPHRASE", "decrypt with only the database", "encrypt new values only".

Not this leaf: Always Encrypted and TDE (both are SQL Server features with their own key management,
and neither gives you a paste-one-statement recovery path), or hashing a password you never read back.

## The decision that drives everything else

The obvious .NET approach is an EF Core `ValueConverter`. **It is unusable the moment recovery must
work from the database alone**, because the converter encrypts in .NET and `DECRYPTBYPASSPHRASE`
cannot decrypt .NET AES. There is no T-SQL that reads an arbitrary AES-CBC blob either, so the
requirement forces the crypto server-side and every other decision follows from that:

| Requirement | Consequence |
|---|---|
| Recover with SQL alone | `ENCRYPTBYPASSPHRASE` on write, in a parameterized `UPDATE` |
| Read back through the ORM | A SQL scalar function mapped with `HasDbFunction`, used in the LINQ projection |
| Never migrate existing rows | A second column beside the old one, and a read-order rule |

If recovery from the database alone is *not* a requirement, use a value converter and stop reading:
it is simpler, needs no round trip, and does not carry the traps below.

## Storage shape and the read-order rule

Keep the existing plaintext column, never write it again, and add a cipher column beside it. Old rows
are then correct by construction, with no migration and no `UPDATE` anywhere in the delta:

```
Password       IS NOT NULL -> Password                                        (legacy row)
PasswordCipher IS NOT NULL -> CONVERT(nvarchar(4000), DECRYPTBYPASSPHRASE(@k, PasswordCipher))
both NULL                  -> NULL                                            (no value)
```

Column type is `varbinary(8000)`, never `varbinary(max)`: `ENCRYPTBYPASSPHRASE` *returns*
`varbinary(8000)`, so `max` can never be filled and only hides the ceiling. Measured size is
`20 + ceil((2n+9)/16)*16` bytes for an `nvarchar(n)` input (4-byte version header, 16-byte IV,
AES-256 blocks).

## Making it attribute-driven

An attribute plus a naming convention keeps the mechanism generic. For a property `P` carrying
`[DbEncrypted(maxLength)]`:

| Aspect | Rule |
|---|---|
| `P` | `Ignore()`d in the model: an unmapped, in-memory plaintext carrier |
| `{P}Legacy` | `string?` with a `private set`, mapped to column `P` |
| `{P}Cipher` | `byte[]?` with a `private set`, mapped to column `{P}Cipher` |
| Read | `{P}Legacy ?? DecryptFn({P}Cipher, passphrase)` in the projection |
| Write | one `UPDATE` per entity after `SaveChangesAsync`, inside the same transaction |

`private set` is what makes "plaintext never reaches a persisted column, even transiently" structural
rather than a promise: no code outside the entity can assign the legacy column, so EF writes `NULL`.

Adding a second encrypted property later costs the attribute, the two companion properties, and one
delta adding its cipher column. No new C#. No convention can add a column to a database that forbids
migrations, so the delta is not optional.

## The write path

Encryption cannot run in a value converter, so it runs as one parameterized statement issued after
`SaveChangesAsync` and inside the same transaction. Derive table, schema and key column from the EF
model so the helper stays entity-agnostic, and interpolate **only** model metadata, never request data:

```csharp
var sql = $"UPDATE [{schema}].[{table}] SET [{cipherColumn}] = ENCRYPTBYPASSPHRASE(@passphrase, @v0) " +
          $"OUTPUT INSERTED.[{cipherColumn}] WHERE [{keyColumn}] = @key;";
```

Read the `OUTPUT` back in the same round trip and throw if the returned cipher is `NULL`. Without that
check the write silently stores nothing (see the ceiling trap below) and the row reads back as empty.
Send the passphrase and every value as `SqlDbType.NVarChar`, never as an inferred `string` parameter.

## The read path

Map the SQL function once and let LINQ do the rest:

```csharp
public static string? DecryptDbValue(byte[]? cipher, string passphrase) =>
    throw new NotSupportedException("dbo.fn_DecryptDbValue is evaluated by SQL Server only.");

modelBuilder.HasDbFunction(typeof(Ctx).GetMethod(nameof(DecryptDbValue), [typeof(byte[]), typeof(string)])!)
    .HasName("fn_DecryptDbValue").HasSchema("dbo");
```

The body throws on purpose: it is a marker for the translator and must never execute client-side.
`DECRYPTBYPASSPHRASE` is deterministic and is allowed inside a scalar UDF, so the function is one line.

## Five traps, every one of them silent

**A wrong passphrase returns NULL, it does not throw.** So a naive `COALESCE` projection hands back
"no value" for every row and nothing anywhere reports an error. Carry a `HasCipher` flag through the
projection and throw a dedicated exception type when `HasCipher && value is null`. A dedicated type
matters: catching `InvalidOperationException` reports every EF connection and model failure as a bad
passphrase.

**Past roughly 3979 `nvarchar` characters `ENCRYPTBYPASSPHRASE` returns NULL without raising.** Guard
the plaintext length in C# before it reaches SQL, and guard it inside the write helper rather than
relying on callers, because a `SqlParameter` sized at `MaxLength` truncates silently and the `UPDATE`
still reports one row affected.

**The ciphertext is salted**, so two encryptions of the same plaintext differ. No equality search, no
unique index, no persisted computed column, no dedupe by value, and no test may assert on blob bytes.
Assert round-trips only.

**`CONVERT` must target `nvarchar`.** `CONVERT(varchar(...), DECRYPTBYPASSPHRASE(...))` returns
garbage, silently, with no error anywhere. Encrypt `nvarchar`, convert back to `nvarchar`, and expect a
reviewer to "tidy" it at some point.

**Portable across instances, not backwards across versions.** The ciphertext depends only on the
passphrase: no database master key, no service master key, so detach and attach anywhere works. But
SQL Server 2017+ writes AES-256 (header `0x02000000`) while 2016 and earlier used Triple DES, so
restoring forward is fine and backward is not. That caveat travels with the recovery statement, not
just with the code.

## The recovery statement

This is the deliverable the whole design exists for. Hand it over with its conditions:

```sql
SELECT s.[Name],
       COALESCE(s.[Password],
                CONVERT(nvarchar(4000), DECRYPTBYPASSPHRASE(N'<passphrase>', s.[PasswordCipher]))) AS [Plain]
FROM [dbo].[Secrets] AS s;
```

A `NULL` result where the cipher column is non-`NULL` means the passphrase is wrong, not that the row
is empty. Say that explicitly wherever the statement is published, because the two are indistinguishable
at the SQL layer.

## Verifying it still holds

Run these against a scratch database, never the live one:

```sql
DECLARE @p nvarchar(500) = N'Grüße-€-123';
DECLARE @c varbinary(8000) = ENCRYPTBYPASSPHRASE(N'key', @p);
SELECT CASE WHEN CONVERT(varbinary(1000), CONVERT(nvarchar(4000), DECRYPTBYPASSPHRASE(N'key', @c)))
             = CONVERT(varbinary(1000), @p) THEN 'BINARY-IDENTICAL' ELSE 'MISMATCH' END;
```

Compare binaries, not console output: `sqlcmd` mangles non-ASCII on display and a correct round trip
looks broken. Then prove the boundary in the application: a row written before the change still reads
its plaintext and still has a `NULL` cipher, and a row written after has a `NULL` plaintext column and
a non-`NULL` cipher. That pair is the receipt for "encrypt new values, never touch existing records",
and it is the one check worth running after every schema change to the table.

**A failure path that cannot fire reports success.** Before trusting the wrong-passphrase guard, assert
that at least one row actually carries ciphertext. With zero encrypted rows, every passphrase including
a single letter passes, because no decrypt ever runs.
