$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { $hookData = $inputJson | ConvertFrom-Json } catch { exit 0 }

$dataPath = Join-Path $PSScriptRoot "../../.copilot-conversation/data"
$sessionFile = Join-Path $dataPath "current-session.txt"

if (-not (Test-Path $sessionFile)) { exit 0 }
$sessionId = (Get-Content $sessionFile -Raw).Trim()

$historyPath = Join-Path $dataPath "history-$sessionId.json"
if (-not (Test-Path $historyPath)) { exit 0 }

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
$prompt = if ($hookData.prompt) { [string]$hookData.prompt } else { "" }

$debugPath = Join-Path $dataPath "debug-$sessionId.log"
"[userPrompt] $(Get-Date -Format o)`nRAW: $inputJson`n" | Add-Content $debugPath

$history = Get-Content $historyPath -Raw | ConvertFrom-Json
if (-not $history.messages) {
    $history | Add-Member -NotePropertyName messages -NotePropertyValue @() -Force
}

$history.messages += @{
    role      = "user"
    timestamp = $timestamp
    content   = $prompt
}

$history | ConvertTo-Json -Depth 10 | Set-Content $historyPath
