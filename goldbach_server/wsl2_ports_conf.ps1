$WSL_IP = wsl hostname -I
$WELCOME_PORT = 8001

clear

${menu} = " ","Port configuration for wsl", "1) Configure port", "2) Reset port"," "
${menu}

$input = Read-Host "Choice (1-2) "
$condition = $input -eq "1"
if ( $condition )
{
    # Server pc configuration
    $command = "netsh interface portproxy add v4tov4 listenport=$WELCOME_PORT listenaddress=0.0.0.0 connectport=$WELCOME_PORT connectaddress=$WSL_IP"
    Start-Process powershell -Verb RunAs -Wait -ArgumentList $command

    netsh interface portproxy show all
    Write-Host "Successful configuration"
    Write-Host " "
    $input = Read-Host "Press any key to exit"
}else
{
    # Server pc reset
    $command = "netsh interface portproxy delete v4tov4 listenport=$WELCOME_PORT listenaddress=0.0.0.0"
    Start-Process powershell -Verb RunAs -Wait -ArgumentList $command
    
    netsh interface portproxy show all
    Write-Host "Successful reset"
    Write-Host " "
    $input = Read-Host "Press any key to exit"
}