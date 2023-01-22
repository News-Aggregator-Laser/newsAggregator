"""
WSGI config for newsAggregator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.cache import cache
from django.db.models.signals import post_save
from DataFetcher.tasks import run, stop
from DataFetcher.tasks.ProviderFill import fill
from news.models import Provider
from django.dispatch import receiver
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsAggregator.settings')
application = get_wsgi_application()
if not cache.get('function_has_run'):
    # fill()
    run()


    @receiver(post_save, sender=Provider)
    def my_callback(sender, instance, created, **kwargs):
        stop()
        run()


    cache.set('function_has_run', True, None)
