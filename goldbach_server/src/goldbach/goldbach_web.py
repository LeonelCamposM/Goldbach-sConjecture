from time import time
import threading
import helpers as Helpers

# Protocol defined message size
PACKAGE_SIZE = 1024

class Result_Package():
  def __init__(self, work_package, worker_response):
    self.work_package = work_package
    self.worker_response = worker_response

class Work_Package():
  def __init__(self, input_id, number, client_id, request_size, start, calculator, unified_workload):
    self.input_id = input_id
    self.number = number
    self.client_id = client_id
    self.request_size = request_size
    self.start = start
    self.calculator = calculator
    self.unified_workload = unified_workload
    self.final_time = -1

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

class Goldbach_Web:
  def __init__(self):
    self.work_queue = Queue()
    self.result_queue = Queue()
    self.response_queue = Queue()
    self.can_print = threading.Lock()

    self.dispatch_queues = dict()
    threading.Thread(target = self.dispatcher, args=(),
      daemon = True).start()

    threading.Thread(target = self.responseSender, args=(),
      daemon = True).start()

  def serveGoldbachresults(self,connection, results, time):
    results_str = ""
    for result in results:
      results_str += str(result[0])+"<br>"+"<br>"
    html = Helpers.loadHTML("results")
    html = html.replace("(time)", str(round(time,5)))
    html = html.replace("(result)", results_str)
    html = html.encode("utf_8")
    connection.sendall(html)

  # Thread safe print
  def logAppend(self, message):
    self.can_print.acquire()
    print("\n[Goldbach] "+message)
    self.can_print.release()

  # [Thread]
  # Send number to workers and enqueue result in self.result_queue
  def handleWorker(self, connection):
    while True:
      work = self.work_queue.dequeue()
      goldbach_number = work.number
      self.logAppend("Client on "+str(connection.getpeername()[1])+" is working in "+str(goldbach_number))
      worker_request = str(goldbach_number)+","+work.calculator+","+str(work.unified_workload)
      Helpers.sendWebMessage(worker_request, connection)
      worker_response = Helpers.recvWorkerMessage(connection)
      if work.unified_workload == "True":
        worker_response = worker_response.split("&")
        work.final_time = float(worker_response[0])
        worker_response = worker_response[1]
      result_package = Result_Package(work, worker_response)
      self.result_queue.enqueue(result_package)
  
  # [Thread]
  # Produces a work packages from a request 
  # and queues them in in self.work_queue
  def handleRequest(self, request, calculator, connection, unified_workload):
    if unified_workload == False:
      self.handleDistributedWork(request, connection, calculator)
    else:
      self.handleUnifiedWork(request, connection, calculator)

  def handleDistributedWork(self, request, connection, calculator):
    input_numbers = request.split("%2C") 
    for input_id in range(0,len(input_numbers)):
      request_size = len(input_numbers)
      number = input_numbers[input_id]
      client_id = connection
      start = time()
      work_package = Work_Package(input_id, number,client_id, request_size, start, calculator, "False")
      self.work_queue.enqueue(work_package)

  def handleUnifiedWork(self, request, connection, calculator):
    request_size = 1
    number = request
    client_id = connection
    start = -1
    work_package = Work_Package(1, number,client_id, request_size, start, calculator, "True")
    self.work_queue.enqueue(work_package)

  # [Thread]
  # Create and send html response 
  # Consumer thread from self.response_queue
  def responseSender(self):
    while True:
      goldbach_result = self.response_queue.dequeue()
      connection = goldbach_result[0]
      results = goldbach_result[1]
      time = goldbach_result[2]
      self.serveGoldbachresults(connection, results, time)
      connection.close()
  
  # [Thread]
  # Consumer thread from self.result_queue
  # Produce on client_queue on self.dispatch_queues
  # Produce on sel.response whem client_queue is full
  def dispatcher(self):
    while True:
      result_package = self.result_queue.dequeue()
      work_package = result_package.work_package
      client_queue = self.dispatch_queues.setdefault(work_package.client_id, [])
      client_queue.append((result_package.worker_response, work_package.input_id))
      if len(client_queue) == work_package.request_size:
        finish = time()
        if work_package.final_time == -1:
          work_package.final_time = finish - work_package.start
        goldbach_result = (work_package.client_id, client_queue, work_package.final_time)
        self.response_queue.enqueue(goldbach_result)
        self.dispatch_queues.pop(work_package.client_id)








