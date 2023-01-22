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
from django.urls import include
from django.urls import path

from api.views import ReadLaterViewSet, HistoryViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('create-read-later/', ReadLaterViewSet.as_view({'post': 'create'})),
    path('create-history/', HistoryViewSet.as_view({'post': 'create'})),
    path('delete-read-later/<int:pk>', ReadLaterViewSet.as_view({'delete': 'update'})),
    path('delete-history/<int:pk>', HistoryViewSet.as_view({'delete': 'update'})),
    path('', include('news.urls')),
]
