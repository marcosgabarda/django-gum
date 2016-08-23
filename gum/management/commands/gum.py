# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.core.management import BaseCommand, CommandError

from gum.indexer import indexer

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model


class Command(BaseCommand):

    help = "Command for managing indices from Elasticsearch"

    def add_arguments(self, parser):
        actions = parser.add_mutually_exclusive_group()
        actions.add_argument(
            "--init", action="store_const", dest="action", const="init",
            help="creates indexes and updates the settings",
        )
        actions.add_argument(
            "--update-index", nargs="*", action="store", dest='update-index', help="updates indices for given models"
        )
        actions.add_argument(
            "--update-settings", action="store_const", dest="action",  const="update-settings", help="updates settings",
        )
        actions.add_argument(
            "--remove", action="store_const", dest="action", const="remove", help="remove all indices"
        )

    def _init_index(self):
        """Order to update index."""
        self.stdout.write('Initializing index...', ending='')
        indexer.initialize_index()
        indexer.update_settings()
        self.stdout.write(' OK')
        indexer.update_index(stdout=self.stdout, only_mapping=True)

    def _update_index(self, models):
        """Order to update index."""
        selected_models = []
        for input_model in models:
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

    def _update_settings(self):
        """Order to update settings."""
        self.stdout.write('Updating index settings... ', ending='')
        indexer.update_settings()
        self.stdout.write(' OK')

    def _remove_index(self):
        """Order to remove index."""
        self.stdout.write('Removing index... ', ending='')
        indexer.remove_index()
        self.stdout.write(' OK')

    def handle(self, *args, **options):
        actions = {
            "update-settings": self._update_settings,
            "remove": self._remove_index,
            "init": self._init_index,
        }
        action = options.get("action")
        if action in actions:
            actions[options.get("action")]()
        elif "update-index" in options:
            self._update_index(options.get("update-index"))
