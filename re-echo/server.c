#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <error.h>
#include <stdlib.h>

/* 反转字符串函数 */
int reverse_str(char *str, int size)
{
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++)
    {
        char tmp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = tmp;
    }
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("Arg too less.\n");
        return 0;
    }
    int port = atoi(argv[1]); // port number
    printf("Port: %d\n", port);
    int serverfd, clientfd; // 服务端和客户端的fd
    struct sockaddr_in server_addr;

    /* sock_stream: TCP; sock_dgram: UDP */
    if ((serverfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket error");
        assert(0);
    }

    /* 指定参数 */
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    /* 允许所有主机连接 */
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY); // INADDR_ANY表示本机所有IP地址
    memset(&server_addr.sin_zero, 0, sizeof(server_addr.sin_zero));

    /* 绑定地址 */
    if (bind(serverfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0)
    {
        perror("bind failed");
        assert(0);
    }
    else
        printf("Bind Succeed.\n");
    /* 最大连接数 1 */
    if (listen(serverfd, 2) < 0)
        perror("Listen failed.\n");

    while (1)
    {
        /* 连接的主机信息 */
        if ((clientfd = accept(serverfd, NULL, NULL)) < 0)
        {
            perror("Accept failed.");
            assert(0);
        };
        /* 显示连接的主机 */
        printf("Accept: %d\n", clientfd);
        char recv_msg[1024];
        /* 客户机连接后进行交互，占用整个进程 */
        pid_t pid = 0;
        send(clientfd, &pid, sizeof(pid_t), 0);
        while (1)
        {
            /* 接受信息 */
            memset(recv_msg, 0, sizeof(recv_msg));
            printf("Start Receiving...\n");
            if (recv(clientfd, recv_msg, sizeof(recv_msg), 0) <= 0)
                break;

            /* 处理信息,接受信息反转信息 */
            printf("Received: %s\n", recv_msg);
            reverse_str(recv_msg, sizeof(recv_msg));
            /* 发送信息 */
            send(clientfd, recv_msg, strlen(recv_msg), 0);
        }
        perror("exit");
        close(clientfd);
    }
    close(serverfd);
    return 0;
}