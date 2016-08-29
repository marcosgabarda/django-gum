#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

# Dynamically calculate the version based on gum.VERSION.
version = __import__('gum').get_version()

setup(
    name='django-gum',
    version=version,
    description='Elasticsearch client with Django support.',
    author='Marcos Gabarda',
    author_email='hey@marcosgabarda.com',
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/marcosgabarda/django-gum',
    packages=[
        'gum',
        'gum.management',
        'gum.management.commands'
    ],
    install_requires=[
        'django>=1.5',
        'elasticsearch>=2.0.0,<3.0.0',
        'celery',
        'six'
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
