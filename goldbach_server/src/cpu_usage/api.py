import json
import threading
from time import sleep
from urllib import response
from flask import Flask,Response,request
import helpers as Helpers

# Thread safe Dict, only one thread can use it
class Dict():
  def __init__(self):
    self.memory= dict()
    self.can_use = threading.Lock()
  
  def update(self, ip, status):
    self.can_use.acquire()
    # data = [{'x':0, 'y':ip, 'value':status}, {'x':1, 'y':ip, 'value':status},{'x':2, 'y':ip, 'value':status}]
    data = [{'x':0, 'y':ip, 'value':status}]
    
    self.memory = data
    print("\n\nupdate "+str(self.memory)+"\n\n")
    self.can_use.release()
  
  def get(self):
    self.can_use.acquire()
    memory = self.memory.copy()
    print("\nget "+str(self.memory))
    self.can_use.release()
    return memory

storage = Dict()
app = Flask(__name__)

# Send current storage status to client
@app.route('/cpu_status', methods=['GET'])
def handle_get_cpu():
    memory = storage.get()
    cpu_status = json.dumps(memory)
    respuesta = Response(cpu_status)
    respuesta.headers["Access-Control-Allow-Origin"] = "*"
    sleep(1)
    return respuesta

# Update storage with arrived data
@app.route('/update_cpu', methods=['POST'])
def handle_update_cpu():
    data = request.get_json()
    data = json.loads(data)
    ip = data["ip"]
    cpu_usage = data["data"]
    storage.update(ip, cpu_usage)
    return Response("ok")

@app.get('/open_cpu_api')
def handle_open_cpu():
    page = Helpers.loadHTML("cpu_usage")
    page = Response(page)
    return page

def start():
  app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
  threading.Thread(target = start, args=(),
    daemon = True).start() 
