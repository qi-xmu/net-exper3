#!/usr/bin/python3
import socket
import atexit

client_list = []
name_list = []
port = 8899

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 断开后防止端口被占用

s.bind(("0.0.0.0", port))
print(f"Port: {port}")

@atexit.register # 注册退出函数
def leave():
    print("shutdown")
    for cli in client_list:
        s.sendto("shutdown".encode(), cli)

while True:
    # 第一次传输名字
    msg, c = s.recvfrom(1024)
    print(f"{c} : {msg.decode()}")
    # 新用户
    if c not in client_list:
        # 验证名字不重复
        name = msg.decode()
        if name in name_list:
            s.sendto("e:名字重复。".encode(), c)
        else:
        # 验证成功
            s.sendto(f"欢迎{msg.decode()}！在线人数: {len(client_list)}".encode(), c) # 新用户欢迎语句
            for cli in client_list:
                s.sendto(f"[Server]: {name}进入聊天室。".encode(), cli)
            client_list.append(c)
            name_list.append(name)
            print(f"- 在线人数: {len(client_list)}")  # 服务端打印人数
    # 老用户
    else:
        # 退出
        if msg.decode() == "exit":
            s.sendto("exit".encode(), c)
            client_list.remove(c)
            name_list.remove(name)
            for cli in client_list:
                s.sendto(f"[Server]: {c}退出聊天室。".encode(), cli)
            continue
        # 广播
        for cli in client_list:
            if cli == c:
                continue
            s.sendto(msg, cli)
