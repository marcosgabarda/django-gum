.. :changelog:

History
-------

2.0.2 (2016-12-15)
++++++++++++++++++

* Support for indexing several documents from a single instance.

2.0.1 (2016-08-30)
++++++++++++++++++

* Added ``update_all_types`` parameter to ``update_index`` method.

2.0.0 (2016-08-29)
++++++++++++++++++

* Django Gum now works with Elasticsearch 2.X

1.2.0 (2016-08-23)
++++++++++++++++++

* Added command to initialize index
* Change return value for ``gum.tasks.handle_save`` task

1.1.1 (2016-04-12)
++++++++++++++++++

* Fixed problem building connections cache key
* Updated documentation

1.1.0 (2016-04-05)
++++++++++++++++++

* Added ``urls`` attribute to ``MappingType`` to be able to custom urls of Elasticsearch servers
* Added ``GenericElasticsearchManager`` class to make queries without specific ``MappingType`` class


1.0.1 (2016-03-31)
++++++++++++++++++

* Fixed problem running --update-settings


1.0.0 (2016-03-24)
++++++++++++++++++

* New settings var for configure Elasticsearch connection.
* Better project structure for distribution.


1.0.0rc1 (2016-02-29)
+++++++++++++++++++++

* First release on PyPI.
