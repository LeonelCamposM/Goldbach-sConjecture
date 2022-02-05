import socket
import threading
from time import sleep

# Protocol defined message size
PACKAGE_SIZE = 1024

# Server main socket
WELCOME_PORT = 5000
SERVER_IP = '172.31.172.203'

class Server:
    def __init__(self, addr):
        # Create a TCP socket to recieve clients
        self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.can_print = threading.Lock()
        self.logAppend("Starting connection on "+str(addr[0])+" port "+str(addr[1]))

        # Start listening on main socket
        self.welcome_socket.bind(addr)
        self.welcome_socket.listen(1)

    def listenClient(self):
        try:
            # Main thread always keep listening
            while True:
                # Recieve connection from new client
                connection, client_address = self.welcome_socket.accept()
                # Handle connection on new thread
                threading.Thread(target = self.handleClient, args=(connection, client_address),
                  daemon = True).start()
                self.logAppend("Active connections "+ str(threading.active_count() -1))
        except KeyboardInterrupt:
            self.stop()

    def handleClient(self, connection, client_address):
        self.logAppend('New connectiopn from: %s port %s' % client_address)
        available_threads = self.recvMessage(connection)
        self.logAppend("Client on "+str(client_address[1])+" has "+available_threads+" threads")
        while True:
            sleep(5)

    def stop(self):
        self.logAppend("Shutting down server")
        self.welcome_socket.close()
    
    def sendMessage(self, connection, message):
        message = message.encode("utf-8")
        connection.sendall(message)

    def recvMessage(self, connection):
        message = connection.recv(PACKAGE_SIZE)
        message = message.decode("utf-8")
        return message

    # Thread safe print
    def logAppend(self, message):
        self.can_print.acquire()
        print("\n[SERVER] "+message)
        self.can_print.release()

if __name__ == "__main__":
    server_address = (SERVER_IP,WELCOME_PORT)
    server = Server(server_address)
    server.listenClient()
