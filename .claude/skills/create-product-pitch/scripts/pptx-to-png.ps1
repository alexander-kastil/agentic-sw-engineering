param(
    [Parameter(Mandatory=$true)][string]$PptxPath,
    [Parameter(Mandatory=$true)][string]$OutDir,
    [int]$Width = 1920,
    [int]$Height = 1080
)

# Convert a PPTX to per-slide PNG images via PowerPoint COM automation.
# Required on Windows where soffice / pdftoppm are typically unavailable.
# msoTrue is hard-coded as -1 because [Microsoft.Office.Core.MsoTriState]
# cannot be resolved without loading the Office interop assembly.

$ErrorActionPreference = 'Stop'

$PptxFull = (Resolve-Path -LiteralPath $PptxPath).Path
if (-not (Test-Path -LiteralPath $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}
$OutFull = (Resolve-Path -LiteralPath $OutDir).Path

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = -1  # msoTrue. PPT refuses to run with $false or $true.
try {
    $pres = $ppt.Presentations.Open($PptxFull, $true, $false, $false)
    $slideCount = $pres.Slides.Count
    for ($i = 1; $i -le $slideCount; $i++) {
        $slide = $pres.Slides.Item($i)
        $outFile = Join-Path $OutFull ("slide-{0}.png" -f $i)
        $slide.Export($outFile, 'PNG', $Width, $Height)
        Write-Output ("exported {0}" -f $outFile)
    }
    $pres.Close()
} finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
