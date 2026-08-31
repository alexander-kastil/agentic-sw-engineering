param(
    [int]$MaxLines = 60,
    [int]$MaxWords = 400,
    [int]$MaxSentences = 3,
    [int]$MaxBulletWords = 25,
    [int]$MaxHeadingDepth = 2
)

$inputJson = [Console]::In.ReadToEnd()
try { $hookData = $inputJson | ConvertFrom-Json } catch { exit 0 }

$target = Join-Path $PSScriptRoot "..\copilot-instructions.md"
$touched = ($inputJson -replace '\\', '\') -match 'copilot-instructions\.md'
if (-not $touched) { exit 0 }
if (-not (Test-Path $target)) { exit 0 }

$lines = Get-Content $target
$violations = @()

$body = ($lines | Where-Object { $_ -notmatch '^\s*$' }).Count
if ($body -gt $MaxLines) { $violations += "File is $body non-empty lines, limit is $MaxLines." }

$words = ($lines -join ' ' -split '\s+' | Where-Object { $_ }).Count
if ($words -gt $MaxWords) { $violations += "File is $words words, limit is $MaxWords." }

$inFence = $false
$paragraph = @()
$paraStart = 0

function Test-Paragraph($buffer, $start, $limit) {
    if ($buffer.Count -eq 0) { return $null }
    $text = ($buffer -join ' ')
    $count = ([regex]::Matches($text, '[.!?](\s|$)')).Count
    if ($count -gt $limit) { return "Line ${start}: paragraph has $count sentences, limit is $limit. Cut it to a table row or a bullet." }
    return $null
}

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $n = $i + 1

    if ($line -match '^\s*```') { $inFence = -not $inFence; continue }
    if ($inFence) { continue }

    if ($line -match '^(#+)\s') {
        $depth = $Matches[1].Length
        if ($depth -gt $MaxHeadingDepth) { $violations += "Line ${n}: heading depth $depth, limit is $MaxHeadingDepth." }
        $v = Test-Paragraph $paragraph $paraStart $MaxSentences
        if ($v) { $violations += $v }
        $paragraph = @(); continue
    }

    if ($line -match '^\s*\|') { continue }

    if ($line -match '^\s*([-*+]|\d+\.)\s+(.*)$') {
        $bullet = $Matches[2]
        $bw = ($bullet -split '\s+' | Where-Object { $_ }).Count
        if ($bw -gt $MaxBulletWords) { $violations += "Line ${n}: bullet is $bw words, limit is $MaxBulletWords." }
        $v = Test-Paragraph $paragraph $paraStart $MaxSentences
        if ($v) { $violations += $v }
        $paragraph = @(); continue
    }

    if ($line -match '^\s*$') {
        $v = Test-Paragraph $paragraph $paraStart $MaxSentences
        if ($v) { $violations += $v }
        $paragraph = @(); continue
    }

    if ($paragraph.Count -eq 0) { $paraStart = $n }
    $paragraph += $line
}

$v = Test-Paragraph $paragraph $paraStart $MaxSentences
if ($v) { $violations += $v }

if ($violations.Count -eq 0) { exit 0 }

$message = @"
copilot-instructions.md failed the anti-bloat check. Rewrite the offending parts as terse rules, tables, or bullets before continuing:
$($violations -join "`n")
Instructions are context loaded on every turn. They carry rules, not explanations.
"@

@{ additionalContext = $message } | ConvertTo-Json -Compress
exit 0
