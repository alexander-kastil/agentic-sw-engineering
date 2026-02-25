param(
    [ValidateSet("start", "stop")]
    [string]$Phase = "start"
)

$ErrorActionPreference = "Continue"

$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { 
    $hookData = $inputJson | ConvertFrom-Json 
} catch { 
    exit 0 
}

$dataPath = Join-Path $PSScriptRoot "../../.copilot-conversation/data"
$sessionFile = Join-Path $dataPath "current-session.txt"

if (-not (Test-Path $sessionFile)) { 
    exit 0 
}

try {
    $sessionId = (Get-Content $sessionFile -Raw -ErrorAction Stop).Trim()
} catch {
    exit 0
}

$agentName = if ($hookData.agentName) { $hookData.agentName } else { "unknown" }
$debugPath = Join-Path $dataPath "debug-$sessionId.log"

"[$Phase-agent] $(Get-Date -Format o) agent="$agentName" input=$inputJson" | Add-Content $debugPath -ErrorAction SilentlyContinue

$epoch = [datetime]::new(1970, 1, 1, 0, 0, 0, [DateTimeKind]::Utc)
$timestamp = if ($hookData.timestamp -and [double]$hookData.timestamp -gt 0) {
    try {
        $epoch.AddMilliseconds([double]$hookData.timestamp).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    } catch {
        (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    }
} else {
    (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
}

$agentFile = Join-Path $dataPath "agents-$agentName-$sessionId.json"

$maxRetries = 3
for ($i = 0; $i -lt $maxRetries; $i++) {
    try {
        if (Test-Path $agentFile) {
            $agentData = Get-Content $agentFile -Raw -ErrorAction Stop | ConvertFrom-Json
            if (-not $agentData.events) {
                $agentData | Add-Member -NotePropertyName events -NotePropertyValue @() -Force
            }
            $agentData.events += @{ timestamp = $timestamp; phase = $Phase }
            $agentData | ConvertTo-Json -Depth 10 | Set-Content -Path $agentFile -ErrorAction Stop
            "[$Phase-agent] Updated existing agent file: $agentName" | Add-Content $debugPath -ErrorAction SilentlyContinue
        } else {
            @{
                sessionId = $sessionId
                agentName = $agentName
                events    = @(@{ timestamp = $timestamp; phase = $Phase })
            } | ConvertTo-Json -Depth 10 | Set-Content -Path $agentFile -ErrorAction Stop
            "[$Phase-agent] Created agent file: $agentName" | Add-Content $debugPath -ErrorAction SilentlyContinue
        }
        exit 0
    } catch {
        if ($i -lt ($maxRetries - 1)) {
            Start-Sleep -Milliseconds 50
        } else {
            "[$Phase-agent] ERROR after $maxRetries retries: $_" | Add-Content $debugPath -ErrorAction SilentlyContinue
        }
    }
}
