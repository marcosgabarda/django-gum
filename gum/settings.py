# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings


# List of URLs of Elasticsearch servers
DEFAULT_ELASTICSEARCH_URLS = ["http://127.0.0.1:9200/"]
ELASTICSEARCH_URLS = getattr(settings, "GUM_ELASTICSEARCH_URLS", DEFAULT_ELASTICSEARCH_URLS)

# Params for connection to Elasticsearch
DEFAULT_ELASTICSEARCH_TIMEOUT = 5
ELASTICSEARCH_TIMEOUT = getattr(settings, "GUM_ELASTICSEARCH_TIMEOUT", DEFAULT_ELASTICSEARCH_TIMEOUT)
DEFAULT_ELASTICSEARCH_CONNECTION_PARAMS = {
    "timeout": ELASTICSEARCH_TIMEOUT
}
ELASTICSEARCH_CONNECTION_PARAMS = getattr(
    settings, "GUM_ELASTICSEARCH_CONNECTION_PARAMS", DEFAULT_ELASTICSEARCH_CONNECTION_PARAMS
)

# A comma-separated list of index names the alias should point to (supports wildcards);
# use _all or omit to perform the operation on all indices.
DEFAULT_INDICES = "_all"
ELASTICSEARCH_INDICES = getattr(settings, "GUM_ELASTICSEARCH_INDEX", DEFAULT_ELASTICSEARCH_TIMEOUT)

DEBUG = getattr(settings, 'GUM_DEBUG', False)
USE_CELERY = getattr(settings, 'GUM_USE_CELERY', False)
INDEX_FILES = tuple(getattr(settings, 'GUM_INDEX_FILES', ()))

# Default configuration for indices
DEFAULT_ELASTICSEARCH_SETTINGS = getattr(
    settings,
    'GUM_DEFAULT_ELASTICSEARCH_SETTINGS',
    {
        'settings': {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": ["gum_ngram"]
                    },
                    "edgengram_analyzer": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": ["gum_edgengram"]
                    }
                },
                "tokenizer": {
                    "gum_ngram_tokenizer": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15,
                    },
                    "gum_edgengram_tokenizer": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15,
                        "side": "front"
                    }
                },
                "filter": {
                    "gum_ngram": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15
                    },
                    "gum_edgengram": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15
                    }
                }
            }
        }
    }
)
