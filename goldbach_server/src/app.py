import socketio
import psutil
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': './html/'
})

@sio.event
def connect(sid, environ):
    print(sid, 'connected')

@sio.event
def disconnect(sid):
    print(sid, 'disconnected')

@sio.event
def get_cpu_status(sid, data):
    while True:
        percents = psutil.cpu_percent(percpu=True, interval=1)
        use_percpu = []
        for value in percents:
            use_percpu.append(value)    
        print("CPU Usage = " + str(use_percpu))
        print("\n\n") 
        cpu_status = json.dumps(use_percpu)
        sio.emit('cpu_status', {'status': cpu_status}, to=sid)
