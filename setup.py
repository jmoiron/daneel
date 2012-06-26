#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for daneel."""

from setuptools import setup, find_packages
import sys, os

version = '0.1'

# some trove classifiers:

# License :: OSI Approved :: MIT License
# Intended Audience :: Developers
# Operating System :: POSIX

setup(
    name='daneel',
    version=version,
    description="",
    long_description=open('README.rst').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    keywords='irc bot',
    author='Jason Moiron',
    author_email='jmoiron@jmoiron.net',

    url='http://github.com/jmoiron/daneel',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    install_requires=[
        "requests",
        "lxml",
        "irctk",
      # -*- Extra requirements: -*-
    ],
    scripts=[
        "bin/daneel-bot.py",
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
