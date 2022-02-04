#!/usr/bin/env python3
"""
TeaCuP.iptables Tests
=====================
"""

import mock
import pytest

import teacup.iptables


# This many mocks makes me worry about whether I'm testing anything...
@mock.patch('teacup.iptables.iptc.easy')
@mock.patch('teacup.iptables.iptc.Chain')
@mock.patch('teacup.iptables.iptc.Table')
def test_make_block_rule(mock_iptc_easy, mock_iptc_Chain, mock_iptc_Table):
    """
    Make sure the block rule looks ok
    """
    src = '172.16.254.254/255.255.255.255'
    iface = 'eth0'
    ipt = teacup.iptables.IPTables(iface)
    rule = ipt._make_block_rule(src=src)
    assert rule.src == src
    assert rule.in_interface == iface

if __name__ == '__main__':
    pytest.main()
