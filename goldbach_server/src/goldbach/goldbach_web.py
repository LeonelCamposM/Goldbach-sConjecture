from time import time
import threading

# Protocol defined message size
PACKAGE_SIZE = 1024

class Result_Package():
  def __init__(self, work_package, worker_response):
    self.work_package = work_package
    self.worker_response = worker_response

class Work_Package():
  def __init__(self, input_id, number, client_id, request_size):
    self.input_id = input_id
    self.number = number
    self.client_id = client_id
    self.request_size = request_size

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
        client_queue.append(result_package.worker_response)
        print("dispatch queue:"+ str(client_queue))
        if len(client_queue) == work_package.request_size:
          responses.enqueue(client_queue)
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
    

  def handleWorker(self, connection):
    while True:
      work = self.work_queue.dequeue()
      goldbach_number = work.number
      self.sendMessage(connection, str(goldbach_number))
      self.logAppend("Client on "+str(work.client_id)+" is working in "+str(goldbach_number))
      worker_response = self.recvMessage(connection)
      result_package = Result_Package(work, worker_response)
      self.results_queue.enqueue(result_package)
    
  def handleRequest(self, request, connection):
    input_numbers = request[21:].split("%2C")
    last_number = input_numbers[len(input_numbers)-1]
    input_numbers[len(input_numbers)-1] = last_number.split(" ",1)[0]
    client_address = connection.getsockname()
    
    start = time()
    #enqueue work
    for input_id in range(0,len(input_numbers)):
      request_size = len(input_numbers)
      number = input_numbers[input_id]
      client_id = client_address[1]
      work_package = Work_Package(input_id, number,client_id, request_size)

      #TODO
      a = work_package.number
      print(a)

      self.work_queue.enqueue(work_package)
    
    msg = ""
    ordered_results = self.response_queue.dequeue()
    print(ordered_results)
    for result in ordered_results:
      msg += "<br>"
      msg += str(result)
    finish = time()
    msg += "<br>"
    msg +=("time: "+str(finish-start))
    self.serveGoldbachresults(connection, msg)

  def serveGoldbachresults(self,connection, results):
    title = "Goldbach sums"
    response = "<html lang=\"en\">\n  <meta charset=\"ascii\"/>\n  <title>" + title + "</title>\n\n"+"<h2>"+ title+"<br>"+results + "</h2>\n\n</html>\n"

    header = "HTTP/1.1 200 OK\n    <label for=\"number\">Number</label>\n"
    mimetype = "text/html"
    header += "Content-Type: "+mimetype+"\n\n"

    home_page = header
    home_page += response
    home_page = home_page.encode("utf_8")
    connection.sendall(home_page)

  def serveHomepage2(self,connection):
    title = "Goldbach sums"
    response = "<html lang=\"en\">\n  <meta charset=\"ascii\"/>\n  <title>" + title + "</title>\n  <style>body {font-family: monospace}</style>\n  <h1>" + title + "</h1>\n  <form method=\"get\" action=\"/goldbach\">\n <input type=\"text\" name=\"number\" required/>\n    <button type=\"submit\">Calculate</button>\n  </form>\n</html>\n"

    header = "HTTP/1.1 200 OK\n    <label for=\"number\">Number</label>\n"
    mimetype = "text/html"
    header += "Content-Type: "+mimetype+"\n\n"

    home_page = header
    home_page += response
    home_page = home_page.encode("utf_8")
    connection.sendall(home_page)
  
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

    # Thread safe print
  def logAppend(self, message):
    self.can_print.acquire()
    print("\n[SERVER] "+message)
    self.can_print.release()

    








