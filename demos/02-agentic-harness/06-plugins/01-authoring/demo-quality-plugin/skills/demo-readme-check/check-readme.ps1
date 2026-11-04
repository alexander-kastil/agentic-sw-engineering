param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$lines = Get-Content -LiteralPath $Path
$findings = @()
$inFence = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $n = $i + 1

    if ($line -match '^\s*```') {
        if (-not $inFence) {
            $lang = ($line -replace '^\s*```', '').Trim()
            if ($lang -eq '') { $findings += "Line ${n}: code fence opens without a language." }
        }
        $inFence = -not $inFence
        continue
    }
    if ($inFence) { continue }

    if ($line -match '—') { $findings += "Line ${n}: em dash. Use a colon, comma, semicolon or parentheses." }

    foreach ($m in [regex]::Matches($line, '\]\((/[^)]*)\)')) {
        $findings += "Line ${n}: absolute internal link $($m.Groups[1].Value). Use a relative path."
    }
}

if ($findings.Count -eq 0) {
    Write-Output "OK: $Path"
    exit 0
}

Write-Output "FAIL: $Path"
$findings | ForEach-Object { Write-Output "  $_" }
exit 1
