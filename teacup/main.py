#!/usr/bin/env python3
"""
TeaCuP
======

Main loop for TeaCuP CLI.
"""
import logging
import signal
import sys

from prometheus_client import Counter

from .args import parse_args
from .bpf import XDPTCPConnections
from .connection import ConnectionTracker
from .iptables import IPTables
from .prometheus import PrometheusExporter

LOG = logging.getLogger('TeaCuP')
THREADS = []


def setup_logging(debug=False):
    """
    Setup logging
    """
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(
        stream=sys.stderr,
        level=level,
        format=('%(asctime)s: %(message)s'),
        force=True  # re-do all root handlers
    )


def exit():
    """
    Graceful exit
    """
    global THREADS
    for thread in THREADS:
        thread.stop()
    sys.exit(0)


def main(argv=None):
    """
    Main program entrypoint
    """
    global THREADS
    args = parse_args(argv)
    setup_logging(args.debug)

    prometheus_counter = Counter(
        'tcp_connection_count',
        'Count the number of TCP connections'
    )

    iptables = IPTables(args.iface)

    conn_tracker = ConnectionTracker(
        counter=prometheus_counter,
        portscan_handler=iptables.block,
        threshold=args.threshold
    )

    xdp = XDPTCPConnections(
        args.iface,
        on_connection=conn_tracker.on_connection
    )

    pe = PrometheusExporter(
        args.prometheus_port
    )

    THREADS.append(xdp)
    THREADS.append(pe)

    for thread in THREADS:
        thread.start()

    # Deinit iptables / Remove lingering chains
    THREADS.append(iptables)

    signal.signal(signal.SIGUSR1, exit)
    signal.signal(signal.SIGTERM, exit)
    while True:
        try:
            signal.pause()
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    main()
