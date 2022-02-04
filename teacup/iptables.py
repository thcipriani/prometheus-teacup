"""
teacup.iptables
===============

Handle iptables in teacup
"""
import logging

# TODO: Find a non iptables-legacy library (possibly python-nftables)
import iptc

LOG = logging.getLogger('TeaCuP')


class IPTables(object):
    CHAIN = 'TeaCup'

    def __init__(self, interface):
        """
        Initialize IPTabels
        """
        self._setup_chains()
        self.chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), self.CHAIN)
        self.interface = interface
        self.blocked = {}

    def _setup_chains(self):
        """
        Create a new chain, add a jump rule to the existing INPUT chain
        """
        self.stop(startup=True)
        iptc.easy.add_chain('filter', self.CHAIN)
        iptc.easy.add_rule('filter', 'INPUT', {'target': self.CHAIN})

    def block(self, src):
        """
        block: Add a new iptables rule to drop new tcp packets from src
        """
        if self.blocked.get(src) is not None:
            LOG.debug(f'{src} already blocked')
            return

        self.chain.insert_rule(self._make_block_rule(src))
        LOG.info(f'Blocked: {src}')
        self.blocked[src] = True

    def stop(self, startup=False):
        """
        Remove the TeaCuP chain

        If you're shutting down, log some info about what's no longer being
        blocked.
        """
        if not startup:
            self._dump_chain()

        try:
            iptc.easy.delete_rule(
                'filter', 'INPUT', {'target': self.CHAIN})
            iptc.easy.delete_chain('filter', self.CHAIN, flush=True)
            # TODO: upstream ValueError -> custom error type?
        except ValueError:
            if startup:
                return
            raise

    def _dump_chain(self):
        """
        Dump Chain Info
        """
        msg = [f'\n\tRemoving iptables chain: {self.CHAIN}']
        blocked = [
            rule['src'] for rule in
            iptc.easy.dump_chain('filter', self.CHAIN)
        ]
        if len(blocked):
            msg.append(
                '\t\tUnblocking: {}'.format(
                   ','.join(blocked)
                )
            )
        LOG.info('\n'.join(msg))

    def _make_block_rule(self, src):
        """
        Create a block rule
        """
        rule = iptc.Rule()
        target = iptc.Target(rule, 'DROP')

        rule.protocol = 'tcp'
        rule.in_interface = self.interface
        rule.src = src
        rule.target = target
        return rule
