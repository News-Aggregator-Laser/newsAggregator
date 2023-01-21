import os
from threading import Thread

import schedule

from DataFetcher.tasks.RequestProvider import RequestProvider
from DataFetcher.tasks.RequestProvidersScheduler import RequestProvidersScheduler
from news.models import Provider

scheduler = RequestProvidersScheduler([], True)  # Add True For Debugging


def run():
    news_api = []
    scheduler.running = True
    providers = Provider.objects.all()
    for provider in providers:
        if provider.is_active:
            news_api.append(RequestProvider(provider.host, provider.token, provider))
    scheduler.providers = news_api
    scheduler_thread = Thread(target=scheduler.run)
    scheduler_thread.start()


def stop():
    scheduler.stop()
    schedule.clear()
