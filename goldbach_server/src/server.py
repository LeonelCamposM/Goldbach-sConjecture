import socket
import threading
import goldbach.goldbach_web as Goldbach_Web

# Protocol defined message size
PACKAGE_SIZE = 1024

# Server main socket
WELCOME_PORT = 5000
SERVER_IP = '172.17.118.225'

class Server:
  def __init__(self, addr):
    # Create a TCP socket to recieve clients
    self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    
    # Thread safe print
    self.can_print = threading.Lock()
    self.logAppend("Start listening on "+str(addr[0])+" port "+str(addr[1]))

    # Start listening on main socket
    self.welcome_socket.bind(addr)
    self.welcome_socket.listen(1)

    # Web apps
    self.goldbach = Goldbach_Web.Goldbach_Web()
    
  def stop(self):
    self.logAppend("Shutting down server")
    self.welcome_socket.close()

  def listenClient(self):
    try:
      # Main thread always keep listening
      while True:
        # Recieve connection from new client
        connection, client_address = self.welcome_socket.accept()
        # Handle connection on new thread
        threading.Thread(target = self.handleConnection, args=(connection,),
          daemon = True).start()
        self.logAppend("Active connections "+ str(threading.active_count() -1))
    except KeyboardInterrupt:
      self.stop()

  # Handle client, worker connection
  def handleConnection(self, connection):
    client_address = connection.getsockname()
    rcvd_message = self.recvMessage(connection)
    connection_info = "New connection from: "+ str(client_address[0]) +" port "+str(client_address[1])

    if rcvd_message == "worker":
      connection_info += " ("+rcvd_message+")"
      self.logAppend(connection_info)
      self.goldbach.handleWorker(connection)
    else:
      connection_info += " ("+"client"+")"
      self.logAppend(connection_info)
      self.handleClient(connection, rcvd_message)
  
  def sendMessage(self, connection, message):
    message = message.encode("utf-8")
    connection.sendall(message)

  def recvMessage(self, connection):
    message = connection.recv(PACKAGE_SIZE)
    message = message.decode("utf-8")
    message = message.replace('$','')
    return message

  # Thread safe print
  def logAppend(self, message):
    self.can_print.acquire()
    print("\n[SERVER] "+message)
    self.can_print.release()
    
  def handleClient(self, connection, request):
    client_request = (request.split(" "))[1]
    header = str(client_request)[1:17]
    if header == "":
      self.serveHomepage(connection)
    elif header == "goldbach?number=":
      self.goldbach.handleRequest(request, connection)
    else:
      pass

  def serveHomepage(self,connection):
    self.goldbach.serveHomepage2(connection)

if __name__ == "__main__":
  server_address = (SERVER_IP, WELCOME_PORT)
  server = Server(server_address)
  server.listenClient()