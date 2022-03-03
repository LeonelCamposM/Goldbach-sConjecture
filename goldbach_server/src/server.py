import socket
import threading
import goldbach.goldbach_web as Goldbach_Web
import helpers as Helpers

class Server:
  def __init__(self, port):
    ip = self.getIP()
    self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    self.can_print = threading.Lock()
    self.logAppend("Start listening on "+str(ip)+" port "+str(port))
    address = (ip,port)
    self.welcome_socket.bind(address)
    self.welcome_socket.listen(1)

    # Web apps
    self.goldbach = Goldbach_Web.Goldbach_Web()
  
  # @brief Gets ip of machine where server is running
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

  def handleConnection(self, connection):
    rcvd_message = Helpers.recvWebMessage(connection)
    rcvd_message = self.analyzeMessage(rcvd_message, connection)
    connection_type = rcvd_message[0]
    request = rcvd_message[1]
    if connection_type == "worker":
      self.goldbach.handleWorker(connection)
    elif connection_type == "home":
      self.serveHomepage(connection)
    elif connection_type == "goldbach":
      arguments = self.parseGoldbachArguments(request)
      unified_workload = arguments[0]
      calculator = arguments[1]
      numbers = arguments[2]
      self.goldbach.handleRequest(numbers, calculator, connection, unified_workload)
    else:
      # self.logAppend("Request :"+request+" has been ignored")
      pass

  def stop(self):
    self.logAppend("Shutting down server")
    self.welcome_socket.close()

  # @return (connection_type, request)
  # Connection types: worker, home, goldbach
  def analyzeMessage(self, rcvd_message, connection):
    address = connection.getpeername()
    connection_info = "New connection from: "+ str(address[0]) +" port "+str(address[1])+" ("
    request = ""
    connection_type = "unknown"
    if rcvd_message == "worker":
      connection_type = rcvd_message
    else:
      request = (rcvd_message.split(" "))[1]
      parsed_request = self.parseRequest(request)
      connection_type = parsed_request[0]
      request = parsed_request[1]
    connection_info += connection_type+")"
    if connection_type != "unknown":
      self.logAppend(connection_info)
    return (connection_type, request)
  
  # @brief Clean request and get connection type
  # @return (connection_type, request)
  def parseRequest(self, request):
    connection_type = "unknown"
    header = str(request)[1:9]
    request = request.replace(header,"")
    request = request.replace("/","")
    request = request.replace("?","")
    if header == "":
      connection_type = "home"
    elif header == "goldbach":
      connection_type = header
    return (connection_type, request)
  
  # @param request provided by analyzeMessage()
  # @return (unified_workload, calculator, numbers)
  def parseGoldbachArguments(self, request):
    request = request.split("&")
    if len(request) > 2:
      unified_workload = True
      calculator = request[1].replace("calculator=","")
      numbers = request[2].replace("number=","")
    else:
      unified_workload = False
      calculator = request[0].replace("calculator=","")
      numbers = request[1].replace("number=","")
    return (unified_workload, calculator, numbers)

  def serveHomepage(self,connection):
    home_page = Helpers.loadHTML("home")
    Helpers.sendWebMessage(home_page, connection)
    connection.close()

if __name__ == "__main__":
  server = Server(Helpers.WELCOME_PORT)
  server.listenClient()