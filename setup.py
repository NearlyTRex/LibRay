#!/usr/bin/env python3
# -*- coding: utf8 -*-

from setuptools import setup

setup(
  name="libray",
  version="0.0.2",
  description='A Libre (FLOSS) Python application for unencrypting, extracting, repackaging, and encrypting PS3 ISOs',
  author="Nichlas Severinsen",
  author_email="ns@nsz.no",
  url="https://notabug.org/necklace/libray",
  packages=['libray'],
  scripts=['libray/libray'],
  install_requires=[
    'tqdm==4.32.2',
    'pycrypto==2.6.1',
    'requests==2.22.0',
    'beautifulsoup4==4.7.1',
  ],
)
