import socket
import threading
import goldbach.goldbach_web as Goldbach_Web
import helpers as Helpers

class Server:
  def __init__(self, port):
    ip = self.getIP()

    self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    
    self.can_print = threading.Lock()
    self.logAppend("Start listening on "+str(ip)+" port "+str(port))

    address = (ip,port)
    self.welcome_socket.bind(address)
    self.welcome_socket.listen(1)

    # Web apps
    self.goldbach = Goldbach_Web.Goldbach_Web()
  
  def getIP(self):
    ip = 'NULL'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
      sock.connect(('8.8.8.8', 1))
      ip = sock.getsockname()[0]
    except Exception:
      pass
    sock.close()
    assert ip != 'NULL', "[SERVER] Could not get machine ip\n"
    return ip

  # Thread safe print
  def logAppend(self, message):
    self.can_print.acquire()
    print("\n[SERVER] "+message)
    self.can_print.release()

  def listenClient(self):
    try:
      while True:
        connection, client_address = self.welcome_socket.accept()
        # Handle client on new thread with connection socket
        threading.Thread(target = self.handleConnection, args=(connection,),
          daemon = True).start()
    except KeyboardInterrupt:
      self.stop()
  
  def stop(self):
    self.logAppend("Shutting down server")
    self.welcome_socket.close()

  def handleConnection(self, connection):
    rcvd_message = Helpers.recvWebMessage(connection)
    message = self.analyzeMessage(rcvd_message, connection)

    connection_type = message[0]
    request = message[1]

    if connection_type == "worker":
      self.goldbach.handleWorker(connection)
    elif connection_type == "home":
      self.serveHomepage(connection)
    elif connection_type == "goldbach":
      request = request.split("&")
      calculator = request[0].replace("calculator=","")
      numbers = request[1].replace("number=","")
      self.goldbach.handleRequest(numbers, calculator, connection)
    else:
      # self.logAppend("Request :"+request+" to "+connection_type+" has been ignored")
      pass

  # Return connection type, request
  # Connection types: worker, home, goldbach
  def analyzeMessage(self, rcvd_message, connection):
    address = connection.getpeername()
    connection_info = "New connection from: "+ str(address[0]) +" port "+str(address[1])+" ("
    connection_type = ""
    request = ""
    if rcvd_message == "worker":
      connection_type = rcvd_message
    else:
      request = (rcvd_message.split(" "))[1]
      header = str(request)[1:9]
      request = request.replace(header,"")
      request = request.replace("/","")
      request = request.replace("?","")
      if header == "":
        connection_type = "home"
      elif header == "goldbach?number=":
        connection_type= "goldbach"
      else:
        connection_type= header
    connection_info += connection_type+")"
    if connection_type != "favicon.":
      self.logAppend(connection_info)
    return (connection_type, request)
    
  def serveHomepage(self,connection):
    home_page = Helpers.loadHTML("home")
    Helpers.sendWebMessage(home_page, connection)
    connection.close()

if __name__ == "__main__":
  server = Server(Helpers.WELCOME_PORT)
  server.listenClient()