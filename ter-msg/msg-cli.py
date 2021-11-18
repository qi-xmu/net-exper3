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

print(sys.argv)
if len(sys.argv) ==1:
    name = "anony"
else:
    name = sys.argv[1]
s.send(name.encode("utf-8"))

def send_mode():
    while True:
        msg = input(name + ">> ")
        if msg == "exit":
            s.send(msg.encode("utf-8"))
            break

        msg = name + ">> " + msg
        s.send(msg.encode("utf-8"))
        
    print("End msg send")

    return

def listen_recv():
    while True:
        recv_msg = s.recv(1024)
        if(recv_msg.decode("utf-8") == "exit"):
            break
        print("\r" + recv_msg.decode("utf-8"), end='')
        print("\n"+name + ">> ", end="")
    print("End msg recv")
     

try:
    Thread(target=listen_recv, args=()).start()
    # t2 = Thread(target=send_msg, args=())

    send_mode()
    
except Exception as e:
    print("Error: Thread", e)

s.close()

