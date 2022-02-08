import socket
import threading
from time import time

# Protocol defined message size
PACKAGE_SIZE = 1024

# Server main socket
WELCOME_PORT = 5000
SERVER_IP = '172.31.172.232'

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
                threading.Thread(target = self.handleClient, args=(connection, client_address),
                  daemon = True).start()
                self.logAppend("Active connections "+ str(threading.active_count() -1))
        except KeyboardInterrupt:
            finish = time()
            print("\ntime: "+str(finish-start))
            self.stop()

    def handleClient(self, connection, client_address):
      connection_type = self.recvMessage(connection)
      self.logAppend("New connectiopn from: "+ str(client_address[0]) +" port "+str(client_address[1])+" ("+connection_type+")")
      if connection_type == "worker":
        while True:
          client_work = self.work_queue.dequeue()
          results_id = client_work[0]
          goldbach_number = client_work[1]
          self.sendMessage(connection, str(goldbach_number))
          self.logAppend("Client on "+str(client_address[1])+" is working in "+str(goldbach_number))
          client_results = self.recvMessage(connection)
          if client_results == "disconect":
            self.can_access_worker_count.acquire()
            self.worker_count += 1
            if self.worker_count == WORKERS:
              self.can_send_results.release()
            self.can_access_worker_count.release()
            break
          self.results.add(results_id, client_results)
      elif "client":
        while True:
          input_numbers = self.recvMessage(connection)
          if input_numbers == "disconect":
            break
          else:
            self.can_send_results.acquire()
            msg = ""
            ordered_results = self.results.get_all()
            for result in range(len(ordered_results), 0, -1):
              msg += str(ordered_results[result])
            results = msg
            self.sendMessage(connection, results)


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

# Thread safe queue, sleep thread when queue is empty
# Alternate betwen send and rcv 
class Queue():
  def __init__(self):
    # self.queue = [77401,412680,1753664,26084,806,58691,888888,34956,674,17027,84733,4123,10000000,953,6827,30733,61832,20134,86523,62132,3020,128594,62,536736,61610,288,39415,74074,8134,96274,1443614,17177,68515,8218212,133211,58165,677,9,-3,-20,27748,187322,99893,14194,1479,450,263586,2202020,8013,59811,23559,-104,7777]

    self.queue = [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]

    
    self.can_access_queue = threading.Lock()
    self.index = 0
  
  # Awake thread consumer of queue after add a new message
  def enqueue(self, message):
    self.queue.append(message)
  
  # Sleep thread consumer when queue is empty
  def dequeue(self):
    message = "stop"
    my_index = -1
    self.can_access_queue.acquire()
    if len(self.queue) > 0:
      message = self.queue.pop()
      self.index += 1
      my_index = self.index
    self.can_access_queue.release()
    return (my_index, message)

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