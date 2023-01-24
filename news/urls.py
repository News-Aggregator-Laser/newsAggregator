from django.urls import path
from .views import home, category, article

urlpatterns = [
    path("home/", home),
    path("category/<str:category>/", category),
    path("article/<int:article_id>/", article),
]
