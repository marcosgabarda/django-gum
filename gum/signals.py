# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from gum.settings import USE_CELERY
from gum import tasks


def handle_save(sender, instance, **kwargs):
    """Handle save model.

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """

    if USE_CELERY:
        sender_content_type = ContentType.objects.get_for_model(sender)
        tasks.handle_save.delay(sender_content_type.pk, instance.pk)
    else:
        from gum.indexer import indexer, NotRegistered
        try:

            mapping_type = indexer.get_mapping_type(sender)
            mapping_type.index_document(instance)
        except NotRegistered:
            pass


def handle_delete(sender, instance, **kwargs):
    """Handle delete model.

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if USE_CELERY:
        sender_content_type = ContentType.objects.get_for_model(sender)
        tasks.handle_delete.delay(sender_content_type.pk, instance.pk)
    else:
        from gum.indexer import indexer, NotRegistered
        try:
            mapping_type = indexer.get_mapping_type(sender)
            mapping_type.delete_document(instance)
        except NotRegistered:
            pass