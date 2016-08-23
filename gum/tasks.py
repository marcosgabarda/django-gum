# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from celery.task import task
from celery.utils.log import get_task_logger
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


logger = get_task_logger(__name__)


@task
def handle_save(sender_content_type_pk, instance_pk):
    """Async task to handle the indexation of a model.
    :param instance_pk:
    :param sender_content_type_pk:
    """
    from gum.indexer import indexer, NotRegistered
    try:
        sender_content_type = ContentType.objects.get(pk=sender_content_type_pk)
        sender = sender_content_type.model_class()
        instance = sender.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        logger.warning("Object ({}, {}) not found".format(sender_content_type_pk, instance_pk))
        return None
    try:
        mapping_type = indexer.get_mapping_type(sender)
        mapping_type.index_document(instance)
    except NotRegistered:
        logger.warning("Object ({}, {}) not register".format(sender_content_type_pk, instance_pk))
        return None
    return sender_content_type_pk, instance_pk


@task
def handle_delete(sender_content_type_pk, instance_pk):
    """Async task to delete a model from the index.
    :param instance_pk:
    :param sender_content_type_pk:
    """
    from gum.indexer import indexer, NotRegistered
    try:
        sender_content_type = ContentType.objects.get(pk=sender_content_type_pk)
        sender = sender_content_type.model_class()
        instance = sender.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        logger.warning("Object ({}, {}) not found".format(sender_content_type_pk, instance_pk))
        return None
    try:
        mapping_type = indexer.get_mapping_type(sender)
        mapping_type.delete_document(instance)
    except NotRegistered:
        return None
    return sender_content_type_pk, instance_pk
