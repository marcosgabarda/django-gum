.. _ref-settings:

==========================
Configuration and defaults
==========================

Gum options
===========

GUM_DEBUG
---------

Activates/deactivates the debug output.

Defaults to ``False``.

GUM_USE_CELERY
--------------

Boolean setting to activate/desactivate the use of Celery
to update a model document when it is saved.

Defaults to ``False``.

GUM_INDEX_FILES
---------------

You can use this variable to give a list of index files to be checked
by Gum in order to find registered mappings, in addition to index.py files.

Defaults to ``tuple()``.

Elasticsearch options
=====================

GUM_ELASTICSEARCH_URLS
----------------------

A list of address of Elasticsearch servers.

Defaults to ``["http://127.0.0.1:9200/"]``.

GUM_ELASTICSEARCH_CONNECTION_PARAMS
-----------------------------------

Parameters given to `Elasticsearch class <https://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch.Elasticsearch>`_ to
connect with Elasticsearch server.

Defatils to::

    {
        "timeout": 5
    }

GUM_ELASTICSEARCH_INDEX
-----------------------

Index name to use by default.

Defaults to ``"_all"``.

GUM_DEFAULT_ELASTICSEARCH_SETTINGS
----------------------------------

Defines the settings of all indices created by Gum.

Defaults to::

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
