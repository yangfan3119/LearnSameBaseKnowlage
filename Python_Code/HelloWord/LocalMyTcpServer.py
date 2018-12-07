import socket


sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
addr = ('127.0.0.1',7878)
sk.bind(addr)
sk.listen(5)
try:
    while True:
        conn,addrip = sk.accept()
        print('Connect By:',addrip)
        while True:
            ts = conn.recv(1024)
            print(ts.decode())
        conn.close()
except:
    print("Error Stop!")