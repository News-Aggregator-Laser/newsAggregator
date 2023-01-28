"""
WSGI config for newsAggregator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from threading import Thread

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.wsgi import get_wsgi_application

from scheduled_services import ScheduledServices
from news.models import Provider

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsAggregator.settings")
application = get_wsgi_application()


scheduled_services = ScheduledServices()
scheduler_thread = Thread(target=scheduled_services.run)
scheduler_thread.start()


@receiver(post_save, sender=Provider)
def my_callback(sender, instance, created, **kwargs):
    scheduled_services.restart()


# =============== OLD (Lal taware2) =============== #
# if not cache.get("function_has_run"):
#     fill()
#     print("Here is reached...")
#     data_fetcher_thread = Thread(target=run_data_fetcher)
#     data_fetcher_thread.start()

#     scheduled_services_thread = Thread(target=start_scheduled_services)
#     scheduled_services_thread.start()

#     #! Not sure that this will works on multi threading
#     @receiver(post_save, sender=Provider)
#     def my_callback(sender, instance, created, **kwargs):
#         stop_data_fetcher()
#         run_data_fetcher()

#     cache.set("function_has_run", True, None)
# ============================================ #
