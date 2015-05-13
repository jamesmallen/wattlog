#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='WattLog',
    # GETTING-STARTED: set your app version:
    version='1.0',
    # GETTING-STARTED: set your app description:
    description='OpenShift App',
    # GETTING-STARTED: set author name (your name):
    author='James M. Allen',
    # GETTING-STARTED: set author email (your email):
    author_email='james.m.allen@gmail.com',
    # GETTING-STARTED: set author url (your url):
    url='http://jamesmallen.net',
    # GETTING-STARTED: define required django version:
    install_requires=['Django<=1.8', 'djangorestframework<=3.1.1'],
)
