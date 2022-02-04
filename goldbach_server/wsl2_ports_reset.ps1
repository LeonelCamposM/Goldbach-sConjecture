# Number of worker pc's
$CONSUMERS_COUNT = 3
$FIRST_PORT = 5000

for($i=0; $i -lt $CONSUMERS_COUNT; $i++){
    $new_port = $FIRST_PORT+$i
    netsh interface portproxy delete v4tov4 listenport=$new_port listenaddress=0.0.0.0
}

netsh interface portproxy show all