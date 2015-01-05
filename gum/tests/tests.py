# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, override_settings
from gum.tests.test_settings import TEST_SETTINGS


@override_settings(**TEST_SETTINGS)
class GumTestBase(TestCase):
    pass
