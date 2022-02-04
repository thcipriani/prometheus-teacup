#!/usr/bin/env python3
"""
TeaCuP
======

Package Configuration
"""

from setuptools import find_packages, setup

install_requires = [
    'prometheus_client',
    'python-iptables',
]

tests_require = [
    'coverage',
    'pytest',
]

setup(
    name='teacup',
    maintainer='Tyler Cipriani',
    maintainer_email='tyler@tylercipriani.com',
    description=('prometheus exporter showing new tcp connections via a BPF '
                 'logger running in the express data path (XDP)'),
    url='https://github.com/thcipriani/teacup',
    license='GPLv3+',
    packages=find_packages(exclude=['tests.*']),
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Monitoring',
    ],
    keywords=['tcp', 'xdp', 'bpf', 'prometheus'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'teacup = teacup.main:main',
        ],
    },
    tests_require=tests_require,
    extras_require={
        'tests': install_requires + tests_require,
    }
)
