#!/usr/bin/env python3
"""
teacup.args
==========

Handles everything to do with argparse
"""

import argparse


def parse_args(argv):
    """
    Parse main program args
    """
    parser = argparse.ArgumentParser(
        description=('Prometheus exporter showing new TCP connections '
                     'via a BPF logger running in the eXpress Data Path')
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='Show DEBUG output',
        action='store_true',
        dest='debug'
    )
    parser.add_argument(
        '-t',
        '--threshold',
        help=(
            'Number of connections per minute before blocking IPs '
            '(default: 3)'
        ),
        default=3
    )
    parser.add_argument(
        '-i',
        '--iface',
        help='Interface to attach XDP TCP listener (default: lo)',
        metavar='<DEVICE>',
        default='lo'
    )
    parser.add_argument(
        '-p'
        '--prometheus-port',
        help='Listening port for prometheus connections (default: 8000)',
        metavar='<PORT>',
        default=8000,
        dest='prometheus_port'
    )

    return parser.parse_args(argv)
