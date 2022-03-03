import socket
import os
from ctypes import CDLL
from time import time
import helpers as Helpers

goldbach_pthread = CDLL("./goldbach/bin/lib_goldbach_pthread.so")
goldbach_omp = CDLL("./goldbach/bin/lib_goldbach_omp.so")
goldbach_serial = CDLL("./goldbach/bin/lib_goldbach_serial.so")

class Worker():
  def __init__(self):
    self.server_address = (Helpers.SERVER_IP, Helpers.WELCOME_PORT)
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.logAppend('Connecting on %s port %s \n' % self.server_address)

  def logAppend(self, message):
    print("[Worker] "+message)

  # @brief Start worker - server communication protocol
  def start(self):
    self.server_socket.connect(self.server_address)
    Helpers.sendWebMessage("worker", self.server_socket)
    while True:
      work = Helpers.recvWebMessage(self.server_socket)
      if work == '':
        self.stop()
        break
      else:
        time_elapsed = self.writeGoldbachResults(work)
        response = self.readGoldbachResult()
        self.logAppend(response)
        worker_response = ""
        if time_elapsed != -1:
          worker_response += str(time_elapsed)+"&"
        Helpers.sendWorkerMessage(self.server_socket, worker_response+response)

  def stop(self):
    self.logAppend("closing sockets...")
    self.server_socket.close()
  
  # @brief Write results of work in Output.txt
  # @param work string with goldbach_number,calculator_name,calculator
  def writeGoldbachResults(self, work):
    work = work.split(",")
    goldbach_number = work[0]
    calculator_name = work[1]
    unified_work = work[2]
    calculator = self.getCalculator(calculator_name)
    time_elapsed = -1
    if unified_work == "False":
      calculator.calculate_number(int(goldbach_number))
    else:
      time_elapsed = self.getSingleWorkerResults(calculator, goldbach_number)
    return time_elapsed

  # @brief Read Output.txt and return it in a string
  def readGoldbachResult(self):
    result = ""
    file = open('Output.txt','r')
    lines = file.readlines()
    for line in lines:
      result+= line
    os.remove("Output.txt")
    return result

  # @param calculator_name name of calculator to be used
  def getCalculator(self, calculator_name):
    calculator = goldbach_omp
    if calculator_name == "serial":
      calculator =  goldbach_serial
    elif calculator_name == "pthread":
      calculator =  goldbach_pthread
    return calculator

  # @brief Get results from a single worker with no communication latency
  # @param calculator_name name of calculator to be used
  # @param work string of numbers separated by %2C
  # @return time_elapsed
  def getSingleWorkerResults(self, calculator, work):
    work = work.split("%2C")
    c_array = calculator.array_create()
    for number in work:
      calculator.array_append(c_array,int(number))
    start = time()
    calculator.calculate_array(c_array)
    finish = time()
    time_elapsed = finish-start
    time_elapsed = str(round(time_elapsed,5))
    return time_elapsed

if __name__ == "__main__":
  client = Worker()
  client.start()