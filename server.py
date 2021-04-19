import socket
import threading
import time

connPool = []

def recv(conn):
    while True:
        try:
            data = conn.recv(200)
            if len(data) == 0:
                connPool.remove(conn)
                conn.close()
                for c in connPool:
                    c.send(("Current users : %d" % len(connPool)).encode('utf8'))
                return
        except:
            connPool.remove(conn)
            conn.close()
            for c in connPool:
                c.send(("Current users : %d" % len(connPool)).encode('utf8'))
            return
            
        message = "%s : %s" % (conn.getpeername()[1], data.decode('utf8'))
        print(message)
        for c in connPool:
            if c.getpeername() == conn.getpeername():
                continue
            c.send(message.encode('utf8'))


def accept(mySocket):
    while True:
        conn, addr = mySocket.accept()
        print("connected by : ", addr)
        connPool.append(conn)
        recvThread = threading.Thread(target=recv, args=(conn,))
        recvThread.daemon = True
        recvThread.start()

        for c in connPool:
            c.send(("Current users : %d" % len(connPool)).encode('utf8'))


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(("127.0.0.1", 7777))
mySocket.listen(2)
acceptThread = threading.Thread(target=accept, args=(mySocket,))
acceptThread.daemon = True
acceptThread.start()

while True:
    time.sleep(1)
