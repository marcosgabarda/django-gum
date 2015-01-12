# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.task import task
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from gum.indexer import indexer, NotRegistered


@task
def handle_save(sender_content_type_pk, instance_pk):
    """Async task to handle the indexation of a model."""
    try:
        sender_content_type = ContentType.objects.get(pk=sender_content_type_pk)
        sender = sender_content_type.model_class()
        instance = sender.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        return False
    try:
        mapping_type = indexer.get_mapping_type(sender)
        mapping_type.index_document(instance)
    except NotRegistered:
        return False
    return True


@task
def handle_delete(sender_content_type_pk, instance_pk):
    """Async task to delete a model from the index."""
    try:
        sender_content_type = ContentType.objects.get(pk=sender_content_type_pk)
        sender = sender_content_type.model_class()
        instance = sender.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        return False
    try:
        mapping_type = indexer.get_mapping_type(sender)
        mapping_type.delete_document(instance)
    except NotRegistered:
        pass
