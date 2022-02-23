# Server info
SERVER_IP = '192.168.1.115'
WELCOME_PORT = 5000
PACKAGE_SIZE = 1024

# len(message) < PACKAGE_SIZE
# Send data to web client or worker
def sendWebMessage(message, connection):
    message = message.encode("utf_8")
    connection.sendall(message)

def recvWebMessage(connection):
    message = connection.recv(PACKAGE_SIZE)
    message = message.decode("utf-8")
    return message

# Fills the message with trash to avoid message concatenation
def fill_with_trash(message):
    for index in range(PACKAGE_SIZE-len(message)):
        message += '$'
    return message

# len(message) > PACKAGE_SIZE
# Send big messages, usually in n parts
def sendWorkerMessage(connection, message):
    message = fill_with_trash(message)
    sendWebMessage(message, connection)
    sendWebMessage("end", connection)

# Receives packages from the worker until it receive the (end) word
def recvWorkerMessage(connection):
    buffer = ""
    message = ""
    while True:
      message = connection.recv(PACKAGE_SIZE)
      message = message.decode("utf-8")
      message = message.replace('$','')
      if "end" in message:
        message = message.replace('end','')
        buffer += message
        break
      else:
        buffer += message
    return buffer

# Add 200 OK status and load html page 
# Return html loaded in a string
def loadHTML(name):
    header = "HTTP/1.1 200 OK\n    <label for=\"number\">Number</label>\n"
    header += "Content-Type: text/html\n\n"
    html = header

    file = open("html/"+str(name)+".html", "r")
    for line in file:
      html += line
    
    return html
