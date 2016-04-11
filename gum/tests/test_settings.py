# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import settings as _settings

TEST_SETTINGS = dict((k, getattr(_settings, k)) for k in dir(_settings) if k == k.upper())

TASKS_TEST_SETTINGS = TEST_SETTINGS
TASKS_TEST_SETTINGS.update(dict(GUM_USE_CELERY=True))
