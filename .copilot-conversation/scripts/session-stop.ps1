$ErrorActionPreference = "Continue"

$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { 
    $hookData = $inputJson | ConvertFrom-Json 
} catch { }

$metadataPath = Join-Path $PSScriptRoot "../../.copilot-conversation"
$dataPath = Join-Path $metadataPath "data"
$sessionFile = Join-Path $dataPath "current-session.txt"

if (-not (Test-Path $sessionFile)) { 
    exit 0 
}

try {
    $sessionId = (Get-Content $sessionFile -Raw -ErrorAction Stop).Trim()
} catch {
    exit 0
}

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

"[sessionEnd] $(Get-Date -Format o)`nRAW: $inputJson`n" | Add-Content $debugPath -ErrorAction SilentlyContinue

# Update history with end time
$historyPath = Join-Path $dataPath "history-$sessionId.json"
if (Test-Path $historyPath) {
    try {
        $history = Get-Content $historyPath -Raw -ErrorAction Stop | ConvertFrom-Json
        $history | Add-Member -NotePropertyName endTime -NotePropertyValue ([string]$timestamp) -Force
        $history | Add-Member -NotePropertyName status -NotePropertyValue "completed" -Force
        if ($hookData.reason) {
            $history | Add-Member -NotePropertyName reason -NotePropertyValue ([string]$hookData.reason) -Force
        }
        $history | ConvertTo-Json -Depth 10 | Set-Content -Path $historyPath -ErrorAction Stop
        "[sessionEnd] Updated history with end time" | Add-Content $debugPath -ErrorAction SilentlyContinue
    } catch {
        "[sessionEnd] ERROR updating history: $_" | Add-Content $debugPath -ErrorAction SilentlyContinue
    }
}

# Run visualization
Push-Location $metadataPath
try {
    if (Test-Path "scripts/visualize.mjs") {
        "[sessionEnd] Running visualization script..." | Add-Content $debugPath -ErrorAction SilentlyContinue
        node scripts/visualize.mjs $sessionId 2>&1 | Out-Null
        "[sessionEnd] Visualization completed" | Add-Content $debugPath -ErrorAction SilentlyContinue
    } else {
        "[sessionEnd] WARNING: visualize.mjs not found" | Add-Content $debugPath -ErrorAction SilentlyContinue
    }
} catch {
    "[sessionEnd] ERROR running visualization: $_" | Add-Content $debugPath -ErrorAction SilentlyContinue
} finally {
    Pop-Location
}

# Clean up session file
try {
    Remove-Item $sessionFile -ErrorAction Stop
    "[sessionEnd] Cleaned up session file" | Add-Content $debugPath -ErrorAction SilentlyContinue
} catch {
    "[sessionEnd] WARNING: Could not remove session file: $_" | Add-Content $debugPath -ErrorAction SilentlyContinue
}
