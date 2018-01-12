# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ElasticSearchConfig(AppConfig):
    name = 'elastic_search'

    def ready(self):
        import elastic_search.signals
