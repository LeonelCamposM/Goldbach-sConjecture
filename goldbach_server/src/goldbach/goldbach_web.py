from time import time
import threading

# Protocol defined message size
PACKAGE_SIZE = 1024

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

class Goldbach_Web:
  def __init__(self):
    self.work_queue = Queue()
    self.results_queue = Queue()

    self.results = Dict()
    self.worker_count = 0
    self.can_access_worker_count = threading.Lock()
    self.can_send_results = threading.Semaphore(0)
    self.can_print = threading.Lock()

  def handleWorker(self, connection):
    client_address = connection.getsockname()
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
    
  def handleRequest(self, request, connection):
    #elif client_request[1:17] == "goldbach?number=":
    input_numbers = request[21:].split("%2C")
    last_number = input_numbers[len(input_numbers)-1]
    input_numbers[len(input_numbers)-1] = last_number.split(" ",1)[0]
    print(input_numbers[len(input_numbers)-1])
    start = time()
    
    #enqueue work
    self.work_queue.enqueue("wait")
    for number in range(0,len(input_numbers)):
      #TODO
      a = input_numbers[number]
      print(a)
      self.work_queue.enqueue(str(number)+","+str((input_numbers[number])))

    # wait to send results
    self.can_send_results.acquire()
    msg = ""
    ordered_results = self.results.get_all()
    for result in ordered_results:
        msg += "<br>"
        msg += str(ordered_results[result])
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