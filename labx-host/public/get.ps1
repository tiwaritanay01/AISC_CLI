param($Id, [string]$Lab = "")
if (-not $Id) {
    $Id = Read-Host "Enter experiment number (1-10 for ERTOS, 1-12 for AISC, or 1-22)"
}

$intId = [int]$Id
$cat = Invoke-RestMethod "https://aisccli.netlify.app/catalog.json"

if ($Lab -eq "ertos" -or $Lab -eq "es") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
} elseif ($Lab -eq "aisc") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "AISC" -and $_.lab_serial -eq $intId }
} else {
    $item = $cat.experiments | Where-Object { $_.id -eq $intId }
    if (-not $item -and $intId -le 10) {
        # Default to ERTOS if requested 1-10
        $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
    }
}

if (-not $item) {
    Write-Host "[!] Experiment $Id not found." -ForegroundColor DarkGray
    return
}

$num = "{0:D2}" -f [int]$item.id
$mf = Invoke-RestMethod "https://aisccli.netlify.app/$($item.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://aisccli.netlify.app/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($item.title) into $dir/" -ForegroundColor White

if ($item.output_url) {
    $outName = Split-Path $item.output_url -Leaf
    Invoke-WebRequest "https://aisccli.netlify.app/$($item.output_url)" -OutFile (Join-Path $dir $outName) -UseBasicParsing
    Write-Host "[OK] Downloaded Output PDF: $outName into $dir/" -ForegroundColor White
}
