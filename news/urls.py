from django.urls import path
from .views import home, category, article, read_later, history, your_feed

urlpatterns = [
    path("", home),
    path("category/<str:category>/", category),
    path("article/<int:article_id>/", article),
    path("read_later/", read_later),
    path("history_list/", history),
    path("your_feed/", your_feed),
]
