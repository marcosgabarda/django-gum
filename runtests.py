#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import django
from django.conf import settings
from django.core.management import call_command


def run_tests():
    if not settings.configured:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }

        # Configure test environment
        settings.configure(
            DATABASES=DATABASES,
            INSTALLED_APPS=(
                'gum',
                'gum.tests',
                'gum.tests.test_app',
            ),
            GUM_DEBUG=True,
            GUM_ELASTICSEARCH_URLS=["http://127.0.0.1:9200/"],
            GUM_ELASTICSEARCH_INDEX=".gum-tests",
            ROOT_URLCONF=None,
            MIDDLEWARE_CLASSES=(),
        )

        if django.VERSION >= (1, 7):
            django.setup()

        failures = call_command(
            'test', 'gum', interactive=False, failfast=False, verbosity=2
        )

        sys.exit(bool(failures))

if __name__ == '__main__':
    run_tests()
