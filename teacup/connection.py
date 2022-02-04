#!/usr/bin/env python3
"""
TeaCuP.Connection
=================

Someday we'll find it, the teacup connection, the lovers, the dreamers, and me
"""

import logging
import time

LOG = logging.getLogger('TeaCuP')


def ip_from_be32(ipaddr):
    """
    Translate __be32 ip to string
    """
    ip = []
    for i in range(0, 25, 8):
        ip.append((ipaddr >> i) & 0xff)
    return '.'.join(map(str, ip))


class Connection(object):
    """
    Object that holds connection details
    """
    def __init__(self, src, sport, dst, dport, timestamp):
        self.src = src
        self.dst = dst
        self.sport = sport
        self.dport = dport
        self.timestamp = timestamp


def new_connection(event):
    """
    make a connection from an event
    """
    src = ip_from_be32(event.src)
    dst = ip_from_be32(event.dst)
    return Connection(
       src,
       event.sport,
       dst,
       event.dport,
       time.time()
    )


class ConnectionTracker(object):
    MINUTE = 60.0

    def __init__(self, counter, portscan_handler, threshold):
        self.counter = counter
        self.connections = {}
        self.portscan_handler = portscan_handler
        self.threshold = threshold

    def on_connection(self, event):
        """
        Handle new connection events
        """
        self.counter.inc()
        connection = new_connection(event)
        self.connections\
            .setdefault(connection.src, {})\
            .setdefault(connection.dst, [])\
            .append(connection)
        self.log(self.log_connection_fmt(connection))
        self.check_portscan(connection.src)

    def log(self, line):
        """
        Log output
        """
        LOG.info(line)

    def check_portscan(self, src):
        """
        if there are > self.threshold connections from the same src to
        the same destination within the portscan time threshold the alert

        TODO: either make this more testable or mock / stub handler/log
        """
        time_threshold = time.time() - self.MINUTE
        for k, connections in self.connections[src].items():
            conns = set([
                (src, k, conn.dport)
                for conn
                in connections
                if conn.timestamp > time_threshold
            ])
            if len(conns) > self.threshold:
                self.log(self.log_portscan_fmt(conns))
                self.portscan_handler(src)

    @staticmethod
    def log_connection_fmt(conn):
        """
        Format logline
        """
        return (
            f'New Connection: '
            f'{conn.src}:{conn.sport} -> '
            f'{conn.dst}:{conn.dport}'
        )

    @staticmethod
    def log_portscan_fmt(conns):
        """
        Format portscan log
        """
        conns = list(conns)
        src = conns[0][0]
        dst = conns[0][1]
        ports = ','.join(map(str, sorted([x[2] for x in conns])))
        return f'Port scan detected: {src} -> {dst} on ports {ports}'
