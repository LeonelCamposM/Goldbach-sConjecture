import json
import threading
from time import sleep
from flask import Flask,Response,request
from waitress import serve
import helpers as Helpers
import logging


# Thread safe Dict, only one thread can use it
class Dict():
  def __init__(self):
    self.memory= dict()
    self.can_use = threading.Lock()
  
  def update(self, ip, status_array):
    self.can_use.acquire()
    self.memory[ip] = status_array
    self.can_use.release()
  
  def get(self):
    self.can_use.acquire()
    memory = self.memory.copy()
    memory = self.formatDataObject(memory)
    self.can_use.release()
    return memory
  
  def formatDataObject(self, memory):
    cpu_reports = []
    for key in memory:
      data = {'ip':key, 'value':memory[key]}
      cpu_reports.append(data)
    cpu_reports = json.dumps(cpu_reports)
    return cpu_reports

storage = Dict()
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

# Send current storage status to client
@app.get('/cpu_status')
def handle_cpu_status():
    memory = storage.get()
    response = Response(memory)
    response.headers["Access-Control-Allow-Origin"] = "*"
    sleep(0.5)
    return response

# Update storage with arrived data
@app.route('/update_cpu', methods=['POST'])
def handle_update_cpu():
    data = request.get_json()
    data = json.loads(data)
    ip = data["ip"]
    cpu_usage = data["cpu_use"]
    storage.update(ip, cpu_usage)
    return Response("OK")

@app.get('/open_cpu_api')
def handle_open_cpu_api():
  page = Helpers.loadWebPage("cpu_usage", False)
  page = Response(page)
  return page
 
def start():
  serve(app, host=Helpers.SERVER_IP, port=Helpers.API_PORT)
