# Number of worker pc's
$CONSUMERS_COUNT = 3
$WSL_IP = "172.31.174.166"
$FIRST_PORT = 5000

for($i=0; $i -lt $CONSUMERS_COUNT; $i++){
    $new_port = $FIRST_PORT+$i
    netsh interface portproxy add v4tov4 listenport=$new_port listenaddress=0.0.0.0 connectport=$new_port connectaddress=$WSL_IP
}

netsh interface portproxy show all