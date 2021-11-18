#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <error.h>

int main(int argc, char **argv)
{
    int port = atoi(argv[2]);
    char *addr = argv[1]; //地址

    int serverfd;
    struct sockaddr_in server_addr;
    char send_msg[1024]; //发送信息
    char recv_msg[1024]; //接受信息

    /* 创建socket */
    serverfd = socket(AF_INET, SOCK_STREAM, 0);

    /* 指定服务器 */
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = inet_addr(addr);
    memset(server_addr.sin_zero, 0, sizeof(server_addr.sin_zero)); //零填充

    /* 连接服务器 */
    if(connect(serverfd, (struct sockaddr *)&server_addr, sizeof(server_addr))<0)
    {
        perror("connect");
        return -1;
    }

    while (1)
    {
        memset(recv_msg, 0, sizeof(recv_msg));
        printf("SendMsg: ");
        scanf("%s", send_msg);
        if (strcmp(send_msg, "exit") == 0){
            close(serverfd);
            break;
        }
            
        printf("Sending: %s\n", send_msg);
        if(send(serverfd, send_msg, strlen(send_msg), 0) <0){
            perror("send");
            return -1;
        };

        recv(serverfd, recv_msg, sizeof(recv_msg), 0);
        printf("Received: %s\n", recv_msg);
    }
    
    return 0;
}