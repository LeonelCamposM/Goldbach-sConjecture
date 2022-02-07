import socket
import threading
from time import sleep
from unittest import result

# Protocol defined message size
PACKAGE_SIZE = 1024

# Server main socket
WELCOME_PORT = 5000
SERVER_IP = '172.31.161.60'

class Server:
    def __init__(self, addr):
        # Create a TCP socket to recieve clients
        self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.can_print = threading.Lock()
        self.logAppend("Starting connection on "+str(addr[0])+" port "+str(addr[1]))
        self.work_queue = Queue()

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
        while True:
            client_work = self.work_queue.dequeue()
            self.sendMessage(connection, str(client_work))
            self.logAppend("Client on "+str(client_address[1])+" is working in "+str(client_work))
            results = self.recvMessage(connection)
            self.logAppend("Client on "+str(client_address[1])+" results: "+str(results))
            if results == "print":
                break

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

# Thread safe queue, sleep thread when queue is empty
# Alternate betwen send and rcv 
class Queue():
  def __init__(self):
    self.queue = [77401,412680,1753664,26084,806,58691,888888,34956,674,17027,84733,4123,10000000,953,6827,30733,61832,20134,86523,62132,3020,128594,62,536736,61610,288,39415,74074,8134,96274,1443614,17177,68515,8218212,133211,58165,677,9,-3,-20,27748,187322,99893,14194,1479,450,263586,2202020,8013,59811,23559,-104,7777]
    self.can_access_queue = threading.Lock()
    self.last = True
  
  # Awake thread consumer of queue after add a new message
  def enqueue(self, message):
    self.queue.append(message)
  
  # Sleep thread consumer when queue is empty
  def dequeue(self):
    message = "stop"
    self.can_access_queue.acquire()
    if len(self.queue) > 0:
      message = self.queue.pop()
    self.can_access_queue.release()
    return message

if __name__ == "__main__":
    server_address = (SERVER_IP,WELCOME_PORT)
    server = Server(server_address)
    server.listenClient()
