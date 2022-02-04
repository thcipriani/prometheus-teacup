CONTRIBUTING TO TeaCuP
======================

To contribute a fix or change to TeaCuP you should include tests.

TESTS
-----

Requirements:

* `tox`
* The [BPF Compiler Colleciton](https://github.com/iovisor/bcc/blob/master/INSTALL.md) (BCC) for your distribution.

You must install `python-bpfcc` in addition to tox as bpfcc is not available
via pypi.

Tox will create a virtualenvironment and install the remaining test
requirements (`flake8`, `pytest` and `coverage`).

Running tests and linting via tox should be done by invoking tox on the command
line:

    $ tox
