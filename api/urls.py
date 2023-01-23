from django.urls import path

from api.views import ReadLaterViewSet, HistoryViewSet

urlpatterns = [
    path('create-read-later/', ReadLaterViewSet.as_view({'post': 'create'})),
    path('create-history/', HistoryViewSet.as_view({'post': 'create'})),
    path('delete-read-later/<int:pk>', ReadLaterViewSet.as_view({'delete': 'update'})),
    path('delete-history/<int:pk>', HistoryViewSet.as_view({'delete': 'update'})),
]
