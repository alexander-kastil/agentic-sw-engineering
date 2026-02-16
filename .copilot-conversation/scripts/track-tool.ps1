param(
    [ValidateSet("pre", "post")]
    [string]$Phase = "pre"
)

$inputJson = [Console]::In.ReadToEnd()
$hookData = $null
try { $hookData = $inputJson | ConvertFrom-Json } catch { exit 0 }

$dataPath = Join-Path $PSScriptRoot "../../.copilot-conversation/data"
$sessionFile = Join-Path $dataPath "current-session.txt"

if (-not (Test-Path $sessionFile)) { exit 0 }
$sessionId = (Get-Content $sessionFile -Raw).Trim()

$toolsPath = Join-Path $dataPath "tools-$sessionId.json"
if (-not (Test-Path $toolsPath)) { exit 0 }

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
$toolName = if ($hookData.tool_name) { [string]$hookData.tool_name } elseif ($hookData.toolName) { [string]$hookData.toolName } else { "unknown" }

$debugPath = Join-Path $dataPath "debug-$sessionId.log"
"[$Phase-tool] $(Get-Date -Format o) tool=$toolName`nRAW: $inputJson`n" | Add-Content $debugPath

$entry = [ordered]@{
    timestamp = [string]$timestamp
    phase     = [string]$Phase
    toolName  = [string]$toolName
}

if ($Phase -eq "post") {
    $rt = "success"
    if ($hookData.toolResult -and $hookData.toolResult.resultType) {
        $rt = [string]$hookData.toolResult.resultType
    }
    $entry.resultType = $rt
}

$maxRetries = 3
for ($i = 0; $i -lt $maxRetries; $i++) {
    try {
        $toolsData = Get-Content $toolsPath -Raw | ConvertFrom-Json
        if (-not $toolsData.tools) {
            $toolsData | Add-Member -NotePropertyName tools -NotePropertyValue @() -Force
        }
        $toolsData.tools += [pscustomobject]$entry
        $toolsData | ConvertTo-Json -Depth 10 | Set-Content $toolsPath
        break
    } catch {
        Start-Sleep -Milliseconds 50
    }
}
