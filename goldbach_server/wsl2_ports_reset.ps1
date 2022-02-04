# # Server pc reset
# $CLIENT_COUNT = 3
# $FIRST_PORT = 5000

# for($i=0; $i -lt $CLIENT_COUNT+2; $i++){
#     $new_port = $FIRST_PORT+$i
#     netsh interface portproxy delete v4tov4 listenport=$new_port listenaddress=0.0.0.0
# }

# netsh interface portproxy show all

# Client pc reset
$FIRST_PORT = 5000

netsh interface portproxy delete v4tov4 listenport=$FIRST_PORT listenaddress=0.0.0.0

netsh interface portproxy show all