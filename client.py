import socket
import threading
from datetime import datetime

def recv(conn):
    while True:
        data = conn.recv(200).decode('utf8')
        if len(data) == 0: # close from server
            print("Server closed")
            conn.close()
            return
        now = datetime.now()
        print("%s %s" % (now.strftime("%H:%M"), data))

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.connect(("127.0.0.1", 7777))
recvThread = threading.Thread(target=recv, args = (mySocket,))
recvThread.daemon = True
recvThread.start()

while True:
    data = input()
    if data == "":
        continue
    mySocket.send(data.encode('utf8'))
