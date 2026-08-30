#!/usr/bin/env python3
"""Emit a guarded, idempotent, self-verifying ADDITIVE SQL delta from a manifest.

The deterministic half of "add rows to a table a generator already owns". The judgement half,
which tables, which natural key, which rows, is harvested per repo into the manifest; this
script turns that manifest into SQL the same way every time.

    python gen-additive-delta.py --manifest <manifest.json> --out <delta.sql>
    <manifest producer> | python gen-additive-delta.py --manifest - --out <delta.sql>

What the emitted script does, and nothing else:

- refuses to run unless DB_NAME() is one of the named databases, and unless every table exists;
- loads the rows into temp tables, so no surrogate id is ever embedded;
- inserts parents whose natural key is absent, then updates in place the ones already there,
  so a re-run refreshes copy rather than duplicating rows;
- deletes and reinserts child rows only for those parents, leaving every other row untouched;
- resolves foreign keys by natural key through a lookup table, and throws on an unresolved one
  instead of writing NULL or silently skipping;
- runs inside one transaction and ends with one count SELECT per table restricted to the keys,
  so RowsFound beside RowsExpected proves the scope and not merely the run.

Manifest shape:

{
  "databases": ["app", "app-blue", "app_dev"],
  "requireTables": ["Parent", "Lookup"],
  "parent": {
    "table": "CapabilityItems",
    "idColumn": "ItemId",
    "keyColumn": "Slug",
    "columns": [{"name": "Slug", "type": "nvarchar(160)"}, {"name": "SortOrder", "type": "int"}],
    "literals": {"IsPublished": "CAST(1 AS bit)"},
    "rows": [{"Slug": "a", "SortOrder": 1}]
  },
  "children": [
    {
      "table": "CapabilityItemGroups",
      "parentFkColumn": "ItemId",
      "columns": [{"name": "SortOrder", "type": "int"}],
      "lookups": [
        {"column": "GroupId", "table": "CapabilityGroups", "keyColumn": "Label",
         "rowField": "GroupLabel", "type": "nvarchar(120)",
         "errorNumber": 50011, "errorText": "A row names a group label that does not exist."}
      ],
      "rows": [{"_key": "a", "GroupLabel": "Bookkeeping", "SortOrder": 2}]
    }
  ]
}

`_key` on a child row is the parent's natural key. `type` is the SQL type the temp table uses;
`int` columns are emitted unquoted, everything else as an N'' literal, and null as NULL.
"""

import argparse
import json
import sys

class ManifestError(Exception):
    pass

def lit(value, sql_type):
    if value is None:
        return "NULL"
    if sql_type == "int":
        return str(int(value))
    if sql_type == "bit":
        return "CAST(%d AS bit)" % (1 if value else 0)
    return "N'" + str(value).replace("'", "''") + "'"

def require(mapping, field, where):
    if field not in mapping:
        raise ManifestError("%s is missing %r" % (where, field))
    return mapping[field]

def validate(manifest):
    for field in ("databases", "parent"):
        require(manifest, field, "the manifest")
    parent = manifest["parent"]
    for field in ("table", "keyColumn", "columns", "rows"):
        require(parent, field, "parent")
    if not parent["rows"]:
        raise ManifestError("parent has no rows: nothing to add")

    names = [c["name"] for c in parent["columns"]]
    if parent["keyColumn"] not in names:
        raise ManifestError("parent keyColumn %r is not among its columns" % parent["keyColumn"])
    keys = [row[parent["keyColumn"]] for row in parent["rows"]]
    if len(set(keys)) != len(keys):
        raise ManifestError("two parent rows carry the same key")
    for row in parent["rows"]:
        for name in names:
            if name not in row:
                raise ManifestError("parent row %r has no %r" % (row.get(parent["keyColumn"]), name))

    known = set(keys)
    for child in manifest.get("children", []):
        for field in ("table", "parentFkColumn", "rows"):
            require(child, field, "child %r" % child.get("table"))
        for row in child["rows"]:
            if "_key" not in row:
                raise ManifestError("a %s row has no _key" % child["table"])
            if row["_key"] not in known:
                raise ManifestError("%s row names an unknown parent key %r"
                                    % (child["table"], row["_key"]))

def temp_table(name, columns):
    out = ["IF OBJECT_ID(N'tempdb..%s') IS NOT NULL DROP TABLE %s;" % (name, name),
           "CREATE TABLE %s (" % name]
    out.append(",\n".join("    [%s] %s NULL" % (c["name"], c["type"]) for c in columns))
    out.append(");")
    return out

def values_block(rows, columns):
    lines = []
    for row in rows:
        cells = [lit(row.get(c["name"]), c["type"]) for c in columns]
        lines.append("    (" + ", ".join(cells) + ")")
    return ",\n".join(lines) + ";"

def emit(manifest):
    validate(manifest)
    parent = manifest["parent"]
    children = manifest.get("children", [])
    key = parent["keyColumn"]
    key_type = next(c["type"] for c in parent["columns"] if c["name"] == key)
    keys = [row[key] for row in parent["rows"]]
    key_list = ", ".join(lit(k, key_type) for k in keys)
    literals = parent.get("literals", {})

    out = []
    w = out.append
    w(":on error exit")
    w("SET NOCOUNT ON;")
    w("SET XACT_ABORT ON;")
    w("GO")
    w("")
    w("-- Additive change, scoped to these %s values:" % key)
    for k in keys:
        w("--   %s" % k)
    w("-- No schema, no migration-history row, no wholesale delete. A re-run refreshes these rows")
    w("-- and leaves every other row alone.")
    w("IF DB_NAME() NOT IN (%s)" % ", ".join("N'%s'" % d for d in manifest["databases"]))
    w("    THROW 50001, 'Refusing to run: this delta targets other databases.', 1;")
    w("")
    tables = manifest.get("requireTables") or ([parent["table"]] + [c["table"] for c in children])
    w("IF " + " OR ".join("OBJECT_ID(N'%s') IS NULL" % t for t in tables))
    w("    THROW 50002, 'Refusing to run: a target table is missing.', 1;")
    w("GO")
    w("")
    w("BEGIN TRANSACTION;")
    w("GO")
    w("")

    out.extend(temp_table("#Parents", parent["columns"]))
    w("INSERT INTO #Parents (%s) VALUES"
      % ", ".join("[%s]" % c["name"] for c in parent["columns"]))
    w(values_block(parent["rows"], parent["columns"]))
    w("GO")
    w("")

    for index, child in enumerate(children):
        columns = [{"name": "_key", "type": key_type}]
        columns += [{"name": l["rowField"], "type": l.get("type", "nvarchar(200)")}
                    for l in child.get("lookups", [])]
        columns += child.get("columns", [])
        child["_temp"] = "#Child%d" % index
        child["_tempColumns"] = columns
        out.extend(temp_table(child["_temp"], columns))
        w("INSERT INTO %s (%s) VALUES"
          % (child["_temp"], ", ".join("[%s]" % c["name"] for c in columns)))
        w(values_block(child["rows"], columns))
        w("GO")
        w("")

    for child in children:
        for lookup in child.get("lookups", []):
            w("-- Every %s must resolve; an unresolved one is an error, not a skip."
              % lookup["table"])
            w("IF EXISTS (SELECT 1 FROM %s c WHERE NOT EXISTS (SELECT 1 FROM [%s] l WHERE l.[%s] = c.[%s]))"
              % (child["_temp"], lookup["table"], lookup["keyColumn"], lookup["rowField"]))
            w("BEGIN")
            w("    SELECT DISTINCT c.[%s] AS Unresolved FROM %s c" % (lookup["rowField"], child["_temp"]))
            w("    WHERE NOT EXISTS (SELECT 1 FROM [%s] l WHERE l.[%s] = c.[%s]);"
              % (lookup["table"], lookup["keyColumn"], lookup["rowField"]))
            w("    THROW %d, '%s', 1;" % (lookup.get("errorNumber", 50011),
                                          lookup.get("errorText", "A row names a value that does not exist.")
                                          .replace("'", "''")))
            w("END")
            w("GO")
            w("")

    insert_columns = [c["name"] for c in parent["columns"]] + list(literals.keys())
    select_columns = ["s.[%s]" % c["name"] for c in parent["columns"]] + list(literals.values())
    w("-- Parents that are not there yet")
    w("INSERT INTO [%s] (%s)" % (parent["table"], ", ".join("[%s]" % c for c in insert_columns)))
    w("SELECT %s" % ", ".join(select_columns))
    w("FROM #Parents s")
    w("WHERE NOT EXISTS (SELECT 1 FROM [%s] p WHERE p.[%s] = s.[%s]);"
      % (parent["table"], key, key))
    w("GO")
    w("")

    updatable = [c["name"] for c in parent["columns"] if c["name"] != key]
    if updatable or literals:
        w("-- Refresh the copy of these rows on a re-run")
        w("UPDATE p SET")
        sets = ["    p.[%s] = s.[%s]" % (c, c) for c in updatable]
        sets += ["    p.[%s] = %s" % (c, v) for c, v in literals.items()]
        w(",\n".join(sets))
        w("FROM [%s] p" % parent["table"])
        w("JOIN #Parents s ON s.[%s] = p.[%s];" % (key, key))
        w("GO")
        w("")

    if children:
        w("-- Children of these parents only: replaced, never merged")
        for child in children:
            w("DELETE c FROM [%s] c JOIN [%s] p ON p.[%s] = c.[%s] JOIN #Parents s ON s.[%s] = p.[%s];"
              % (child["table"], parent["table"], parent["idColumn"], child["parentFkColumn"],
                 key, key))
        w("GO")
        w("")

    for child in children:
        lookups = child.get("lookups", [])
        cols = [child["parentFkColumn"]] + [l["column"] for l in lookups] \
            + [c["name"] for c in child.get("columns", [])]
        sel = ["p.[%s]" % parent["idColumn"]] \
            + ["l%d.[%s]" % (i, l["column"]) for i, l in enumerate(lookups)] \
            + ["c.[%s]" % c["name"] for c in child.get("columns", [])]
        w("INSERT INTO [%s] (%s)" % (child["table"], ", ".join("[%s]" % c for c in cols)))
        w("SELECT %s" % ", ".join(sel))
        w("FROM %s c" % child["_temp"])
        w("JOIN [%s] p ON p.[%s] = c.[_key]" % (parent["table"], key))
        for i, lookup in enumerate(lookups):
            w("JOIN [%s] l%d ON l%d.[%s] = c.[%s]"
              % (lookup["table"], i, i, lookup["keyColumn"], lookup["rowField"]))
        out[-1] = out[-1] + ";"
        w("GO")
        w("")

    w("COMMIT TRANSACTION;")
    w("GO")
    w("")
    for name in ["#Parents"] + [c["_temp"] for c in children]:
        w("IF OBJECT_ID(N'tempdb..%s') IS NOT NULL DROP TABLE %s;" % (name, name))
    w("GO")
    w("")
    w("-- Verification: RowsFound must equal RowsExpected on every line")
    w("SELECT N'%s' AS TableName, COUNT(*) AS RowsFound, %d AS RowsExpected"
      % (parent["table"], len(parent["rows"])))
    w("FROM [%s] WHERE [%s] IN (%s);" % (parent["table"], key, key_list))
    for child in children:
        w("SELECT N'%s' AS TableName, COUNT(*) AS RowsFound, %d AS RowsExpected"
          % (child["table"], len(child["rows"])))
        w("FROM [%s] c JOIN [%s] p ON p.[%s] = c.[%s] WHERE p.[%s] IN (%s);"
          % (child["table"], parent["table"], parent["idColumn"], child["parentFkColumn"],
             key, key_list))
    w("GO")
    w("")
    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--manifest", required=True, help="path to the manifest, or - for stdin")
    parser.add_argument("--out", required=True, help="path to write the SQL to, or - for stdout")
    args = parser.parse_args()

    if args.manifest == "-":
        manifest = json.load(sys.stdin)
    else:
        with open(args.manifest, encoding="utf-8") as fh:
            manifest = json.load(fh)

    script = emit(manifest)

    if args.out == "-":
        sys.stdout.write(script)
    else:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(script)
        counts = [(manifest["parent"]["table"], len(manifest["parent"]["rows"]))]
        counts += [(c["table"], len(c["rows"])) for c in manifest.get("children", [])]
        print("wrote %s" % args.out)
        for table, count in counts:
            print("  %-24s %d" % (table, count))

if __name__ == "__main__":
    try:
        main()
    except ManifestError as error:
        print("manifest error: %s" % error, file=sys.stderr)
        sys.exit(1)
