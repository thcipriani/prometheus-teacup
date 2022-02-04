#!/usr/bin/env python3
"""
TeaCuP.ConnectionTracker tests
==============================

Tests for teacup.connectiontracker
"""
import pytest

import teacup.connection


class EventStub(object):
    def __init__(self, src, sport, dst, dport):
        self.src = src
        self.sport = sport
        self.dst = dst
        self.dport = dport


def test_log_connection_fmt():
    assert teacup.connection.ConnectionTracker.log_connection_fmt(
        teacup.connection.new_connection(
            EventStub(0xE90D10AC, 10, 0xE90D10AC, 10)
        )
    ) == 'New Connection: 172.16.13.233:10 -> 172.16.13.233:10'


def test_log_port_scan():
    assert teacup.connection.ConnectionTracker.log_portscan_fmt(
        set([('1', '2', 3), ('1', '2', 4), ('1', '2', 5), ('1', '2', 6)])
    ) == 'Port scan detected: 1 -> 2 on ports 3,4,5,6'


if __name__ == '__main__':
    pytest.main()
