README for TeaCuP
=================

TeaCuP is an express data path (XDP) eBPF program and service that monitors for
new TCP connections, exposes a count of those connections via prometheus, and
blocks portscans via iptables.

By default, the prometheus endpoint will run on http://0.0.0.0:8000.

USAGE
-----

	usage: teacup [-h] [-v] [-t THRESHOLD] [-i <DEVICE>] [-p--prometheus-port <PORT>]

	Prometheus exporter showing new TCP connections via a BPF logger running in the eXpress Data Path

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --verbose         Show DEBUG output
	  -t THRESHOLD, --threshold THRESHOLD
							Number of connections per minute before blocking IPs (default: 3)
	  -i <DEVICE>, --iface <DEVICE>
							Interface to attach XDP TCP listener (default: lo)
	  -p--prometheus-port <PORT>
							Listening port for prometheus connections (default: 8000)

☠️🐉 Here Be Dragons❣️ 🐉☠️
-------------------------

**No one should use this for anything important**.

I've done limited testing on Debian Bullseye and Bookworm — mostly using a few
ephemeral [Linode](https://www.linode.com/) instances (😻 Linode).

INSTALL
-------

First, install the requirements:

* Linux header files
* Iptables
* Python3
* Pip
* And the [BPF Compiler Colleciton](https://github.com/iovisor/bcc/blob/master/INSTALL.md) (BCC) for your distribution.

On Debian, this looks like

```
sudo apt update
sudo apt install \
    iptables \
    python3-pip \
    bpfcc-tools \
    python3-bpfcc \
    libbpfcc \
    libbpfcc-dev \
    linux-headers-$(uname -r)
```

Then install TeaCuP via pip:

```
$ git clone https://github.com/thcipriani/prometheus-teacup.git
$ cd prometheus-teacup
$ sudo pip3 install -e .
```

Docker
------

The docker image doesn't have header files as it's meant to share the header
files of the host machine. You need to install linux header files for your
distribution.

On Debian, this looks like

```
sudo apt-get install linux-headers-$(uname -r)
```

To build and run the docker image run:

    make

Running the tool in the docker image requires sharing directories containing
linux header files and shared objects for BPF.

You may need to adjust the docker base image if BPF compilation fails.

If your goal is to monitor traffic on the docker host, use the host network
namespace via the docker `--net=host` param.

Using the command

    make

Will monitor the `lo` interface of your localhost.

Use `IFACE=` to change the iface:

    IFACE=eth0 make

Tests
-----

See [CONTRIBUTING.md](CONTRIBUTING.md)
