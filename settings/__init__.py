# your_project/__init__.py
from __future__ import absolute_import, unicode_literals

# Это позволяет работать Celery в Django
from .celery import app as celery_app

__all__ = ("celery_app",)
