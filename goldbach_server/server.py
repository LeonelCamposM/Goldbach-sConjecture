import socket
import threading

# protocol defined message size
PACKAGE_SIZE = 1024

# server main socket
WELCOME_PORT = 5000
SERVER_IP = '172.31.173.207'

# template of new user socket info
#COMM_IP = '172.31.171.155'
COMM_PORT = 5001
#COMM_ADDR = (COMM_IP, COMM_PORT)


class Server:
    def __init__(self, addr):
        # Create a TCP socket to recieve clients
        self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        print ('\n[Server] Starting connection on %s port %s \n' % addr)

        # Start listening on main socket
        self.welcome_socket.bind(addr)
        self.welcome_socket.listen(1)

    def listenClient(self):
        try:
             # main thread always keep listening
            while True:
                # recieve connection from new client
                connection, clientAddress = self.welcome_socket.accept()
                #handle connection on new thread
                threading.Thread(target = self.handleClient, args=(connection, clientAddress),
                  daemon = True).start()
                print(f"\n[Server] Active connections {threading.active_count() -1}")
        except KeyboardInterrupt:
            self.stop()

    def handleClient(self, connection, clientAddress):
        print ('\n[Server] New connectiopn from: %s port %s \n' % clientAddress)
        msj = "server say hi".encode("utf-8")
        connection.sendall(msj)
        msj2 = connection.recv(1024)
        print(msj2)

    def stop(self):
        print("\n[Server] Shutting down server")
        self.welcome_socket.close()

if __name__ == "__main__":
    server_address = (SERVER_IP,WELCOME_PORT)
    server = Server(server_address)
    server.listenClient()



