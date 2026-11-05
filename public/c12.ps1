# LabX Remote: CN Exp 12 (Dynamic Routing Configuration using RIP v2 in GNS3)
$filename = "dynamic_routing_rip_v2_commands.txt"
$code = @'
EXPERIMENT 8 — DYNAMIC ROUTING (RIP v2)
GNS3 topology: PC1 — Switch1 — R1 — R2 — Switch2 — PC2

IP ADDRESSING
PC1: 192.168.1.2 /24, gateway 192.168.1.1
R1 FastEthernet0/0: 192.168.1.1 /24
R1 FastEthernet1/0: 192.168.2.1 /24
R2 FastEthernet1/0: 192.168.2.2 /24
R2 FastEthernet0/0: 192.168.3.1 /24
PC2: 192.168.3.2 /24, gateway 192.168.3.1
Subnet mask: 255.255.255.0

Run each section in the named device's console, in order.
Use the same interface names as your current GNS3 topology.
This assumes interface IP addresses are already configured and static routes have been removed.

============================================================
PC1 TERMINAL
============================================================
ip 192.168.1.2 255.255.255.0 192.168.1.1

============================================================
R1 TERMINAL — ENABLE RIP VERSION 2
============================================================
enable
configure terminal
router rip
version 2
no auto-summary
network 192.168.1.0
network 192.168.2.0
end

============================================================
R2 TERMINAL — ENABLE RIP VERSION 2
============================================================
enable
configure terminal
router rip
version 2
no auto-summary
network 192.168.2.0
network 192.168.3.0
end

============================================================
PC2 TERMINAL
============================================================
ip 192.168.3.2 255.255.255.0 192.168.3.1

============================================================
VERIFY ROUTING — RUN ON R1 AND R2
============================================================
show ip route

Wait briefly for RIP to exchange routes. Remote LAN routes should be marked R.

============================================================
TEST CONNECTIVITY
============================================================
On PC1:
ping 192.168.3.2

On PC2:
ping 192.168.1.2

'@
$target = Join-Path $PWD $filename
Set-Content -Path $target -Value $code -Encoding utf8
Write-Host "[OK] Saved: $filename (Theory embedded after line 50)" -ForegroundColor White
