Set-Location $PSScriptRoot

$site = 'https://integrationsonline.sharepoint.com/sites/copilot-demo'
$recipient = 'alexander.kastil@integrations.at'
$subject = 'HR-Documents Update Status Report'

$prompt = @"
Use the hr-doc-report skill.
Query the HR-Documents library at $site using the work-iq MCP server.
Return only the documents where the boolean field NeedsUpdate is true.
Include the document name, modified date, and modified by fields.
Format the result as an HTML table with a summary line giving the count.
In PowerShell, run Connect-MgGraph -Scopes Mail.Send -NoWelcome first,
then send the table to $recipient with the subject '$subject' by calling Send-MgUserMail,
passing -BodyParameter @{ Message = @{ Subject; Body = @{ ContentType = 'HTML'; Content }; ToRecipients = @(@{ EmailAddress = @{ Address } }) } }.
"@

copilot -p $prompt --allow-all-tools -s
