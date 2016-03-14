# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from elasticsearch import Elasticsearch

from gum.settings import ELASTICSEARCH_URLS, ELASTICSEARCH_TIMEOUT, ELASTICSEARCH_CONNECTION_PARAMS


def _build_key(urls):
    key = (urls,)
    return key


_cached_elasticsearch = {}


def elasticsearch_connection(urls=None):
    """Create an elasticsearch `Elasticsearch` object and return it.
    :param urls:
    """
    connection_urls = urls or ELASTICSEARCH_URLS
    key = _build_key(urls)
    if key in _cached_elasticsearch:
        return _cached_elasticsearch[key]
    try:
        _ = iter(connection_urls)
    except TypeError:
        connection_urls = [connection_urls]
    es_params = ELASTICSEARCH_CONNECTION_PARAMS
    es = Elasticsearch(hosts=connection_urls, **es_params)
    _cached_elasticsearch[key] = es
    return es
