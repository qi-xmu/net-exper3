all: build


build:
	cd re-echo && make
	@echo build finished

.PHONY:server, client
server: 
	cd re-echo && make run_ser

client:
	cd re-echo && make run_cli