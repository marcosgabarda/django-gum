# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from gum.utils import elasticsearch_connection


class ElasticsearchManager(object):
    """Like a `ModelManager` gives to the user methods to apply queries
    to Elasticsearch from a specific model.
    """

    def __init__(self, model=None, mapping_type=None, urls=None):
        self.model = model
        self.mapping_type = mapping_type
        self.urls = urls

    def get_elasticsearch_connection(self):
        """Gets the Elasticsearch connection with the urls attribute"""
        if self.mapping_type is not None:
            return self.mapping_type.get_elasticsearch_connection()
        return elasticsearch_connection(urls=self.urls)

    def search(self, **kwargs):
        """Partial application of `search` function from Elasticsearch
        module.

        :param kwargs:
        """
        es = self.get_elasticsearch_connection()
        if 'index' not in kwargs:
            kwargs["index"] = self.mapping_type.index
        if 'doc_type' not in kwargs:
            kwargs["doc_type"] = self.mapping_type.get_type()
        return es.search(**kwargs)

    def index(self, instance):
        """Shortcut to index an instance.

        :param instance:
        :return:
        """
        return self.mapping_type.index_document(instance)


class GenericElasticsearchManager(ElasticsearchManager):
    """Generic Elasticsearch manager to make queries without using MappingTypes."""

    def search(self, **kwargs):
        """For this manager it's mandatory to specify index and doc_type on each call:

        >>> elasticsearch = GenericElasticsearchManager()
        >>> elasticsearch.search(index="index-name", doc_type="mapping-type-name")

        :param kwargs:
        :return:
        """
        assert "index" in kwargs
        assert "doc_type" in kwargs
        return super(GenericElasticsearchManager, self).search(**kwargs)
