.. _ref-commands:

===================
Management commands
===================

gum
===

Base command to manage Gum based indices. It accepts the
following arguments:

``--update-index (<app_name.model> <app_name.model> ... )``:
    By default, it updates all registered models indices. It can
    be provided a list of models to restrict the update.

``--update-settings``:
    It updates the settings of the indices.

``--remove``:
    Deletes all indices.

Examples::

    # Update everything.
    ./manage.py gum --update-index
    # Update a model.
    ./manage.py gum --update-index blog.Post
