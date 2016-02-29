# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import time

import six
from django.core.management import call_command
from django.test import override_settings, TestCase
from model_mommy import mommy

from gum.indexer import indexer
from gum.tests.test_app.models import Post, Tag
from gum.tests.test_settings import TEST_SETTINGS
from gum.utils import elasticsearch_connection


@override_settings(**TEST_SETTINGS)
class GumTestBase(TestCase):

    def setUp(self):
        indexer.initialize_index()
        indexer.update_index()

    def tearDown(self):
        indexer.remove_index()

    def test_registered_models(self):
        registered_models = indexer.get_registered_models()
        self.assertTrue(Post in registered_models)
        self.assertFalse(Tag in registered_models)

    def test_mapping_created(self):
        es = elasticsearch_connection()
        mapping_type_name = Post.elasticsearch.mapping_type.get_type()
        response = es.indices.get_mapping(
            index=TEST_SETTINGS["GUM_ELASTICSEARCH_INDEX"],
            doc_type=mapping_type_name
        )
        self.assertDictEqual(
            response.get(TEST_SETTINGS["GUM_ELASTICSEARCH_INDEX"], {}).get("mappings"),
            Post.elasticsearch.mapping_type.mapping()
        )

    def test_update_index(self):
        number_of_posts = 5
        mommy.make("test_app.Post", _quantity=number_of_posts)
        self.assertEquals(Post.objects.count(), number_of_posts)
        # Index isn't available at this moment, we have to wait
        time.sleep(2)
        # Gets all indexed documents
        response = Post.elasticsearch.search(body={
            "query": {
                "match_all": {}
            }
        })
        self.assertEquals(response["hits"]["total"], number_of_posts)

    def test_delete_model(self):
        number_of_posts = 5
        mommy.make("test_app.Post", _quantity=number_of_posts)
        self.assertEquals(Post.objects.count(), number_of_posts)
        # Index isn't available at this moment, we have to wait
        time.sleep(2)
        # Delete a post
        post = Post.objects.all()[0]
        post.delete()
        time.sleep(2)
        # Gets all indexed documents
        response = Post.elasticsearch.search(body={
            "query": {
                "match_all": {}
            }
        })
        self.assertEquals(response["hits"]["total"], number_of_posts - 1)

    def test_command_gum(self):
        out = six.StringIO()
        call_command("gum", "--update-index", "test_app.Post", stdout=out)
        self.assertIn("Initializing index... OK", out.getvalue())
