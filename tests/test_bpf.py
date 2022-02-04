#!/usr/bin/env python3
"""
TeaCuP.bpf Tests
================

This is a harder class to unit test as it's interacting with the system
"""

import pytest

import teacup.bpf

class EventStub(object):
    def __init__(self):
        self.foo = 'foo'

    def event(self, data):
        return self.foo + data

def test_init():
    """
    Make sure the object is initialized correctly
    """
    events = []
    xdp = teacup.bpf.XDPTCPConnections(
        device='eth0',
        on_connection=lambda x: events.append(x)
    )
    assert xdp.b == None
    xdp.b = {'buffer': EventStub()}
    xdp.callback(1,'FOO',3)
    assert events[0] == 'fooFOO'

if __name__ == '__main__':
    pytest.main()
