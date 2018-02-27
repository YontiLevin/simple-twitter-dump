#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, Command

# Package meta-data.
NAME = 'simple_twitter_dump'
DESCRIPTION = 'a wrapper for tweepy to quickly scrape twitter'
URL = 'https://github.com/yontilevin/simple_twitter_dump'
EMAIL = 'yonti0@gmail.com'
AUTHOR = 'Yonti Levin'
VERSION = '0.0.1'

# requirements
with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description='',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires='>=3.6.0',
    packages=['std'],
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)