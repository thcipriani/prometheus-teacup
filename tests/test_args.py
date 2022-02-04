#!/usr/bin/env python3
"""
TeaCuP.args Tests
=================

Tests for TeaCuP
"""

import pytest

import teacup.args


def test_parse_args():
    args = teacup.args.parse_args(['-v'])
    assert args.debug


if __name__ == '__main__':
    pytest.main()
