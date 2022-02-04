"""
teacup.prometheus
=================

Anything related to the prometheus client in teacup
"""
import logging

from prometheus_client import start_http_server

LOG = logging.getLogger('TeaCuP')


class PrometheusExporter(object):
    """
    Prometheus client abstraction
    """
    def __init__(self, port):
        """
        Initialize prometheus client class
        """
        self.port = port

    def start(self):
        start_http_server(self.port)
        LOG.info(f'Prometheus client active on :{self.port}')

    def stop(self):
        pass
