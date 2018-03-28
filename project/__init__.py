# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

"""Entry point to all things to avoid circular imports."""
from project.app import app, freezer, pages
from project.views import *
