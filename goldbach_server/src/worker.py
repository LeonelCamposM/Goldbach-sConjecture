import socket
import os
from ctypes import CDLL
import threading
from time import sleep, time
import helpers as Helpers
import subprocess
import shutil
import psutil
import json
import requests

class Worker():
  def __init__(self):
    self.server_address = (Helpers.SERVER_IP, Helpers.WELCOME_PORT)
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.logAppend('Connecting on %s port %s \n' % self.server_address)
    self.goldbach_pthread = CDLL("./goldbach/bin/lib_goldbach_pthread.so")
    self.goldbach_omp = CDLL("./goldbach/bin/lib_goldbach_omp.so")
    self.goldbach_serial = CDLL("./goldbach/bin/lib_goldbach_serial.so")

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
        worker_response = ""
        if time_elapsed != -1:
          self.logAppend("\n"+response)
          worker_response += str(time_elapsed)+"&"
        else:
          self.logAppend(response)
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
    calculator = self.goldbach_omp
    if calculator_name == "serial":
      calculator =  self.goldbach_serial
    elif calculator_name == "pthread":
      calculator =  self.goldbach_pthread
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
    
def shell(command):
  subprocess.check_output(command, shell=True)

def makeGoldbachCalculators():
  os.chdir("..")
  os.chdir("..")
  program_names = ["goldbach_serial", "goldbach_pthread", "goldbach_omp"]
  for program in program_names:
    print("Making "+program+"\n")
    command = "make APPNAME="+program
    shell(command)
  print("Moving libraries to server"+"\n")
  try:
    shutil.rmtree("goldbach_server/src/goldbach/bin")
  except OSError as e:
    pass
  shell("mv bin goldbach_server/src/goldbach")
  os.chdir("goldbach_server/src")

def apiUpdater():
  api_port = str(Helpers.API_PORT)
  URL = "http://"+str(Helpers.SERVER_IP)+":"+api_port+"/update_cpu"
  while True:
    data = get_cpu_use()
    data = json.dumps(data)
    requests.post(URL, json = data)
    sleep(0.5)
  
def get_cpu_use():
  percents = psutil.cpu_percent(percpu=True, interval=1)
  use_percpu = []
  for value in percents:
      use_percpu.append(str(int(value)))    
  args = dict()
  args['ip'] = Helpers.getIP()
  args['cpu_use'] = use_percpu
  return args

if __name__ == "__main__":
  threading.Thread(target = apiUpdater, args=(),
        daemon = True).start()
  makeGoldbachCalculators()
  client = Worker()
  client.start()