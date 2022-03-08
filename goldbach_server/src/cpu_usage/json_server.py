import socket
import threading
import json
from time import sleep
import helpers as Helpers

# Thread safe Dict, only one thread can use it
class Dict():
  def __init__(self):
    self.memory= dict()
    self.can_use = threading.Lock()
  
  def update(self, ip, status):
    self.can_use.acquire()
    self.memory[ip] = status
    print("\nupdate "+str(self.memory))
    self.can_use.release()
  
  def get(self):
    self.can_use.acquire()
    memory = dict(self.memory)
    print("\nget "+str(self.memory))
    self.can_use.release()
    return memory

class Json_Server:
  def __init__(self, port):
    ip = self.getIP()
    self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    self.can_print = threading.Lock()
    self.storage = Dict()
    self.logAppend("Start listening on "+str(ip)+" port "+str(port))
    address = (ip,port)
    self.welcome_socket.bind(address)
    self.welcome_socket.listen(1)
  
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
    print("\n[JSON_SERVER] "+message)
    self.can_print.release()

  def listenClient(self):
    while True:
      connection, client_address = self.welcome_socket.accept()
      # Handle client on new thread with connection socket
      threading.Thread(target = self.handleConnection, args=(connection,),
        daemon = True).start()

  def handleConnection(self, connection):
    rcvd_message = Helpers.recvWebMessage(connection)
    rcvd_message = self.analyzeMessage(rcvd_message, connection)
    connection_type = rcvd_message[0]
    request = rcvd_message[1]
    if connection_type == "get_cpu":
      self.handle_get_cpu(connection)
    elif connection_type == "update_cpu":
      self.handle_update_cpu(request, connection)
    else:
      self.logAppend("Request has been ignored")
      pass

  def stop(self):
    self.logAppend("Shutting down server")
    self.welcome_socket.close()

  # @return connection_type
  # Connection types: get_cpu, update_cpu
  def analyzeMessage(self, rcvd_message, connection):
    address = connection.getpeername()
    connection_info = "New connection from: "+ str(address[0]) +" port "+str(address[1])+" ("
    connection_type = "get_cpu"
    request = rcvd_message
    if rcvd_message == "get_cpu":
      connection_type = rcvd_message
    elif rcvd_message[:11] == "update_cpu ":
      request = request.replace("update_cpu ", "")
      connection_type = "update_cpu"
    connection_info += connection_type+")"
    # if connection_type != "unknown":
    #   self.logAppend(connection_info)
    return connection_type, request

  def  handle_get_cpu(self, connection):
    memory = self.storage.get()
    header = "HTTP/1.1 200 OK\n"
    header += "Content-Type: text\n\n"
    response = header
    response = json.dumps(memory)
    response = response.encode("utf-8")
    connection.sendall(response)

  def handle_update_cpu(self, request, connection):
    status = json.loads(request)
    print(status)
    for key in status:
      ip = key
      cpu_status = status[key]
      self.storage.update(ip, cpu_status)
    connection.close()
  
def serverKiller(server):
  try:
    while True: sleep(99999)
  except KeyboardInterrupt:
    server.stop()

def start():
  server = Json_Server(Helpers.REQUEST_PORT)

  # daemon thread handle conections
  threading.Thread(target = server.listenClient, args=(),
    daemon = True).start()

