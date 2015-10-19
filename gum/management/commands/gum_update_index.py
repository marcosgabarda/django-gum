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

    args = "<app_name.model_name app_name.model_name ...>"
    help = "Creates and updates index"

    def handle(self, *args, **options):

        # Parse arguments
        selected_models = []
        for input_model in args:
            try:
                app_name, model_name = input_model.split(".")
                model_class = get_model(app_name, model_name)
                selected_models.append(model_class)
            except (ValueError, LookupError):
                raise CommandError("Model not found for indexing")
        restrict_to = selected_models if selected_models else None

        self.stdout.write('Initializing index...', ending='')
        indexer.initialize_index()
        self.stdout.write(' OK')
        indexer.update_index(stdout=self.stdout, restrict_to=restrict_to)
