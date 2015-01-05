# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    tags = models.ManyToManyField("test_app.Tag")


class Tag(models.Model):
    label = models.CharField(max_length=128)