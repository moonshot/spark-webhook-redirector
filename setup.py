#!/usr/bin/env python

import os
from setuptools import setup

REQUIREMENTS = [line.strip() for line in
                open("requirements.txt").readlines()]
setup(
    name='redirector',
    version='0.1a0',
    author='moonshot',
    packages=['redirector'],
    install_requires=REQUIREMENTS,
)
