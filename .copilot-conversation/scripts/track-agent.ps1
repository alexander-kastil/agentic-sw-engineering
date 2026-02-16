param(
    [ValidateSet("start", "stop")]
    [string]$Phase = "start"
)

$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { $hookData = $inputJson | ConvertFrom-Json } catch { exit 0 }

$dataPath = Join-Path $PSScriptRoot "../../.copilot-conversation/data"
$sessionFile = Join-Path $dataPath "current-session.txt"

if (-not (Test-Path $sessionFile)) { exit 0 }
$sessionId = (Get-Content $sessionFile -Raw).Trim()

$agentName = if ($hookData.agentName) { $hookData.agentName } else { "unknown" }
$agentFile = Join-Path $dataPath "agents-$agentName-$sessionId.json"

$epoch = [datetime]::new(1970, 1, 1, 0, 0, 0, [DateTimeKind]::Utc)
$timestamp = if ($hookData.timestamp) {
    $epoch.AddMilliseconds($hookData.timestamp).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
} else {
    (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
}

if ($Phase -eq "start") {
    if (Test-Path $agentFile) {
        $agentData = Get-Content $agentFile -Raw | ConvertFrom-Json
        $agentData.events += @{ timestamp = $timestamp; phase = "start" }
        $agentData | ConvertTo-Json -Depth 10 | Set-Content $agentFile
    } else {
        @{
            sessionId = $sessionId
            agentName = $agentName
            events    = @(@{ timestamp = $timestamp; phase = "start" })
        } | ConvertTo-Json -Depth 10 | Set-Content $agentFile
    }
} else {
    if (Test-Path $agentFile) {
        $agentData = Get-Content $agentFile -Raw | ConvertFrom-Json
        $agentData.events += @{ timestamp = $timestamp; phase = "stop" }
        $agentData | ConvertTo-Json -Depth 10 | Set-Content $agentFile
    }
}
