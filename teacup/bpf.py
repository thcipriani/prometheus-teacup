#!/usr/bin/env python3
"""
teacup.bpf
==========

Handles everything to do with BPF/XDP
"""

import logging
import threading
import time

from bcc import BPF

from .newtcpc import XDP_COUNT_NEW_TCP, FN

LOG = logging.getLogger('TeaCuP')


class XDPTCPConnections(object):
    """
    XDPTCPConnections

    Compile src_file to BPF bytecode, inject into XDP, and monitor output
    """
    def __init__(self, device, on_connection):
        self.b = None
        self.device = device
        self._running = False
        self.thread = threading.Thread(target=self.run)

        def callback(ctx, data, size):
            event = self.b['buffer'].event(data)
            on_connection(event)

        self.callback = callback

    def _compile(self):
        LOG.debug('Compiling BPF')
        # Added -Wno-macro-redefined due to
        # <https://github.com/iovisor/bcc/pull/3391>
        self.b = BPF(
            text=XDP_COUNT_NEW_TCP,
            cflags=['-Wno-macro-redefined']
        )

    def _attach(self):
        LOG.debug('Attaching function to XDP')
        fn = self.b.load_func(FN, BPF.XDP)

        self.b.attach_xdp(self.device, fn, 0)
        self.b['buffer'].open_ring_buffer(self.callback)

    def start(self):
        self._running = True
        self._compile()
        self._attach()
        self.thread.start()
        LOG.info(
            f'Listening for new connections on {self.device}. '
            'Ctrl+C to stop.'
        )

    def run(self):
        while self._running:
            try:
                self.b.ring_buffer_consume()
                time.sleep(0.1)
            except ValueError:
                continue

    def stop(self):
        self._running = False
        self.thread.join()
        self.b.remove_xdp(self.device, 0)
