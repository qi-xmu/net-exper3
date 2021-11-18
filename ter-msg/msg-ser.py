#!/usr/bin/python3
import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 7788

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))
s.listen(5) # 最多五个用户同时在线

client_list = []

def recv_msg(c, addr, name):
    while True:
        msg = c.recv(1024)
        # 错误捕获
        if(len(msg) == 0):
            c.close()
            break
        msg = msg.decode('utf-8')

        if msg == "exit":
            c.send("exit".encode('utf-8'))
            c.close()
            break
        print(msg)
        # 将消息广播给其他主机
        for client in client_list:
            if client == c:
                continue
            client.send(msg.replace(">>", "<<").encode('utf-8'))
        
    print(f"{name}退出了聊天室，IP地址为{addr}")
    client_list.remove(c)  # 删除断开连接的客户端
    # 用户退出信息广播
    for client in client_list:
        client.send(f"{name}退出了聊天室，IP地址为{addr}".encode('utf-8'))
    return


while True:
    c, addr = s.accept()
    c.send('欢迎来到聊天室！\n'.encode('utf-8'))
    client_list.append(c)
    name = c.recv(1024).decode("utf-8")
    print(f"{name}进入了聊天室，IP地址为{addr}")
    # 对于每一个新用户开辟一个新的线程监听消息
    Thread(target=recv_msg, args=(c, addr, name)).start()
