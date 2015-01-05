# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gum.indexer import MappingType, indexer


class PostMappingType(MappingType):

    def document(self, instance):
        return {
            "title": instance.title,
            "content": instance.content,
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
            }
        }

indexer.register()
