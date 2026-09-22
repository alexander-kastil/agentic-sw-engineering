---
name: hr-doc-report
description: Query the HR-Documents library on the Copilot Demo SharePoint site through the work-iq MCP server, collect every document flagged for update with its metadata, and format the result as an HTML table. Use whenever a task mentions HR-Documents, the Needs Update flag, the copilot-demo SharePoint site, or an HR document status report, and before sending any report built from that library.
---

# HR Document Update Report

The library lives at `https://integrationsonline.sharepoint.com/sites/copilot-demo`, list name `HRDocuments`. Reach it with the `work-iq` server's `search_paths` and `fetch` tools.

## Resolving the site

Resolve the site by hostname and path, never by `$search` on its name. The hyphen in `copilot-demo` breaks search, which is the wrong turn this task takes on a first attempt.

## Reading the flag

The "Needs Update" column is stored as the boolean field `NeedsUpdate`, not as a string and not as `Yes`. Fetch list items with `$expand=fields` and read it from there.

`NeedsUpdate` is not an indexed column, so SharePoint refuses a server-side `$filter` on it and returns an error. Fetch the items and filter them in the response instead; the library is small enough that this is the correct answer rather than a workaround.

## The trap that produces a wrong report

A document that was never flagged carries no value for `NeedsUpdate` at all. Treating "not true" as "needs updating" returns the entire library.

| Read this as flagged | Do not read this as flagged |
|----------------------|-----------------------------|
| `NeedsUpdate` is `true` | `NeedsUpdate` is `false` |
| | `NeedsUpdate` is absent or null |

Three rows out of twelve is the shape of a correct answer. A result near twelve means the filter inverted.

## Output

An HTML table with the columns Document Name, Last Modified, and Modified By, followed by one summary line giving the count. Report the count you actually filtered to, never the number of items fetched.

## Before claiming the mail was sent

Sending is a separate permission from reading, and a denied send still returns prose that reads like success. Report the tool call's actual result, and say the send was not confirmed unless the tool returned a success payload.
