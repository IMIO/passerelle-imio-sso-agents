#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools.command.install_lib import install_lib as _install_lib
from setuptools import setup, find_packages

class install_lib(_install_lib):
    def run(self):
        _install_lib.run(self)

version = "0.1.6"

setup(
    name='passerelle-imio-sso-agents',
    version=version,
    author='iA.Teleservices',
    author_email='support-ts@imio.be',
    url='https://github.com/IMIO/passerelle-imio-sso-agents',
    packages=find_packages(),
    install_requires=['django>=3.2, <3.3',],
    cmdclass={
        'install_lib': install_lib,
    }
)

