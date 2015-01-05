#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup

setup(
    name='django-gum',
    version='0.0.1',
    description='Elasticsearch client with Django support.',
    author='Marcos Gabarda',
    author_email='marcosgabarda@gmail.com',
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/onpublico/django-gum',
    packages=[
        'gum',
        'gum.management',
        'gum.management.commands'
    ],
    requires=[
        'django(>=1.4)',
        'elasticsearch(>=1.0.0,<2.0.0)',
    ],
    # package_data={
    #     'django-gum': []
    # },
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License ::  OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)