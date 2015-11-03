# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError

from gum.indexer import indexer

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model


class Command(BaseCommand):

    help = "Updates index settings"

    def handle(self, *args, **options):
        self.stdout.write('Updating index settings... ', ending='')
        indexer.update_settings()
        self.stdout.write(' OK')
