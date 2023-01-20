import os
from threading import Thread

import schedule
from dotenv import load_dotenv

from DataFetcher.tasks.RequestProvider import RequestProvider
from DataFetcher.tasks.RequestProvidersScheduler import RequestProvidersScheduler
from shared.models import Provider

scheduler = RequestProvidersScheduler([])  # Add True For Debugging


def run():
    load_dotenv()
    news_api = []
    scheduler.running = True
    providers = Provider.objects.all()
    for provider in providers:
        if provider.is_active:
            news_api.append(RequestProvider(os.getenv(provider.host), os.getenv(provider.token), provider))
    scheduler.providers = news_api
    scheduler_thread = Thread(target=scheduler.run)
    scheduler_thread.start()


def stop():
    scheduler.stop()
    schedule.clear()
