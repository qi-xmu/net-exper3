all: build


build:
	cd re-echo && make
	@echo build finished

.PHONY:server, client
server: 
	cd re-echo && make run_ser

client:
	cd re-echo && make run_cli

.PHONY:start, join

start:
	cd ter-msg && ./msg-ser.py
join:
	cd ter-msg && ./msg-cli.py