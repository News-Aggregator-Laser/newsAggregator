from django.shortcuts import render
from .models import *

# Create your views here.
def _common_vars() -> dict:
    return {
        "is_authenticated": True,
        "selected_categories": [
            CMS.objects.first().category1,
            CMS.objects.first().category2,
            CMS.objects.first().category3,
            CMS.objects.first().category4,
            CMS.objects.first().category5,
            CMS.objects.first().category6,
        ],
        "all_categories": Category.objects.all(),
    }


def home(request):
    common_vars = _common_vars()
    # top news (for main slider)
    top_news = News.objects.all().order_by("-publish_date")[:10]
    # top news in each selected category
    top_categories_news = {
        category: News.objects.filter(is_top_in_category=True, news_category=category)
        for category in common_vars["selected_categories"]
    }
    popular_news = News.objects.all().order_by("-publish_date")[:10]
    return render(
        request,
        "index.html",
        {
            **common_vars,
            "top_news": top_news,
            "top_categories_news": top_categories_news,
            "popular_news": popular_news,
        },
    )


def category(request, category: str):
    return render(
        request,
        "category_news.html",
        {
            **_common_vars(),
            "category": category,
            "category_news": News.objects.filter(
                news_category=Category.objects.get(name=category)
            ),
        },
    )
