# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings


# List of URLs of Elasticsearch servers
DEFAULT_ELASTICSEARCH_URLS = ["http://127.0.0.1:9200/"]
ELASTICSEARCH_URLS = getattr(settings, "GUM_ELASTICSEARCH_URLS", DEFAULT_ELASTICSEARCH_URLS)

# Timeout for connection to Elasticsearch
DEFAULT_ELASTICSEARCH_TIMEOUT = 5
ELASTICSEARCH_TIMEOUT = getattr(settings, "GUM_ELASTICSEARCH_TIMEOUT", DEFAULT_ELASTICSEARCH_TIMEOUT)

# A comma-separated list of index names the alias should point to (supports wildcards);
# use _all or omit to perform the operation on all indices.
DEFAULT_INDICES = "_all"
ELASTICSEARCH_INDICES = getattr(settings, "GUM_ELASTICSEARCH_INDEX", DEFAULT_ELASTICSEARCH_TIMEOUT)

DEBUG = getattr(settings, 'GUM_DEBUG', False)
INDEX_FILES = tuple(getattr(settings, 'GUM_INDEX_FILES', ()))