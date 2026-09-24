param(
    [int]$MaxLines = 90,
    [int]$MaxBulletWords = 30,
    [int]$MaxHeadingDepth = 2
)

$inputJson = [Console]::In.ReadToEnd()
try { $hookData = $inputJson | ConvertFrom-Json } catch { exit 0 }

$target = Join-Path $PSScriptRoot "..\copilot-instructions.md"
if ($inputJson -notmatch 'copilot-instructions\.md') { exit 0 }
if (-not (Test-Path $target)) { exit 0 }

$lines = Get-Content $target
$violations = @()

$body = ($lines | Where-Object { $_ -notmatch '^\s*$' }).Count
if ($body -gt $MaxLines) { $violations += "File is $body non-empty lines, limit is $MaxLines. Move detail into the skill or doc that owns it." }

$inFence = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $n = $i + 1

    if ($line -match '^\s*```') { $inFence = -not $inFence; continue }
    if ($inFence) { continue }

    if ($line -match '^(#+)\s') {
        $depth = $Matches[1].Length
        if ($depth -gt $MaxHeadingDepth) { $violations += "Line ${n}: heading depth $depth, limit is $MaxHeadingDepth." }
        continue
    }

    if ($line -match '^\s*([-*+]|\d+\.)\s+(.*)$') {
        $bw = ($Matches[2] -split '\s+' | Where-Object { $_ }).Count
        if ($bw -gt $MaxBulletWords) { $violations += "Line ${n}: bullet is $bw words, limit is $MaxBulletWords." }
    }
}

$required = 'Project|Where the detail lives|Skills|Agents|Hard Rules|Working Method'
$actual = (($lines | Where-Object { $_ -match '^## ' } | ForEach-Object { $_ -replace '^## ', '' -replace '\s+$', '' }) -join '|')
if ($actual -ne $required) {
    $violations += "Sections are out of order or renamed.`nexpected: $required`nfound:    $actual"
}

$inventory = @()
if ($lines | Where-Object { $_ -match '^\| *`?[a-z-]+`? *\| *(Read|Write|Edit|Bash|Glob)' }) { $inventory += 'an agent/tool table' }
if ($lines | Where-Object { $_ -match '^- \*\*(chrome-devtools|playwright|angular-cli|azure-deploy|github|microsoft-learn)\*\*' }) { $inventory += 'an MCP server list' }
if ($lines | Where-Object { $_ -match '(npm start|npm run e2e|dotnet watch run|dotnet test)' }) { $inventory += 'dev commands' }
if ($inventory.Count -gt 0) {
    $violations += "File carries an inventory again: $($inventory -join ', '). Keep the rule, drop the list."
}

if ($violations.Count -eq 0) { exit 0 }

$message = @"
copilot-instructions.md failed the router check. Fix these before continuing:
$($violations -join "`n")
This file is a router: repo purpose, folder layout, one-line rules, where the detail lives.
"@

@{ additionalContext = $message } | ConvertTo-Json -Compress
exit 0
