"""newsAggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db.models.signals import post_save
from django.urls import path, include

from DataFetcher.tasks import run, stop
from DataFetcher.tasks.ProviderFill import fill
from api.views import ReadLaterViewSet, HistoryViewSet
from news.models import Provider
from django.dispatch import receiver
from rest_framework import routers


# run()


# fill()


@receiver(post_save, sender=Provider)
def my_callback(sender, instance, created, **kwargs):
    stop()
    run()


# router = routers.DefaultRouter()
# router.register(r'read-later', ReadLaterViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-read-later/', ReadLaterViewSet.as_view({'post': 'create'})),
    path('create-history/', HistoryViewSet.as_view({'post': 'create'})),
    path('delete-history/<int:pk>', HistoryViewSet.as_view({'delete': 'update'})),
    path('delete-history/<int:pk>', HistoryViewSet.as_view({'delete': 'update'})),
]
