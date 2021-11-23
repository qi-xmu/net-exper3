#!/usr/bin/python3
import socket
from threading import Thread
import sys
import time

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
port = 7788
s.connect((host, port))

if len(sys.argv) ==1:
    name = "Anony"
else:
    name = sys.argv[1]
s.send(name.encode("utf-8"))
print("\r" + s.recv(1024).decode("utf-8"))

def send_mode():
    while True:
        msg = input("[{:^4}]: ".format(name))
        if msg == "exit":
            s.send(msg.encode("utf-8"))
            break
        msg = "[{:^4}]: {:<20}".format(name,msg)
        # print(msg, end='')
        s.send(msg.encode("utf-8"))


def listen_recv():
    while True:
        recv_msg = s.recv(1024).decode("utf-8")
        if(recv_msg == "exit"):
            break
        print(f"\r{recv_msg}",end='')
        print("\n[{:^4}]: ".format(name), end='')
    return
     
try:
    Thread(target=listen_recv, args=()).start()
    send_mode()
except Exception as e:
    print("Error: Thread", e)

s.close()

