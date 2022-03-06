const sio = io();

sio.on('connect', () => {
  console.log('connected');
  sio.emit('get_cpu_status', {numbers: [1, 2]});
});

sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('cpu_status', (data) => {
  document.getElementById("cpu_values").innerHTML = JSON.stringify(data);
});