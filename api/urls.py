from django.urls import path

from api.views import ReadLaterViewSet, HistoryViewSet

urlpatterns = [
    path('read-later/', ReadLaterViewSet.as_view({'post': 'create'})),
    path('history/', HistoryViewSet.as_view({'post': 'create'})),
    path('read-later/<int:pk>', ReadLaterViewSet.as_view({'delete': 'destroy'})),
    path('history/<int:pk>', HistoryViewSet.as_view({'delete': 'destroy'})),
]
