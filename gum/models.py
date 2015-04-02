# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django


def autodiscover():
    """
    Auto-discover INSTALLED_APPS translation.py modules and fail silently when
    not present. This forces an import on them to register.
    Also import explicit modules.
    """
    import os
    import sys
    import copy
    from django.conf import settings
    from django.utils.module_loading import module_has_submodule
    from gum.indexer import indexer
    from gum.settings import INDEX_FILES, DEBUG

    if django.VERSION < (1, 7):
        from django.utils.importlib import import_module
        mods = [(app, import_module(app)) for app in settings.INSTALLED_APPS]
    else:
        from importlib import import_module
        from django.apps import apps
        mods = [(app_config.name, app_config.module) for app_config in apps.get_app_configs()]

    for (app, mod) in mods:
        # Attempt to import the app's translation module.
        module = '%s.index' % app
        before_import_registry = copy.copy(indexer._registry)
        try:
            import_module(module)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            indexer._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an translation module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'index'):
                raise

    for module in INDEX_FILES:
        import_module(module)

    # In debug mode, print a list of registered models and pid to stdout.
    # Note: Differing model order is fine, we don't rely on a particular
    # order, as far as base classes are registered before subclasses.
    if DEBUG:
        try:
            if sys.argv[1] in ('runserver', 'runserver_plus'):
                models = indexer.get_registered_models()
                names = ', '.join(m.__name__ for m in models)
                print('gum: Registered %d models for indexing'
                      ' (%s) [pid: %d].' % (len(models), names, os.getpid()))
        except IndexError:
            pass


def handle_indexer_registrations(*args, **kwargs):
    autodiscover()


if django.VERSION < (1, 7):
    handle_indexer_registrations()
