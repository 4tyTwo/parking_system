PYTHON := $(shell which python3 2>/dev/null || which ./rebar3)

all: start_server

start_server:
	$(PYTHON) parkingServer.py
