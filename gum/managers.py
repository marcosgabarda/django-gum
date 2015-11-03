# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gum.utils import elasticsearch_connection


class ElasticsearchManager(object):
    """Like a `ModelManager` gives to the user methods to apply queries
    to Elasticsearch from a specific model.
    """

    def __init__(self, model=None, mapping_type=None):
        self.model = None
        self.mapping_type = None

    def search(self, **kwargs):
        """Partial application of `search` function from Elasticsearch
        module.

        :param kwargs:
        """
        es = elasticsearch_connection()
        if 'index' not in kwargs:
            kwargs["index"] = self.mapping_type.index
        if 'doc_type' not in kwargs:
            kwargs["doc_type"] = self.mapping_type.get_type()
        return es.search(**kwargs)