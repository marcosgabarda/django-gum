# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import elasticsearch
import six
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save, pre_delete
from elasticsearch.helpers import bulk

from gum.managers import ElasticsearchManager
from gum.settings import ELASTICSEARCH_INDICES, DEFAULT_ELASTICSEARCH_SETTINGS
from gum.signals import handle_save, handle_delete
from gum.utils import elasticsearch_connection


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class MappingType(object):

    # Custom URLs for connecting to an specific Elasticsearch server
    urls = None
    # Index to apply this mapping type
    index = None
    # Settings used for previous index
    settings = None

    def __init__(self, model):
        """Initialize a MappingType instance for a given
         `model`.

        :param model:
        :return:
        """
        self.model = model
        # If ``index`` is not defined, use settings
        if not self.index:
            self.index = ELASTICSEARCH_INDICES
        super(MappingType, self).__init__()

    def get_id(self, instance):
        """Gets the internal Elasticsearch id for instance.
        :param instance:
        """
        try:
            return instance.pk
        except AttributeError:
            return None

    def get_type(self):
        """Gets a strings that represents the type for the model."""
        return "%s_%s" % (
            self.model._meta.app_label, self.model._meta.model_name
        )

    def get_elasticsearch_connection(self):
        """Gets the Elasticsearch connection with the urls attribute"""
        return elasticsearch_connection(urls=self.urls)

    def get_actions(self, documents):
        """Gets a generator for obtaining the bulk action for each document
        in documents. We assume documents is iterable, and each document is
        a dictionary.
        """
        for document in documents:
            document["_index"] = self.index
            document["_type"] = self.get_type()
            yield document

    def mapping(self):
        """Gets the mapping of a given model. Only uses the model class, not
        the instance.

        TODO: By the moment, it must be implemented by subclasses.
        """
        raise NotImplementedError()

    def document(self, instance):
        """Logic to convert an instance of the model into a document for indexing.

        TODO: By the moment, it must be implemented by subclasses.

        :param instance:
        :return:
        """
        raise NotImplementedError()

    def create_mapping_type(self, update_all_types=False):
        """Creates the Elasticsearch type.

        :param update_all_types:
        """
        es = self.get_elasticsearch_connection()
        es.indices.put_mapping(
            index=self.index,
            doc_type=self.get_type(),
            body=self.mapping(),
            update_all_types=update_all_types,
            ignore=409
        )

    def index_single_document(self, es, document_id, document):
        """Creates a single new document in the index."""
        if not document_id:
            es.index(
                index=self.index,
                doc_type=self.get_type(),
                body=document
            )
        es.index(
            index=self.index,
            doc_type=self.get_type(),
            id=document_id,
            body=document
        )

    def index_bulk_documents(self, es, documents):
        """Creates a bulk of new documents in  the index."""
        actions = self.get_actions(documents)
        bulk(es, actions=actions)

    def index_document(self, instance):
        """Indexes an instance of the model.

        :param instance:
        :return:
        """
        es = self.get_elasticsearch_connection()
        document = self.document(instance)
        document_id = self.get_id(instance)
        if isinstance(document, dict):
            # If is a dict, single create
            self.index_single_document(es, document_id=document_id, document=document)
        else:
            try:
                # If iterable, then bulk create...
                _ = iter(document)
                self.index_bulk_documents(es, documents=document)
            except TypeError:
                # Not iterable, we don't index
                pass

    def delete_document(self, instance):
        """Deletes an instance of the model.

        :param instance:
        :return:
        """
        es = self.get_elasticsearch_connection()
        try:
            es.delete(
                index=self.index,
                doc_type=self.get_type(),
                id=self.get_id(instance),
            )
        except elasticsearch.exceptions.NotFoundError:
            pass


class Indexer(object):
    """Allows to register a model with its mapper class."""

    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, mapping_type_class=None):
        """Register a given model(s) with the given mapping type class.

        The model(s) should be Model classes, not instances.

        If a model is already registered, this will raise AlreadyRegistered.
        :param mapping_type_class:
        :param model_or_iterable:
        """
        if not mapping_type_class:
            mapping_type_class = MappingType
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered for indexing' % model.__name__)
            mapping_type = mapping_type_class(model)
            if not hasattr(model, "elasticsearch"):
                model.elasticsearch = ElasticsearchManager()
                model.elasticsearch.model = model
                model.elasticsearch.mapping_type = mapping_type
            post_save.connect(handle_save, sender=model)
            pre_delete.connect(handle_delete, sender=model)
            self._registry[model] = mapping_type

    def get_registered_models(self):
        """Returns a list of all registered models, or just concrete
        registered models.
        """
        return [model for (model, mapping_type_class) in self._registry.items()]

    def get_mapping_type(self, model):
        """Gets the mapping type instance for a given `model` class.
        :param model:
        """
        try:
            return self._registry[model]
        except KeyError:
            raise NotRegistered()

    def initialize_index(self):
        """Creates and initialize index.

        TODO: Add settings configuration of the index.
        """
        es = elasticsearch_connection()
        es.indices.create(index=ELASTICSEARCH_INDICES, body=DEFAULT_ELASTICSEARCH_SETTINGS, ignore=400)
        for _, mapping_type in six.iteritems(self._registry):
            mapping_type_es = mapping_type.get_elasticsearch_connection()
            if mapping_type.index != ELASTICSEARCH_INDICES or mapping_type.urls is not None:
                mapping_type_es.indices.create(
                    index=mapping_type.index,
                    body=mapping_type.settings or DEFAULT_ELASTICSEARCH_SETTINGS,
                    ignore=400
                )

    def update_settings(self):
        """Updates the settings of the indexes."""
        es = elasticsearch_connection()
        es.indices.close(index=ELASTICSEARCH_INDICES)
        es.indices.put_settings(index=ELASTICSEARCH_INDICES, body=DEFAULT_ELASTICSEARCH_SETTINGS)
        es.indices.open(index=ELASTICSEARCH_INDICES)
        for _, mapping_type in six.iteritems(self._registry):
            mapping_type_es = mapping_type.get_elasticsearch_connection()
            if mapping_type.index != ELASTICSEARCH_INDICES or mapping_type.urls is not None:
                mapping_type_es.indices.close(index=mapping_type.index)
                mapping_type_es.indices.put_settings(
                    index=mapping_type.index,
                    body=mapping_type.settings or DEFAULT_ELASTICSEARCH_SETTINGS,
                )
                mapping_type_es.indices.open(index=mapping_type.index)

    def remove_index(self):
        """Deletes used indices.

        TODO: Add settings configuration of the index.
        """
        es = elasticsearch_connection()
        es.indices.delete(index=ELASTICSEARCH_INDICES, ignore=400)
        for _, mapping_type in six.iteritems(self._registry):
            mapping_type_es = mapping_type.get_elasticsearch_connection()
            if mapping_type.index != ELASTICSEARCH_INDICES or mapping_type.urls is not None:
                mapping_type_es.indices.delete(index=mapping_type.index, ignore=400)

    def update_index(self, stdout=None, only_mapping=False, restrict_to=None, update_all_types=False):
        """Update index for all registered models.
        :param update_all_types:
        :param restrict_to:
        :param only_mapping:
        :param stdout:
        """
        for model, mapping_type in six.iteritems(self._registry):
            if restrict_to is not None and model not in restrict_to:
                continue
            if issubclass(model, models.Model):
                try:
                    instances = model.objects.all()
                    total_instances = instances.count()
                except AttributeError:
                    # Abstract model
                    instances = []
                    total_instances = 0
            else:
                # Object, not a Django model
                instances = []
                total_instances = 0
            if stdout:
                stdout.write("Indexing %s instances from %s " % (total_instances, str(model)))
            mapping_type.create_mapping_type(update_all_types=update_all_types)
            if not only_mapping:
                for step, instance in enumerate(instances):
                    mapping_type.index_document(instance)
                    if stdout:
                        import os
                        progress = (step + 1) / float(total_instances)
                        _, columns = os.popen('stty size', 'r').read().split()
                        limit = min(int(columns) - 10, 100)
                        graph_progress = int(progress * limit)
                        stdout.write('\r', ending='')
                        progress_format = "[%-{}s] %d%%".format(limit)
                        stdout.write(progress_format % ('='*graph_progress, int(progress*100)), ending='')
                        stdout.flush()
            if stdout:
                stdout.write('')

# This global object represents the singleton indexer object
indexer = Indexer()
