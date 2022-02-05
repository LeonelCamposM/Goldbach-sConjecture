# Server pc conf
# $CLIENT_COUNT = 3
$WSL_IP = "172.31.173.207"
$FIRST_PORT = 5000

netsh interface portproxy add v4tov4 listenport=$FIRST_PORT listenaddress=0.0.0.0 connectport=$FIRST_PORT connectaddress=$WSL_IP

# for($i=0; $i -lt ($CLIENT_COUNT+2); $i++){
#     $new_port = $FIRST_PORT+$i
#     netsh interface portproxy add v4tov4 listenport=$new_port listenaddress=0.0.0.0 connectport=$new_port connectaddress=$WSL_IP
# }

# netsh interface portproxy show all

# # Client pc conf
# $WSL_IP = "172.31.174.166"
# $FIRST_PORT = 5000

# netsh interface portproxy add v4tov4 listenport=$FIRST_PORT listenaddress=0.0.0.0 connectport=$FIRST_PORT connectaddress=$WSL_IP

# netsh interface portproxy show all