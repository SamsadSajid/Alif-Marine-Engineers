# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class OfficerConfig(AppConfig):
    name = 'officer'

    def ready(self):
        import officer.signals
