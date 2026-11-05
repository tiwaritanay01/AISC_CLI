param($Id, [string]$Lab = "")
if (-not $Id) {
    $Id = Read-Host "Enter experiment number (1-10 for ERTOS, 6-9 for CN, 1-12 for AISC, or 1-26)"
}

$intId = [int]$Id
$cat = Invoke-RestMethod "https://nirpin.vercel.app/catalog.json"

if ($Lab -eq "ertos" -or $Lab -eq "es") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
} elseif ($Lab -eq "cn") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "CN" -and $_.lab_serial -eq $intId }
} elseif ($Lab -eq "aisc") {
    $item = $cat.experiments | Where-Object { $_.subject -eq "AISC" -and $_.lab_serial -eq $intId }
} else {
    $item = $cat.experiments | Where-Object { $_.id -eq $intId }
    if (-not $item -and $intId -ge 6 -and $intId -le 9) {
        $item = $cat.experiments | Where-Object { $_.subject -eq "CN" -and $_.lab_serial -eq $intId }
    }
    if (-not $item -and $intId -le 10) {

        $item = $cat.experiments | Where-Object { $_.subject -eq "ES_RTOS" -and $_.lab_serial -eq $intId }
    }
}

if (-not $item) {
    Write-Host "[!] Experiment $Id not found." -ForegroundColor DarkGray
    return
}

$num = "{0:D2}" -f [int]$item.id
$mf = Invoke-RestMethod "https://nirpin.vercel.app/$($item.manifest_url)"
$dir = "Experiment$num"
New-Item -ItemType Directory -Path $dir -Force | Out-Null
foreach ($f in $mf.files) {
    Invoke-WebRequest "https://nirpin.vercel.app/experiments/$num/$($f.path)" -OutFile (Join-Path $dir $f.path) -UseBasicParsing
}
Write-Host "[OK] Downloaded $($item.title) into $dir/" -ForegroundColor White

if ($item.subject -eq "AISC") {
    $pyFile = $mf.files | Where-Object { $_.path.EndsWith(".py") } | Select-Object -First 1
    if ($pyFile) {
        try {
            $pyPath = Join-Path $dir $pyFile.path
            $pyContent = Get-Content -Path $pyPath -Raw -Encoding utf8
            Set-Clipboard -Value $pyContent -ErrorAction Stop
            Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White
        } catch {
            try { $pyContent | clip.exe; Write-Host "[OK] Code copied to clipboard (Ctrl+V ready!)" -ForegroundColor White } catch {}
        }
    }
}

if ($item.output_files) {
    foreach ($outP in $item.output_files) {
        $outName = Split-Path $outP -Leaf
        Invoke-WebRequest "https://nirpin.vercel.app/$outP" -OutFile (Join-Path $dir $outName) -UseBasicParsing
        Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
    }
} elseif ($item.output_url) {
    $outName = Split-Path $item.output_url -Leaf
    Invoke-WebRequest "https://nirpin.vercel.app/$($item.output_url)" -OutFile (Join-Path $dir $outName) -UseBasicParsing
    Write-Host "[OK] Downloaded Output: $outName into $dir/" -ForegroundColor White
}
