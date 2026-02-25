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

$historyPath = Join-Path $dataPath "history-$sessionId.json"
$debugPath = Join-Path $dataPath "debug-$sessionId.log"

if (-not (Test-Path $historyPath)) { 
    "[userPrompt] WARNING: History file not found at $historyPath" | Add-Content $debugPath -ErrorAction SilentlyContinue
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
$prompt = if ($hookData.prompt) { [string]$hookData.prompt } else { "" }

"[userPrompt] $(Get-Date -Format o) prompt_length=$($prompt.Length)`nRAW: $inputJson`n" | Add-Content $debugPath -ErrorAction SilentlyContinue

$maxRetries = 3
for ($i = 0; $i -lt $maxRetries; $i++) {
    try {
        $history = Get-Content $historyPath -Raw -ErrorAction Stop | ConvertFrom-Json
        if (-not $history.messages) {
            $history | Add-Member -NotePropertyName messages -NotePropertyValue @() -Force
        }

        $history.messages += @{
            role      = "user"
            timestamp = $timestamp
            content   = $prompt
        }

        $history | ConvertTo-Json -Depth 10 | Set-Content -Path $historyPath -ErrorAction Stop
        "[userPrompt] Successfully logged user message" | Add-Content $debugPath -ErrorAction SilentlyContinue
        exit 0
    } catch {
        if ($i -lt ($maxRetries - 1)) {
            Start-Sleep -Milliseconds 50
        } else {
            "[userPrompt] ERROR after $maxRetries retries: $_" | Add-Content $debugPath -ErrorAction SilentlyContinue
        }
    }
}
