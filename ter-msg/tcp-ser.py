#!/usr/bin/python3
import socket
from threading import Thread
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 7788

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 断开后防止端口被占用
s.bind((host, port))
s.listen(5) # 最多五个用户同时在线

client_list = []

def recv_msg(c, addr, name):
    while True:
        msg = c.recv(1024).decode('utf-8') # 解码
        # 错误捕获
        if(len(msg) == 0):
            break
        # 退出指令 需要三次询问，帮助客户端 关闭发送 --> 关闭接收
        if msg == "exit":
            c.send("exit".encode('utf-8'))
            break

        print(time.strftime("[%m-%d %H:%M:%S] "),msg) # 服务端终端打印
        # 将消息广播给其他主机
        for client in client_list:
            if client == c:
                continue
            client.send(msg.encode('utf-8'))
    c.close()
    print(f"{name}退出了聊天室，IP地址为{addr}")
    client_list.remove(c)  # 删除断开连接的客户端
    # 用户退出信息广播
    time.sleep(0.5)
    for client in client_list:
        client.send(f"[Server]: {name}退出了聊天室，IP地址为{addr[0]}".encode('utf-8'))
    return


while True:
    c, addr = s.accept()
    c.send(f'欢迎来到聊天室！当前在线人数：{len(client_list)}\n'.encode('utf-8'))
     
    name = c.recv(1024).decode("utf-8")
    print(f"{name}进入了聊天室，地址为{addr}")
    # 广播给所有人
    for client in client_list:
        client.send(f"[Server]: {name}进入了聊天室，IP地址为{addr[0]}".encode('utf-8'))

    client_list.append(c) # 添加到列表
    # 进入聊天室    
    # 对于每一个新用户开辟一个新的线程监听消息
    try:
        Thread(target=recv_msg, args=(c, addr, name)).start()
    except:
        print("exit")