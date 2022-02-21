from time import time
import threading
from traceback import print_tb

# Protocol defined message size
PACKAGE_SIZE = 1024

class Result_Package():
  def __init__(self, work_package, worker_response):
    self.work_package = work_package
    self.worker_response = worker_response

class Work_Package():
  def __init__(self, input_id, number, client_id, request_size, start):
    self.input_id = input_id
    self.number = number
    self.client_id = client_id
    self.request_size = request_size
    self.start = start

class Results_Dispatcher:
  def __init__(self):
    self.queues = dict()
  
  def start(self, results, responses):
    while True:
      result_package = results.dequeue()
      work_package = result_package.work_package
      if result_package.worker_response == "stop":
        break
      else:
        client_queue = self.queues.setdefault(work_package.client_id, [])
        client_queue.append((result_package.worker_response, work_package.input_id))
        if len(client_queue) == work_package.request_size:
          finish = time()
          final_time = finish - work_package.start
          goldbach_result = (work_package.client_id, client_queue, final_time)
          print("\n")
          print(str(client_queue))
          print("\n")
          responses.enqueue(goldbach_result)
          self.queues.pop(work_package.client_id)


# Thread safe queue, sleep thread when queue is empty
# Alternate betwen send and rcv 
class Queue():
  def __init__(self):
    self.queue= []
    self.can_pop = threading.Semaphore(0)
  
  # Awake thread consumer of queue after add a new message
  def enqueue(self, message):
    self.queue.append(message)
    self.can_pop.release()
  
  # Sleep thread consumer when queue is empty
  def dequeue(self):
    self.can_pop.acquire()
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

class Goldbach_Web:
  def __init__(self):
    self.work_queue = Queue()
    self.results_queue = Queue()
    self.response_queue = Queue()

    self.results = Dict()
    self.can_send_results = threading.Semaphore(0)
    self.can_print = threading.Lock()

    dispatcher = Results_Dispatcher()
    threading.Thread(target = dispatcher.start, args=(self.results_queue,self.response_queue),
      daemon = True).start()

    threading.Thread(target = self.responseSender, args=(self.response_queue,),
      daemon = True).start()
    

  def handleWorker(self, connection):
    while True:
      work = self.work_queue.dequeue()
      goldbach_number = work.number
      self.sendMessage(connection, str(goldbach_number))
      self.logAppend("Client on "+str(work.client_id.getsockname()[1])+" is working in "+str(goldbach_number))
      worker_response = self.recvWorkerMessage(connection)
      print("lego "+str(worker_response))
      result_package = Result_Package(work, worker_response)
      self.results_queue.enqueue(result_package)
    
  def handleRequest(self, request, connection):
    request = request.replace('/goldbach?number=','')
    print(request)
    input_numbers = request.split("%2C")
    
    #enqueue work
    for input_id in range(0,len(input_numbers)):
      request_size = len(input_numbers)
      number = input_numbers[input_id]
      client_id = connection
      start = time()
      work_package = Work_Package(input_id, number,client_id, request_size, start)
      print(work_package.request_size, work_package.number)
      self.work_queue.enqueue(work_package)

  def responseSender(self, responses):
    while True:
      goldbach_result = responses.dequeue()
      connection = goldbach_result[0]
      results = goldbach_result[1]
      time = goldbach_result[2]
      self.serveGoldbachresults(connection, results, time)
      connection.close()

  def serveGoldbachresults(self,connection, results, time):
    results_str = ""
    for result in results:
      results_str += str(result[0])+"<br>"+"<br>"
    self.logAppend(results_str)
    header = "HTTP/1.1 200 OK\n    <label for=\"number\">Number</label>\n"
    header += "Content-Type: text/html\n\n"
    
    file = open("html/results.html", "r")
    response = header
    for line in file:
      response += line

    response = response.replace("(time)", str(round(time,5)))
    response = response.replace("(result)", results_str)
    # self.logAppend(response)
    response = response.encode("utf_8")
    connection.sendall(response)
  
  # Add trash and encode a message
  def fill_with_trash(self, message, package_size):
    for index in range(package_size-len(message)):
      message += '$'
    return message.encode("utf-8")

  def sendMessage(self, connection, message):
    message = self.fill_with_trash(message, PACKAGE_SIZE)
    connection.sendall(message)

  def recvMessage(self, connection):
    message = connection.recv(PACKAGE_SIZE)
    message = message.decode("utf-8")
    # Clean message thrash
    message = message.replace('$','')
    return message

  def recvWorkerMessage(self, connection):
    buffer = ""
    message = ""
    while True:
      message = connection.recv(PACKAGE_SIZE)
      print("mensajito "+str(message))
      message = message.decode("utf-8")
      # Clean message thrash
      message = message.replace('$','')
      if "end" in message:
        message = message.replace('end','')
        buffer += message
        break
      else:
        buffer += message
    return buffer

    # Thread safe print
  def logAppend(self, message):
    self.can_print.acquire()
    print("\n[Goldbach] "+message)
    self.can_print.release()

    








