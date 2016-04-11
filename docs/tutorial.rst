.. _ref-tutorial:

===============
Getting Started
===============


Installation
============

Use your PyPI to install the app::

    pip install django-gum


Configuration
=============

Add Gum to ``INSTALLED_APPS``
-----------------------------

As with most Django applications, you should add Gum to the
``INSTALLED_APPS`` within your settings file (usually ``settings.py``).

Example::

    INSTALLED_APPS += ('gum',)


Modify your ``settings.py``
---------------------------

You have to add to your settings file where is the Elasticsearch server you
want to use and which'll be the default index.

Example::

    GUM_ELASTICSEARCH_URLS = ["http://127.0.0.1:9200/"]
    GUM_ELASTICSEARCH_INDEX = ".gum-tests"


Handling data
=============

Linking models and mapping
--------------------------

Each model have to has a `Mapping Type <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-type>`_ associated
whit it. To do this, you have to create an ``index.py`` file inside your app and create a ``MappingType`` class, and
register this class with the model.

Example::

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


Updating index
--------------

You can use this command to update all registers models::

    ./manage.py gum --update-index

Or you can only update specified models::

    ./manage.py gum --update-index blog.Post

Making queries
--------------

You can perform Elasticsearch searches (accessing ``search`` method) using ``elasticseaech`` model
attribute.

Example::

    response = Post.elasticsearch.search(body={
        "query": {
            "match_all": {}
        }
    })

