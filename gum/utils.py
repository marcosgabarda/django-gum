# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from elasticsearch import Elasticsearch

from gum.settings import ELASTICSEARCH_URLS, ELASTICSEARCH_TIMEOUT


def elasticsearch_connection(urls=None):
    """Create an elasticsearch `Elasticsearch` object and return it."""
    connection_urls = urls or ELASTICSEARCH_URLS
    try:
        _ = iter(connection_urls)
    except TypeError:
        connection_urls = [connection_urls]
    es = Elasticsearch(hosts=connection_urls, timeout=ELASTICSEARCH_TIMEOUT)
    return es