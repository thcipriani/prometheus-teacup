SHELL=/bin/bash
IFACE ?= lo

TCP_C_PY = $(abspath ./teacup/newtcpc.py)
TCP_C_PY_SRC = $(abspath ./xdp_tcp_count.c)
TCP_C_PY_FN = 'xdp_new_tcp_count'

.PHONY: clean build run test
run: build
	# /lib/modules + /usr/src needed for eBPF compilation
	sudo docker run --rm -it --net=host --privileged \
		-v /lib/modules:/lib/modules:ro \
		-v /usr/src:/usr/src:ro \
		teacup \
		--iface $(IFACE)

test: $(TCP_C_PY)
	tox

clean:
	rmdir .build
	sudo docker rmi teacup

build: .build

.build: $(TCP_C_PY)
	sudo docker build -t teacup -f Dockerfile .
	mkdir -p .build

$(TCP_C_PY): $(TCP_C_PY_SRC)
	printf '# == Generated via Makefile == #\n' > "$@"
	printf "FN = $(TCP_C_PY_FN)\n" >> "$@"
	printf "XDP_COUNT_NEW_TCP = r'''\n" >> "$@"
	cat "$<" >> "$@"
	printf "'''\n" >> "$@"
