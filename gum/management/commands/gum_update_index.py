# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from gum.indexer import indexer


class Command(BaseCommand):

    help = "Creates and updates index"

    def handle(self, *args, **options):
        self.stdout.write('Initializing index...', ending='')
        indexer.initialize_index()
        self.stdout.write(' OK')
        self.stdout.write('Updating index...', ending='')
        indexer.update_index(stdout=self.stdout)
        self.stdout.write(' OK')