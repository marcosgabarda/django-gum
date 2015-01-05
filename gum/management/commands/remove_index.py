# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from gum.indexer import indexer


class Command(BaseCommand):

    help = "Removes index"

    def handle(self, *args, **options):
        indexer.remove_index()