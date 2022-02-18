#!/usr/bin/env python3
# -*- coding: utf8 -*-


from setuptools import setup


with open('README.md') as f:
  long_description = f.read()


setup(
  name="libray",
  version="0.0.8",
  description='A Libre (FLOSS) Python application for unencrypting, extracting, repackaging, and encrypting PS3 ISOs',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author="Nichlas Severinsen",
  author_email="ns@nsz.no",
  url="https://notabug.org/necklace/libray",
  packages=['libray'],
  scripts=['libray/libray'],
  install_requires=[
    'tqdm~=4.62.3',
    'pycryptodome~=3.14.1',
    'requests~=2.27.1',
    'beautifulsoup4~=4.10.0',
    'html5lib~=1.1'
  ],
  include_package_data=True,
  package_data={'': ['data/keys.db']},
)
