#requires -Version 5.0
$ErrorActionPreference = "Continue"

$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { 
    $hookData = $inputJson | ConvertFrom-Json 
} catch {
    $hookData = @{}
}

$sessionId = [guid]::NewGuid().ToString()
$metadataPath = Join-Path $PSScriptRoot "../../.copilot-conversation"
$dataPath = Join-Path $metadataPath "data"

# Create data directory if needed
try {
    if (-not (Test-Path $dataPath)) {
        New-Item -ItemType Directory -Path $dataPath -Force | Out-Null
    }
} catch {
    Write-Error "Failed to create data directory: $_"
    exit 1
}

# Create debug log file first for logging
$debugPath = Join-Path $dataPath "debug-$sessionId.log"
$logMessage = "[sessionStart] $(Get-Date -Format o)`nInput JSON: $inputJson`nSessionId: $sessionId`nDataPath: $dataPath`n"

try {
    $logMessage | Set-Content $debugPath
} catch {
    Write-Error "Failed to create debug log: $_"
    exit 1
}

# Helper function to log debug info
function Log-Debug($msg) {
    try {
        "$([DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ss.fffZ')) - $msg`n" | Add-Content $debugPath
    } catch {
        # Silently fail if debug logging fails
    }
}

# Create current session file
try {
    Set-Content -Path (Join-Path $dataPath "current-session.txt") -Value $sessionId -NoNewline -ErrorAction Stop
    Log-Debug "Created current-session.txt"
} catch {
    Log-Debug "ERROR creating current-session.txt: $_"
    Write-Error "Failed to create current-session.txt: $_"
    exit 1
}

function ConvertFrom-UnixMs($val) {
    try {
        $ms = [double]$val
        if ($ms -gt 0 -and $ms -gt 0) {
            return ([datetime]::new(1970, 1, 1, 0, 0, 0, [DateTimeKind]::Utc)).AddMilliseconds($ms).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        }
    } catch { }
    return (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
}

$timestamp = ConvertFrom-UnixMs $hookData.timestamp
Log-Debug "Calculated timestamp: $timestamp"

# Create history JSON file
$historyPath = Join-Path $dataPath "history-$sessionId.json"
$historyObject = @{
    sessionId = $sessionId
    startTime = $timestamp
    endTime   = $null
    status    = "active"
    messages  = @()
}

try {
    $historyJson = $historyObject | ConvertTo-Json -Depth 10
    $historyJson | Set-Content -Path $historyPath -ErrorAction Stop
    Log-Debug "Created history JSON file: $historyPath"
} catch {
    Log-Debug "ERROR creating history JSON: $_"
    Write-Error "Failed to create history JSON: $_"
    exit 1
}

# Create tools JSON file
$toolsPath = Join-Path $dataPath "tools-$sessionId.json"
$toolsObject = @{
    sessionId = $sessionId
    tools     = @()
}

try {
    $toolsJson = $toolsObject | ConvertTo-Json -Depth 10
    $toolsJson | Set-Content -Path $toolsPath -ErrorAction Stop
    Log-Debug "Created tools JSON file: $toolsPath"
} catch {
    Log-Debug "ERROR creating tools JSON: $_"
    Write-Error "Failed to create tools JSON: $_"
    exit 1
}

Log-Debug "Session start completed successfully"
