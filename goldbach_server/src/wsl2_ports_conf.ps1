# Server pc conf
$WSL_IP = "172.31.173.207"
$WELCOME_PORT = 5000

netsh interface portproxy add v4tov4 listenport=$WELCOME_PORT listenaddress=0.0.0.0 connectport=$WELCOME_PORT connectaddress=$WSL_IP
netsh interface portproxy show all