==========
Django Gum
==========

Gum is a Django app for integrate Elasticsearch 1.x with Django. You can find documentation at
`https://django-gum.readthedocs.org <https://django-gum.readthedocs.org>`_.


.. image:: https://badges.gitter.im/marcosgabarda/django-gum.svg
    :target: https://gitter.im/marcosgabarda/django-gum?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://badge.fury.io/py/django-gum.svg
    :target: https://badge.fury.io/py/django-gum

.. image:: https://img.shields.io/pypi/dm/django-gum.svg
    :target: https://pypi.python.org/pypi/django-gum

.. image:: https://readthedocs.org/projects/django-gum/badge/?version=latest
    :target: http://django-gum.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/marcosgabarda/django-gum.svg?branch=master
    :target: https://travis-ci.org/marcosgabarda/django-gum

.. image:: https://coveralls.io/repos/github/marcosgabarda/django-gum/badge.svg?branch=master
    :target: https://coveralls.io/github/marcosgabarda/django-gum?branch=master


Quick start
-----------

**1** Install using pip::

    pip install django-gum

**2** Add "gum" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS += ('gum',)

**3** Add Elasticsearch configuration to your settings like this::

    GUM_ELASTICSEARCH_URLS = ["http://127.0.0.1:9200/"]
    GUM_ELASTICSEARCH_INDEX = ".gum-tests"

List of available configuration variables:

* ``GUM_DEBUG`` (boolean)
* ``GUM_USE_CELERY`` (boolean)
* ``GUM_ELASTICSEARCH_URLS`` (list)
* ``GUM_ELASTICSEARCH_INDEX`` (string)


**4** Create an index.py in your app, with a content like this::

    from gum.indexer import MappingType, indexer

    class PostMappingType(MappingType):

        def document(self, instance):
            tags_text = " ".join(map(lambda x: x.label, instance.tags.all()))
            return {
                "title": instance.title,
                "content": instance.content,
                "text": "{} {} {}".format(instance.title, instance.content, tags_text)
            }

        def mapping(self):
            return {
                "properties": {
                    "title": {
                        "type": "string",
                        "store": True,
                    },
                    "content": {
                        "type": "string",
                        "store": True,
                    },
                    "text": {
                        "type": "string",
                        "store": True,
                    }
                }
            }

    indexer.register(Post, PostMappingType)

**5** Update Elasticsearch index::

    ./manage.py gum --update-index

You can specify the models you want to index::

    ./manage.py gum --update-index blog.Post

Searching
---------

You can perform Elasticsearch searches (accessing ``search`` method) using ``elasticsearch`` model
attribute::

    response = Post.elasticsearch.search(body={
        "query": {
            "match_all": {}
        }
    })

