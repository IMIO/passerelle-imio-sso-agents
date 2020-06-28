#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools.command.install_lib import install_lib as _install_lib
from setuptools import setup, find_packages

class install_lib(_install_lib):
    def run(self):
        _install_lib.run(self)

setup(
    name='passerelle-imio-sso-agents',
    author='Christophe Boulanger',
    author_email='christophe.boulanger@imio.be',
    url='https://github.com/IMIO/passerelle-imio-sso-agents',
    packages=find_packages(),
    install_requires=[
        'django>=1.11',
        ],
    cmdclass={
        'install_lib': install_lib,
    }
)

