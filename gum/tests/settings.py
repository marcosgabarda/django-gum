# -*- coding: utf-8 -*-
from __future__ import unicode_literals

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = (
    'gum',
    'gum.tests',
    'gum.tests.test_app',
)

GUM_DEBUG = True
GUM_ELASTICSEARCH_URLS = ["http://127.0.0.1:9200/"]
GUM_ELASTICSEARCH_URLS_ALT = ["http://127.0.0.1:9200/"]
GUM_ELASTICSEARCH_INDEX = ".gum-tests"

MIDDLEWARE_CLASSES = ()
SECRET_KEY = "dummy"
