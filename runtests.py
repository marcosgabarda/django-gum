#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import django
from django.conf import settings
from django.core.management import call_command


def runtests():
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
        ),
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
    runtests()