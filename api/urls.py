from django.urls import path

from api.views import ReadLaterViewSet, HistoryViewSet, LikeViewSet, CommentViewSet, SubscriptionViewSet

urlpatterns = [
    path("read-later/", ReadLaterViewSet.as_view({"post": "create"})),
    path("read-later/<int:pk>", ReadLaterViewSet.as_view({"delete": "destroy"})),
    path("history/", HistoryViewSet.as_view({"post": "create"})),
    path("history/<int:pk>", HistoryViewSet.as_view({"delete": "destroy"})),
    path("like/", LikeViewSet.as_view({"post": "create"})),
    path("like/<int:pk>", LikeViewSet.as_view({"delete": "destroy"})),
    path("comment/", CommentViewSet.as_view({"post": "create"})),
    path("comment/<int:pk>", CommentViewSet.as_view({"delete": "destroy"})),
    path("subscription/", SubscriptionViewSet.as_view({"post": "create"})),
    path("subscription/<str:pk>", SubscriptionViewSet.as_view({"delete": "destroy"})),

]
