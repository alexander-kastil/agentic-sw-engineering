$payload = [Console]::In.ReadToEnd()
try { $data = $payload | ConvertFrom-Json } catch { exit 0 }

$target = $data.tool_input.file_path
if (-not $target) { $target = $data.tool_input.filePath }
if (-not $target) { exit 0 }

$normalized = $target.Replace([char]92, [char]47)
if ($normalized -notmatch '/(demos|labs)/.*readme\.md$') { exit 0 }
if (-not (Test-Path -LiteralPath $target)) { exit 0 }

$checker = Join-Path $PSScriptRoot "../skills/demo-readme-check/check-readme.ps1"
$report = & pwsh -NoProfile -File $checker -Path $target
if ($LASTEXITCODE -eq 0) { exit 0 }

$message = @"
$target failed the demo readme check. Fix these before continuing:
$($report -join "`n")
"@

@{ additionalContext = $message } | ConvertTo-Json -Compress
exit 0
