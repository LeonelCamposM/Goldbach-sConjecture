import socket
import threading
from time import time

# Protocol defined message size
PACKAGE_SIZE = 1024

# Server main socket
WELCOME_PORT = 5000
SERVER_IP = '172.31.161.171'

WORKERS = 1

class Server:
    def __init__(self, addr):
        # Create a TCP socket to recieve clients
        self.welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.can_print = threading.Lock()
        self.logAppend("Starting connection on "+str(addr[0])+" port "+str(addr[1]))
        self.work_queue = Queue()
        self.results = Dict()
        self.worker_count = 0
        self.can_access_worker_count = threading.Lock()
        self.can_send_results = threading.Semaphore(0)
        self.results_queue = Queue()
        
        # Start listening on main socket
        self.welcome_socket.bind(addr)
        self.welcome_socket.listen(1)

    def listenClient(self):
        start = time()
        try:
            # Main thread always keep listening
            while True:
                # Recieve connection from new client
                connection, client_address = self.welcome_socket.accept()
                # Handle connection on new thread
                threading.Thread(target = self.handleConnection, args=(connection, client_address),
                  daemon = True).start()
                self.logAppend("Active connections "+ str(threading.active_count() -1))
        except KeyboardInterrupt:
            finish = time()
            print("\ntime: "+str(finish-start))
            self.stop()

    def handleConnection(self, connection, client_address):
      connection_type = self.recvMessage(connection)
      self.logAppend("New connectiopn from: "+ str(client_address[0]) +" port "+str(client_address[1])+" ("+connection_type+")")
      if connection_type == "worker":
        self.handleWorker(connection, client_address, )
      elif "client":
        self.handleClient(connection)

    def stop(self):
        self.logAppend("Shutting down server")
        self.welcome_socket.close()
    
    def sendMessage(self, connection, message):
      message = self.fill_with_trash(message, PACKAGE_SIZE)
      connection.sendall(message)

    def recvMessage(self, connection):
        message = connection.recv(PACKAGE_SIZE)
        message = message.decode("utf-8")
        # Clean message thrash
        message = message.replace('$','')
        return message

    # Thread safe print
    def logAppend(self, message):
        self.can_print.acquire()
        print("\n[SERVER] "+message)
        self.can_print.release()
    
    # Add trash and encode a message
    def fill_with_trash(self, message, package_size):
      for index in range(package_size-len(message)):
          message += '$'
      return message.encode("utf-8")

    def handleWorker(self, connection, client_address):
      while True:
          client_work = self.work_queue.dequeue()
          if client_work == "wait":
            self.logAppend("Client on "+str(client_address[1])+" is working in "+str(client_work))
            self.can_send_results.release()
          else:
            client_work = str(client_work).split(",")
            results_id = client_work[0]
            goldbach_number = client_work[1]
            self.sendMessage(connection, str(goldbach_number))
            self.logAppend("Client on "+str(client_address[1])+" is working in "+str(goldbach_number))
            client_results = self.recvMessage(connection)
            self.results.add(results_id, client_results)
     
    def handleClient(self, connection):
      while True:
        input_numbers = self.recvMessage(connection)
        if input_numbers == "disconect":
          break
        else:
          #enqueue work
          input_numbers = str(input_numbers).split(",")
          self.work_queue.enqueue("wait")
          for number in range(0,len(input_numbers)):
            self.work_queue.enqueue(str(number)+","+str((input_numbers[number])))
          
          # wait to send results
          self.can_send_results.acquire()
          msg = ""
          ordered_results = self.results.get_all()
          for result in ordered_results:
            msg += str(ordered_results[result])
          self.sendMessage(connection, msg)
          break

# Thread safe queue, sleep thread when queue is empty
# Alternate betwen send and rcv 
class Queue():
  def __init__(self):
    self.queue= []
    self.can_acces_queue = threading.Semaphore(0)
    self.can_acces_last = threading.Lock()
  
  # Awake thread consumer of queue after add a new message
  def enqueue(self, message):
    self.queue.append(message)
    self.can_acces_queue.release()
  
  # Sleep thread consumer when queue is empty
  def dequeue(self):
    message = "stop"
    self.can_acces_queue.acquire()
    if len(self.queue) > 0:
      message = self.queue.pop()
    return message

# Only 1 thread can use it 
class Dict():
  def __init__(self):
    self.storage = dict()
    self.can_use_storage = threading.Lock()

  def get(self,key):
    self.can_use_storage.acquire()
    data = self.storage[key]
    self.can_use_storage.release()
    return data.copy()

  def add(self,key, value):
    self.can_use_storage.acquire()
    self.storage[key] = value
    self.can_use_storage.release()

  def delete(self, del_key):
    position = 0
    self.can_use_storage.acquire()
    for key,value in self.storage:
      if key == del_key:
        position = key
    self.storage.remove(position)
    self.can_use_storage.release()

  def get_all(self):
    self.can_use_storage.acquire()
    data = dict(self.storage)
    self.can_use_storage.release()
    return data
  
  def clear_dict(self):
    self.can_use_storage.acquire()
    self.storage = dict()
    self.can_use_storage.release()

if __name__ == "__main__":
  server_address = (SERVER_IP,WELCOME_PORT)
  server = Server(server_address)
  server.listenClient()