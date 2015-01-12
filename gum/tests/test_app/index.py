# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gum.indexer import MappingType, indexer
from gum.tests.test_app.models import Post


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
            self.get_type(): {
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
        }

indexer.register(Post, PostMappingType)
