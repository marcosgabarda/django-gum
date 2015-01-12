# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from elasticsearch import Elasticsearch

from gum.settings import ELASTICSEARCH_URLS, ELASTICSEARCH_TIMEOUT


def _build_key(urls):
    key = (urls,)
    return key


_cached_elasticsearch = {}


def elasticsearch_connection(urls=None):
    """Create an elasticsearch `Elasticsearch` object and return it."""
    connection_urls = urls or ELASTICSEARCH_URLS
    key = _build_key(urls)
    if key in _cached_elasticsearch:
        return _cached_elasticsearch[key]
    try:
        _ = iter(connection_urls)
    except TypeError:
        connection_urls = [connection_urls]
    es = Elasticsearch(hosts=connection_urls, timeout=ELASTICSEARCH_TIMEOUT)
    _cached_elasticsearch[key] = es
    return es