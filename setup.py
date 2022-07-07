#!/usr/bin/python3

from codecs import open
from os import path
from setuptools import setup, find_packages


setup(
    install_requires=list(open('requirements.txt')),
    py_modules=[]
)
