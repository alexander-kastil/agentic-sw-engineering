$site = 'https://integrationsonline.sharepoint.com/sites/copilot-demo'
$recipient = 'alexander.kastil@integrations.at'
$subject = 'HR-Documents Update Status Report'

$prompt = @"
Query the HR-Documents library at $site using the work-iq MCP server.
Return only the documents where the boolean field NeedsUpdate is true.
Include the document name, modified date, and modified by fields.
Format the result as an HTML table with a summary line giving the count.
Send it to $recipient with the subject '$subject' by calling Send-MgUserMail in PowerShell,
building the message hashtable with an HTML body and passing it as -BodyParameter.
"@

copilot -p $prompt --allow-all-tools -s
