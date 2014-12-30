# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class GumConfig(AppConfig):
    name = 'gum'
    verbose_name = 'Gum'

    def ready(self):
        from gum.models import handle_indexer_registrations
        handle_indexer_registrations()
