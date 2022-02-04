#!/usr/bin/env python3
"""
TeaCuP.main Tests
=================

Tests for TeaCuP
"""

import logging
import pytest

import teacup.main

class ThreadStub(object):
    def __init__(self):
        self.started = True
    def stop(self):
        self.started = False

def test_setup_logging():
    """
    Make sure logging setup works
    """
    teacup.main.setup_logging(debug=True)
    assert logging.getLogger().level == logging.DEBUG

def test_exit():
    """
    Ensure exit stops threads and exits
    """
    ts = ThreadStub()
    teacup.main.THREADS.append(ts)
    with pytest.raises(SystemExit) as e:
        teacup.main.exit()
    assert e.type == SystemExit
    assert ts.started is False


if __name__ == '__main__':
    pytest.main()
