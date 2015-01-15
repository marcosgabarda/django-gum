# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.base import ModelBase
from django.db.models.signals import pre_save, post_save, pre_delete
from gum.managers import ElasticsearchManager
from gum.signals import handle_save, handle_delete

from gum.utils import elasticsearch_connection
from gum.settings import ELASTICSEARCH_INDICES


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class MappingType(object):

    # Index to apply this mapping type
    index = None

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
        """Gets the internal Elasticsearch id for instance."""
        return instance.pk

    def get_type(self):
        """Gets a strings that represents the type for the model."""
        return "%s_%s" % (
            self.model._meta.app_label, self.model._meta.model_name
        )

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

    def create_mapping_type(self):
        """Creates the Elasticsearch type."""
        es = elasticsearch_connection()
        es.indices.put_mapping(
            index=self.index,
            doc_type=self.get_type(),
            body=self.mapping(),
            ignore=409
        )

    def index_document(self, instance):
        """Indexes an instance of the model.

        :param instance:
        :return:
        """
        es = elasticsearch_connection()
        es.index(
            index=self.index,
            doc_type=self.get_type(),
            id=self.get_id(instance),
            body=self.document(instance)
        )

    def delete_document(self, instance):
        """Deletes an instance of the model.

        :param instance:
        :return:
        """
        es = elasticsearch_connection()
        es.delete(
            index=self.index,
            doc_type=self.get_type(),
            id=self.get_id(instance),
        )


class Indexer(object):
    """Allows to register a model with its mapper class."""

    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, mapping_type_class=None):
        """Register a given model(s) with the given mapping type class.

        The model(s) should be Model classes, not instances.

        If a model is already registered, this will raise AlreadyRegistered.
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
        """Gets the mapping type insance for a given `model` class."""
        try:
            return self._registry[model]
        except KeyError:
            raise NotRegistered()

    def initialize_index(self):
        """Creates and initialize index.

        TODO: Add settings configuration of the index.
        """
        es = elasticsearch_connection()
        es.indices.create(index=ELASTICSEARCH_INDICES, ignore=400)
        for _, mapping_type in self._registry.iteritems():
            if mapping_type.index != ELASTICSEARCH_INDICES:
                es.indices.create(index=mapping_type.index, ignore=400)

    def remove_index(self):
        """Deletes used indices.

        TODO: Add settings configuration of the index.
        """
        es = elasticsearch_connection()
        es.indices.delete(index=ELASTICSEARCH_INDICES, ignore=400)
        for _, mapping_type in self._registry.iteritems():
            if mapping_type.index != ELASTICSEARCH_INDICES:
                es.indices.delete(index=mapping_type.index, ignore=400)

    def update_index(self, stdout=None):
        """Update index for all registered models."""
        for model, mapping_type in self._registry.iteritems():
            instances = model.objects.all()
            total_instances = instances.count()
            if stdout:
                stdout.write("Indexing %s instances from %s " % (total_instances, str(model)))
                stdout.write("Indexing %s instances from %s " % (total_instances, str(model)))
            mapping_type.create_mapping_type()
            for step, instance in enumerate(instances):
                mapping_type.index_document(instance)
                if stdout:
                    progress = (step + 1) / total_instances
                    stdout.write('\r')
                    stdout.write("[%-100s] %d%%" % ('='*progress, progress))
                    stdout.flush()

# This global object represents the singleton indexer object
indexer = Indexer()