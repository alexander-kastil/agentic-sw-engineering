$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { $hookData = $inputJson | ConvertFrom-Json } catch { }

$sessionId = [guid]::NewGuid().ToString()

$metadataPath = Join-Path $PSScriptRoot "../../.copilot-conversation"
$dataPath = Join-Path $metadataPath "data"

if (-not (Test-Path $dataPath)) {
    New-Item -ItemType Directory -Path $dataPath -Force | Out-Null
}

Set-Content -Path (Join-Path $dataPath "current-session.txt") -Value $sessionId -NoNewline

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
"[sessionStart] $(Get-Date -Format o)`nRAW: $inputJson`n" | Set-Content $debugPath

@{
    sessionId = $sessionId
    startTime = $timestamp
    endTime   = $null
    status    = "active"
    messages  = @()
} | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $dataPath "history-$sessionId.json")

@{
    sessionId = $sessionId
    tools     = @()
} | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $dataPath "tools-$sessionId.json")
