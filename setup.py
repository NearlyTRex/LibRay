#!/usr/bin/env python3
# -*- coding: utf8 -*-

from setuptools import setup

setup(
  name="libray",
  version="0.0.1",
  description='A Libre (FLOSS) Python application for unencrypting, extracting, repackaging, and encrypting PS3 ISOs',
  author="Nichlas Severinsen",
  author_email="ns@nsz.no",
  url="https://notabug.org/necklace/libray",
  packages=['libray'],
  scripts=['libray/libray'],
  install_requires=['pycrypto==2.6.1'],
)