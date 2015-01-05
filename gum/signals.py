# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def handle_save(sender, instance, **kwargs):
    """Handle save model.

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
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
    from gum.indexer import indexer, NotRegistered
    try:
        mapping_type = indexer.get_mapping_type(sender)
        mapping_type.delete_document(instance)
    except NotRegistered:
        pass