from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from json import dumps
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta


def authenticated_required(function=None, redirect_url="login"):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated, login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# ==================== Helpers ====================#
def _common_vars(is_anonymous) -> dict:
    return {
        "is_authenticated": not is_anonymous,
        "selected_categories": [
            CMS.objects.first().category1,
            CMS.objects.first().category2,
            CMS.objects.first().category3,
            CMS.objects.first().category4,
            CMS.objects.first().category5,
            CMS.objects.first().category6,
        ],
        "all_categories": Category.objects.all().filter(is_active=True),
        "cms": {
            "logo": "../" + str(CMS.objects.first().logo),
            "title": CMS.objects.first().footer_title,
            "description": CMS.objects.first().footer_description,
            "facebook": CMS.objects.first().facebook_url,
            "instagram": CMS.objects.first().instagram_url,
            "twitter": CMS.objects.first().twitter_url,
        },
    }


def _add_read_later_like_to_news(news, user):
    # if user is not authenticated
    if user.is_anonymous:
        for article in news:
            article.readLater = False
            article.favorite = False
        return news

    # if user is authenticated
    for article in news:
        try:
            read_later = ReadLater.objects.get(user=user, news=article)
            article.readLater = not read_later.is_removed
        except ReadLater.DoesNotExist:
            article.readLater = False

        try:
            like = Like.objects.get(user=user, news=article)
            article.favorite = not like.is_removed
        except Like.DoesNotExist:
            article.favorite = False
    return news


def _encode_article(article: News) -> dict:
    """encode article to dict (to be compatible with JSON serialize)"""
    return {
        "id": article.id,
        "title": article.title,
        "subtitle": article.subtitle,
        "content": article.content,
        "publish_date": str(article.publish_date),
        "url_image": article.url_image,
        "news_category": article.news_category.name,
        "news_author": article.news_author.name,
        "readLater": article.readLater if article.readLater else False,
        "favorite": article.favorite if article.favorite else False,
    }


def _news_to_json(news) -> str:
    """encode the list of news to json (to parse it in client side)"""
    return dumps([_encode_article(article) for article in set(news)])


# ==================== End Points ====================#

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    common_vars = _common_vars(request.user.is_anonymous)
    # top news (for main slider)
    top_news = (
        News.objects.all()
        .filter(
            is_archived=False, news_author__is_active=True, news_source__is_active=True
        )
        .order_by("-publish_date")[:10]
    )
    # top news in each selected category
    top_categories_news = {
        category: News.objects.filter(
            is_top_in_category=True,
            news_category=category,
            is_archived=False,
            news_author__is_active=True,
            news_source__is_active=True,
        )
        for category in common_vars["selected_categories"]
    }
    popular_news = (
        News.objects.all()
        .filter(
            is_archived=False, news_author__is_active=True, news_source__is_active=True
        )
        .order_by("-publish_date")[:10]
    )
    popular_news = _add_read_later_like_to_news(popular_news, request.user)
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
    category_news = News.objects.filter(
        news_category=Category.objects.get(name=category),
        is_archived=False,
        news_author__is_active=True,
        news_source__is_active=True,
    )[:20]
    category_news = _add_read_later_like_to_news(category_news, request.user)
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "category": category,
            "news": _news_to_json(category_news),
            "title": category + " News",
        },
    )


def author(request, author: str):
    author_news = News.objects.filter(
        news_author=Author.objects.get(name=author),
        is_archived=False,
        news_author__is_active=True,
        news_source__is_active=True,
    )[:20]
    category_news = _add_read_later_like_to_news(author_news, request.user)
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "category": author,
            "news": _news_to_json(category_news),
            "title": author + " News",
        },
    )


def article(request, article_id: int):
    articles = News.objects.get(
        id=article_id,
        is_archived=False,
        news_author__is_active=True,
        news_source__is_active=True,
    )
    return render(
        request,
        "article_details.html",
        {
            **_common_vars(request.user.is_anonymous),
            "article": articles,
            "page_url": request.build_absolute_uri(),
        },
    )


@authenticated_required
def read_later(request):
    read_later = ReadLater.objects.filter(
        user=request.user,
        is_removed=False,
        news__is_archived=False,
        news__news_author__is_active=True,
        news__news_source__is_active=True,
    ).values_list("news_id", flat=True)
    read_later_news = News.objects.filter(id__in=read_later)
    _add_read_later_like_to_news(read_later_news, request.user)
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "news": _news_to_json(read_later_news),
            "title": "Read Later",
        },
    )


@authenticated_required
def history(request):
    history = History.objects.filter(
        user=request.user,
        is_removed=False,
        news__is_archived=False,
        news__news_author__is_active=True,
        news__news_source__is_active=True,
    ).values_list("news_id", flat=True)
    history_news = News.objects.filter(id__in=history)
    history_news = _add_read_later_like_to_news(history_news, request.user)
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "news": _news_to_json(history_news),
            "title": "History",
        },
    )


@authenticated_required
def favorite(request):
    favorite = Like.objects.filter(
        user=request.user,
        is_removed=False,
        news__is_archived=False,
        news__news_source__is_active=True,
        news__news_author__is_active=True,
    ).values_list("news_id", flat=True)
    favorite_news = News.objects.filter(id__in=favorite)
    favorite_news = _add_read_later_like_to_news(favorite_news, request.user)
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "news": _news_to_json(favorite_news),
            "title": "Favorite",
        },
    )


def search(request):
    if request.method == "GET":
        search_query = request.GET.get("q")
        if search_query:
            search_results = News.objects.filter(
                Q(title__icontains=search_query)
                | Q(subtitle__icontains=search_query)
                | Q(content__icontains=search_query),
                is_archived=False,
                news_author__is_active=True,
                news_source__is_active=True,
            )[:20]
            search_results = _add_read_later_like_to_news(search_results, request.user)
            return render(
                request,
                "news_list.html",
                {
                    **_common_vars(request.user.is_anonymous),
                    "news": _news_to_json(search_results),
                    "title": "Search Results",
                },
            )
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "news": [],
            "title": "Search Results",
        },
    )


@authenticated_required
def your_feed(request):
    recent_liked_news = (
        News.objects.filter(like__user_id=request.user.id)
        .annotate(like_count=Count("like"))
        .order_by("-publish_date")[:5]
    )
    recent_unliked_news = (
        News.objects.exclude(like__user_id=request.user.id)
        .filter(history__user=request.user.id)
        .order_by("-publish_date")[:5]
    )
    recent_news_set = recent_liked_news | recent_unliked_news
    # Load the data
    ten_days_ago = datetime.now() - timedelta(days=1000)
    news_data = News.objects.filter(publish_date__gt=ten_days_ago).values(
        "id", "title", "subtitle", "content", "news_category__name", "news_author__name"
    )
    df = pd.DataFrame.from_records(news_data)
    # Define the vectorizer
    vectorizer = TfidfVectorizer()
    # Extract the features
    df["concatenated_fields"] = df["title"].str.cat(
        df[["subtitle", "content", "news_category__name", "news_author__name"]], sep=" "
    )
    X = vectorizer.fit_transform(df["concatenated_fields"])
    # Compute the similarity matrix
    similarity = cosine_similarity(X)
    # Get recommendations for a news article
    news_set = News.objects.none()
    for news_recent_item in recent_news_set:
        indices = similarity[news_recent_item.id - 1].argsort()[-10:][::-1]
        for i in indices:
            similarity_coefficient = similarity[news_recent_item.id - 1][i]
            if similarity_coefficient > 0.1:
                print(
                    "Similarity between feature vectors",
                    news_recent_item.id - 1,
                    "and",
                    i,
                    "is:",
                    similarity_coefficient,
                )
                rec = df.iloc[i]["title"]
                news_set = news_set | News.objects.filter(title=rec)

    recommended_news_set = news_set.difference(recent_news_set)
    recommended_news_set = _add_read_later_like_to_news(
        recommended_news_set, request.user
    )
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "news": _news_to_json(recommended_news_set),
            "title": "your feed",
        },
    )
