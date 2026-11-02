param($Id)
if (-not $Id) {
    $Id = Read-Host "Enter experiment number (1-22)"
}
$num = "{0:D2}" -f [int]$Id
$cat = (Invoke-RestMethod "https://aisccli.netlify.app/catalog.json").experiments | Where-Object { $_.id -eq [int]$Id }
if (-not $cat) {
    Write-Host "[!] Experiment $Id not found in catalogue." -ForegroundColor Red
    return
}
$mf = Invoke-RestMethod "https://aisccli.netlify.app/$($cat.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://aisccli.netlify.app/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($cat.title) into $dir/" -ForegroundColor Green
