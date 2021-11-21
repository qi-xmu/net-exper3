ROOT = .
CC = gcc
C_FLAG = -w

all:client server server2

client: client.c
	$(CC) -o $@ $(C_FLAG)  $<

server: server.c
	$(CC) -o $@ $(C_FLAG)  $<

server2: server2.c
	$(CC) -o $@ $(C_FLAG)  $<

clean: 
	rm -f client server *.o


.PHONY: run_ser, run_cli, run_ser2
run_ser: server
	./server 12345
run_ser2: server2
	./server2 12345
run_cli: client
	./client 127.0.0.1 12345