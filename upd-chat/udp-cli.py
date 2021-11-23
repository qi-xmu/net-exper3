#!/usr/bin/python3
import socket
from threading import Thread
import sys

if len(sys.argv) < 2:
    print("Usage: ./udp-cli.py [name]")
    exit(1)

name = sys.argv[1]
ip = "127.0.0.1"
port = 8899
server = (ip, port)
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

c.sendto(name.encode(),server) # 发送姓名
msg = c.recvfrom(1024)[0].decode() # 接受进入信息
# 名字重复，返回错误
if msg[0]  == 'e':
    print("- Error " + msg.split(':')[1])
    exit(1)
print(msg) # 接收欢迎信息

# 创建监听函数
def listen_recv():
    while True:
        recv_msg = c.recvfrom(1024)[0].decode()
        if recv_msg == "shutdown":
            print("- Error " +"服务器关闭。")
            exit(0)
        if(recv_msg == "exit"):
            break
        print(f"\r{recv_msg}",end='') # 接收的信息
        print("\n[{:^4}]: ".format(name), end='') # 发送框
    return

# 发送模式
def send_mode(recvor=server):
    while True:
        msg = input("[{:^4}]: ".format(name))
        if msg == "exit":
            c.sendto(msg.encode("utf-8"), server)
            break
        msg = "[{:^4}]: {:<20}".format(name,msg)
        c.sendto(msg.encode("utf-8"), recvor)
try:
    Thread(target=listen_recv, args=()).start() # 创建监听线程
    send_mode() # 主线程进入发送模式
except:
    print("exit")
