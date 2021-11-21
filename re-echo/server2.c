#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#include <stdlib.h>
#include <arpa/inet.h>
#include <error.h>
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
    if (argc != 2)
    {
        printf("Usage: server2 [Port]\n");
        return 0;
    }
    int port = atoi(argv[1]); // port number
    printf("Port: %d\n", port);
    int serverfd, clientfd; // 服务端和客户端的fd
    struct sockaddr_in server_addr, client_addr;
    memset(&client_addr, 0, sizeof(client_addr));

    /* sock_stream: TCP; sock_dgram: UDP */
    if ((serverfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket");
        return -1;
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
        perror("Bind");
        return -1;
    }
    /* 最大连接数 1 */
    if (listen(serverfd, 5) < 0)
    {
        perror("Listen");
        return -1;
    }
    int num = 0;

    //监听连接的主机
    while (1)
    {
        /* 连接的主机信息 */
        int len = sizeof(client_addr);
        if ((clientfd = accept(serverfd, (struct sockaddr *)&client_addr, &len)) < 0)
        {
            perror("Accept failed.");
            return -1;
        };

        /* 显示连接的主机 显示IP */
        uint32_t cli_addr = client_addr.sin_addr.s_addr;
        uint8_t *pa = &cli_addr;
        uint16_t cli_port = ntohs(client_addr.sin_port);
        printf("- Accept: %d.%d.%d.%d:%d\n", pa[0], pa[1], pa[2], pa[3], cli_port);
        
        /* 创建子进程 */
        pid_t pid;
        if ((pid = fork()) < 0)
        { /* 创建失败 */
            perror("Fork");
        }
        else if (pid == 0)
        { /* 子进程 */
            char recv_msg[1024];
            while (1)
            {
                /* 接受信息 */
                memset(recv_msg, 0, sizeof(recv_msg));
                if (recv(clientfd, recv_msg, sizeof(recv_msg), 0) <= 0)
                    break;
                /* 处理信息,接受信息反转信息 */
                printf("> Received: %s\n", recv_msg);
                reverse_str(recv_msg, sizeof(recv_msg));
                /* 发送信息 */
                send(clientfd, recv_msg, strlen(recv_msg), 0);
                sleep(0.5);
            }
            close(clientfd);
            printf("- Exit %d.%d.%d.%d:%d\n", pa[0], pa[1], pa[2], pa[3], cli_port);
            return 0;
        }
        else
        { /* 父进程 */
            printf("- No.%d PID: %d\n", ++num, pid);
            send(clientfd, &pid, sizeof(pid_t), 0);
            sleep(1);
        }
    }
    close(serverfd);
    return 0;
}