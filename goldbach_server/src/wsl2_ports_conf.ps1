$WSL_IP = wsl hostname -I
$WELCOME_PORT = 5000

clear

${menu} = " ","Port configuration for wsl", "1) Configure port", "2) Reset port"," "
${menu}

$input = Read-Host "Choice (1-2) "
$condition = $input -eq "1"
if ( $condition )
{
    # Server pc configuration
    $open_port = "netsh interface portproxy add v4tov4 listenport=$WELCOME_PORT listenaddress=0.0.0.0 connectport=$WELCOME_PORT connectaddress=$WSL_IP"

    $unable_firewall = "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"
    Start-Process powershell -Verb RunAs -Wait -ArgumentList $open_port
    Start-Process powershell -Verb RunAs -Wait -ArgumentList $unable_firewall
    
    netsh interface portproxy show all
    Write-Host "Successful configuration"
    Write-Host " "
    $input = Read-Host "Press any key to exit"
}else
{
    # Server pc reset
    $close_port = "netsh interface portproxy delete v4tov4 listenport=$WELCOME_PORT listenaddress=0.0.0.0"

    $able_firewall = "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"
    Start-Process powershell -Verb RunAs -Wait -ArgumentList $close_port
    Start-Process powershell -Verb RunAs -Wait -ArgumentList $able_firewall
    
    netsh interface portproxy show all
    Write-Host "Successful reset"
    Write-Host " "
    $input = Read-Host "Press any key to exit"
}