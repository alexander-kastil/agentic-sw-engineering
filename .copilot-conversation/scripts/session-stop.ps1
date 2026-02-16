$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { $hookData = $inputJson | ConvertFrom-Json } catch { }

$metadataPath = Join-Path $PSScriptRoot "../../.copilot-conversation"
$dataPath = Join-Path $metadataPath "data"
$sessionFile = Join-Path $dataPath "current-session.txt"

if (-not (Test-Path $sessionFile)) { exit 0 }
$sessionId = (Get-Content $sessionFile -Raw).Trim()

function ConvertFrom-UnixMs($val) {
    try {
        $ms = [double]$val
        if ($ms -gt 0) {
            return ([datetime]::new(1970, 1, 1, 0, 0, 0, [DateTimeKind]::Utc)).AddMilliseconds($ms).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        }
    } catch { }
    return (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
}

$timestamp = ConvertFrom-UnixMs $hookData.timestamp

$debugPath = Join-Path $dataPath "debug-$sessionId.log"
"[sessionEnd] $(Get-Date -Format o)`nRAW: $inputJson`n" | Add-Content $debugPath

$historyPath = Join-Path $dataPath "history-$sessionId.json"
if (Test-Path $historyPath) {
    $history = Get-Content $historyPath -Raw | ConvertFrom-Json
    $history | Add-Member -NotePropertyName endTime -NotePropertyValue ([string]$timestamp) -Force
    $history | Add-Member -NotePropertyName status -NotePropertyValue "completed" -Force
    if ($hookData.reason) {
        $history | Add-Member -NotePropertyName reason -NotePropertyValue ([string]$hookData.reason) -Force
    }
    $history | ConvertTo-Json -Depth 10 | Set-Content $historyPath
}

Push-Location $metadataPath
try {
    node scripts/visualize.mjs $sessionId 2>&1 | Out-Null
} finally {
    Pop-Location
}

Remove-Item $sessionFile -ErrorAction SilentlyContinue
