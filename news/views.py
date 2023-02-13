from json import dumps

from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.urls import reverse

from ml_logic.suggestions_generator import generate_suggestions
from .models import *


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        # Call the parent form_valid method to perform the default action
        super().form_valid(form)
        try:
            action = str(self.request.POST.get('next')).split(';')[1]
            id = str(self.request.POST.get('next')).split(';')[2]
            if action == 'read_later':
                try:
                    read_later = ReadLater.objects.get(user=self.request.user, news_id=id)
                    read_later.is_removed = False
                    read_later.save()
                except ReadLater.DoesNotExist:
                    ReadLater.objects.create(user=self.request.user, news_id=id).save()
            elif action == 'like':
                try:
                    like = Like.objects.get(user=self.request.user, news_id=id)
                    like.is_removed = False
                    like.save()
                except Like.DoesNotExist:
                    Like.objects.create(user=self.request.user, news_id=id).save()
            elif action == 'comment':
                content = str(self.request.POST.get('next')).split(';')[3]
                Comment.objects.create(user=self.request.user, news_id=id, content=content).save()
        except IndexError:
            pass

        next_page = str(self.request.POST.get('next')).split(';')[0]
        # Return the desired redirect URL
        if next_page:
            return redirect(next_page)
        return redirect('/')


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
        "news_source": article.news_source.name,
        "readLater": article.readLater if article.readLater else False,
        "favorite": article.favorite if article.favorite else False,
    }


def _news_to_json(news) -> str:
    """encode the list of news to json (to parse it in client side)"""
    return dumps([_encode_article(article) for article in news])


def _get_recent_liked_news(user_id: int, limit: int = 10) -> list[News]:
    recent_liked_news = (
        News.objects.filter(like__user_id=user_id)
        .annotate(like_count=Count("like"))
        .order_by("-publish_date")
    )
    try:
        return recent_liked_news[:limit]
    except IndexError:
        return recent_liked_news


def _get_recent_news_from_history(user_id: int, limit: int = 10) -> list[News]:
    history = History.objects.filter(user_id=user_id).order_by("-time")
    news = [News.objects.filter(id=h.news_id).first() for h in history]
    try:
        return news[:limit]
    except IndexError:
        return news


# ==================== End Points ====================#


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


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
    if request.method == "POST":
        if request.user.is_anonymous:
            next_page = request.path + ';comment;' + str(article_id) + ';' + request.POST.get("comment")
            url = reverse('login') + '?next=' + next_page
            return redirect(url)
        comment = request.POST.get("comment")
        comment = Comment.objects.create(
            user=request.user, news_id=article_id, content=comment
        )
        comment.save()
        return redirect("/article/" + str(article_id))
    else:
        articles = News.objects.get(
            id=article_id,
            is_archived=False,
            news_author__is_active=True,
            news_source__is_active=True,
        )
        articles = _add_read_later_like_to_news([articles], request.user)[0]
        comments = (
            Comment.objects.filter(news_id=article_id)
            .values("id", "user__username", "content", "created_at")
            .order_by("-created_at")
        )
        for comment in comments:
            if (
                    request.user.is_authenticated
                    and request.user.username == comment["user__username"]
            ):
                comment["is_user_comment"] = True
            else:
                comment["is_user_comment"] = False

        return render(
            request,
            "article_details.html",
            {
                **_common_vars(request.user.is_anonymous),
                "article": articles,
                "page_url": request.build_absolute_uri(),
                "comments": comments,
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
                    "title": f"Results for '{search_query}'",
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
    recent_liked_news = _get_recent_liked_news(request.user.id, 20)
    history_news = _get_recent_news_from_history(request.user.id, 20)
    suggestions = generate_suggestions(list(recent_liked_news) + list(history_news), 20)

    if not suggestions:
        suggestions = (
            News.objects.all()
            .filter(
                is_archived=False,
                news_author__is_active=True,
                news_source__is_active=True,
            )
            .order_by("-publish_date")[:10]
        )
    return render(
        request,
        "news_list.html",
        {
            **_common_vars(request.user.is_anonymous),
            "news": _news_to_json(
                _add_read_later_like_to_news(suggestions, request.user)
            ),
            "title": "your feed",
        },
    )
