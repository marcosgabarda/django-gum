# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import time

import datetime
import six
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import override_settings, TestCase
from model_mommy import mommy

from gum import get_version, get_git_changeset
from gum.indexer import indexer
from gum.managers import GenericElasticsearchManager
from gum.tasks import handle_save, handle_delete
from gum.tests.test_app.models import Post, Tag, Comment, CommentThread
from gum.tests.test_settings import TEST_SETTINGS, TASKS_TEST_SETTINGS
from gum.utils import elasticsearch_connection


class GumTestBase(TestCase):

    def setUp(self):
        indexer.initialize_index()
        indexer.update_index()

    def tearDown(self):
        indexer.remove_index()


@override_settings(**TEST_SETTINGS)
class GumTest(GumTestBase):

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
        time.sleep(5)
        # Gets all indexed documents
        response = Post.elasticsearch.search(body={
            "query": {
                "match_all": {}
            }
        })
        self.assertEquals(response["hits"]["total"], number_of_posts)

    def test_update_bulk_index(self):
        post = mommy.make("test_app.Post")
        thread = mommy.make("test_app.CommentThread", post=post)
        number_of_comments = 5
        mommy.make("test_app.Comment", thread=thread, _quantity=number_of_comments)
        thread.save()
        self.assertEquals(Comment.objects.count(), number_of_comments)
        self.assertEquals(thread.comments.count(), number_of_comments)
        # Index isn't available at this moment, we have to wait
        time.sleep(5)
        # Gets all indexed documents
        response = CommentThread.elasticsearch.search(body={
            "query": {
                "filtered": {
                    "filter": {
                        "term": {"thread_id": thread.pk}
                    },
                    "query": {
                        "match_all": {}
                    }
                }
            }
        })
        self.assertEquals(response["hits"]["total"], number_of_comments)

    def test_delete_model(self):
        number_of_posts = 5
        mommy.make("test_app.Post", _quantity=number_of_posts)
        self.assertEquals(Post.objects.count(), number_of_posts)
        # Index isn't available at this moment, we have to wait
        time.sleep(5)
        # Delete a post
        post = Post.objects.all()[0]
        post.delete()
        time.sleep(5)
        # Gets all indexed documents
        response = Post.elasticsearch.search(body={
            "query": {
                "match_all": {}
            }
        })
        self.assertEquals(response["hits"]["total"], number_of_posts - 1)

    def test_command_gum_update_index(self):
        out = six.StringIO()
        call_command("gum", "--update-index", "test_app.Post", stdout=out)
        self.assertIn("Initializing index... OK", out.getvalue())

    def test_command_gum_update_settings(self):
        out = six.StringIO()
        call_command("gum", "--update-settings", stdout=out)
        self.assertIn("Updating index settings...  OK", out.getvalue())

    def test_alternative_connection(self):
        from django.conf import settings
        self.assertIsNotNone(settings.GUM_ELASTICSEARCH_URLS_ALT)
        elasticsearch = GenericElasticsearchManager(urls=settings.GUM_ELASTICSEARCH_URLS_ALT)
        self.assertIsInstance(elasticsearch, GenericElasticsearchManager)
        query = {"query": {"match_all": {}}}
        results = elasticsearch.search(index="_all", doc_type="", body=query)
        self.assertIn("hits", results)


@override_settings(**TASKS_TEST_SETTINGS)
class GumTasksTest(GumTestBase):

    def test_task_handle_save(self):
        number_of_posts = 5
        mommy.make("test_app.Post", _quantity=number_of_posts)
        self.assertEquals(Post.objects.count(), number_of_posts)
        # Check there is no indexed documents
        response = Post.elasticsearch.search(body={
            "query": {
                "match_all": {}
            }
        })
        self.assertEquals(response["hits"]["total"], 0)
        # Launch task...
        content_type = ContentType.objects.get_for_model(Post.objects.first())
        for post in Post.objects.all():
            handle_save(sender_content_type_pk=content_type.pk, instance_pk=post.pk)
        time.sleep(5)
        # Gets all indexed documents
        response = Post.elasticsearch.search(body={
            "query": {
                "match_all": {}
            }
        })
        self.assertEquals(response["hits"]["total"], number_of_posts)

    def test_task_handle_delete(self):
        self.test_task_handle_save()
        # Launch task...
        content_type = ContentType.objects.get_for_model(Post.objects.first())
        for post in Post.objects.all():
            handle_delete(sender_content_type_pk=content_type.pk, instance_pk=post.pk)
        time.sleep(5)
        # Gets all indexed documents
        response = Post.elasticsearch.search(body={
            "query": {
                "match_all": {}
            }
        })
        self.assertEquals(response["hits"]["total"], 0)


class GumVersionTest(TestCase):

    def test_version(self):
        version = get_version(version=(1, 0, 0, 'final', 0))
        self.assertEquals(version, "1.0")
        version = get_version(version=(1, 1, 0, 'final', 0))
        self.assertEquals(version, "1.1")
        version = get_version(version=(1, 1, 1, 'final', 0))
        self.assertEquals(version, "1.1.1")

    def test_git_changeset(self):
        version = get_git_changeset()
        self.assertIsNotNone(version)
