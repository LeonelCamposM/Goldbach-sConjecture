# Server pc conf
$WSL_IP = "172.31.173.207"
$WELCOME_PORT = 5000

netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.31.161.171

netsh interface portproxy show all