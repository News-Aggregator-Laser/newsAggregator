# import os
# from threading import Thread

# import schedule

# from .RequestProvider import RequestProvider
# from .RequestProvidersScheduler import RequestProvidersScheduler
# from .ProviderFill import fill
# from news.models import Provider

# scheduler = RequestProvidersScheduler([], True)  # Add True For Debugging


# def run():
#     fill()
#     news_api = []
#     scheduler.running = True
#     providers = Provider.objects.all()
#     for provider in providers:
#         if provider.is_active:
#             news_api.append(RequestProvider(provider.host, provider.token, provider))
#     scheduler.providers = news_api
#     scheduler.run()


# def stop():
#     scheduler.stop()
#     schedule.clear()
