# Server pc reset
$WELCOME_PORT = 5000

netsh interface portproxy delete v4tov4 listenport=$WELCOME_PORT listenaddress=0.0.0.0
netsh interface portproxy show all