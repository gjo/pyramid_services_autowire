#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from setuptools import setup
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))
description = 'An autowire utility for pyramid_services'
try:
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        readme = f.read()
    with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
        changes = f.read()
    long_description = '\n\n'.join([readme, changes])
except:
    long_description = description


setup(
    description=description,
    long_description=long_description,
)
