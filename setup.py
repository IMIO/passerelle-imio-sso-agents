#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install
from setuptools import setup, find_packages
import os

setup(
    name='passerelle-imio-sso-agents',
    author='Christophe Boulanger',
    author_email='christophe.boulanger@imio.be',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/IMIO/passerelle-imio-sso-agents',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    zip_safe=False
)

