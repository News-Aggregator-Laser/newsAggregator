from django.urls import path
from .views import home, category, article, read_later, history, your_feed, favorite, registration, author, search

urlpatterns = [
    path("", home),
    path("category/<str:category>/", category),
    path("article/<int:article_id>/", article),
    path("author/<str:author>/", author),
    path("read_later/", read_later),
    path("history_list/", history),
    path("your_feed/", your_feed),
    path("favorite/", favorite),
    path("registration/", registration),
    path("search/", search)
]
