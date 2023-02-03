import spacy
from news.models import News, Category, Tags
from time import time

CATEGORIES_MAP: dict[str, list[str]] = {
    # health wa 2a5awatouha
    "health": ["sports", "environment", "food"],
    "sports": ["health", "environment", "food"],
    "environment": ["sports", "health", "food"],
    "food": ["sports", "environment", "health"],
    # buisness wa 2a5awatouha
    "business": ["world", "technology", "politics"],
    "world": ["business", "technology", "politics"],
    "technology": ["business", "world", "politics"],
    "politics": ["business", "world", "technology"],
    # entertainment wa 2a5awatouha
    "entertainment": ["lifestyle", "travel", "fashion"],
    "lifestyle": ["entertainment", "travel", "fashion"],
    "travel": ["entertainment", "lifestyle", "fashion"],
    "fashion": ["entertainment", "lifestyle", "travel"],
    # tech wa 2a5awatouha
    "tech": ["science", "technology", "business"],
    "science": ["tech", "technology", "business"],
    "technology": ["tech", "science", "business"],
    "business": ["tech", "science", "technology"],
}


# ==================== Helpers ====================#
def _get_news_with_same_category(category: Category, limit: int = 10):
    news = News.objects.filter(news_category=category).order_by("-publish_date")
    try:
        return news[:limit]
    except IndexError:
        return news


def _get_category_from_name(category_name: str) -> "Category|None":
    try:
        return Category.objects.filter(name=category_name).first()
    except:
        return None


def _get_news_with_similar_tag(tag: Tags) -> list[News]:
    similar_tags = [
        t for t in Tags.objects.filter(tag__icontains=tag.tag) if t.id != tag.id
    ]
    return [News.objects.filter(id=sim_tag.news_id).first() for sim_tag in similar_tags]


# ==================== DS for News frequency ====================#
class NewsPreciser:
    def __init__(self) -> None:
        self._news = {}

    def add(self, news: News):
        if news in self._news:
            self._news[news] += 0.1
        else:
            self._news[news] = 0.1

    def get_sorted(self):
        return sorted(self._news.items(), key=lambda x: x[1], reverse=True)


# ==================== El Essa Kella ====================#
def generate_suggestions(history: list[News], limit: int = 20) -> list[News]:
    start = time()
    suggestions = NewsPreciser()

    for news in history:
        # --- (1) get news with the same category ---#
        for sim_news in _get_news_with_same_category(news.news_category, 10):
            if sim_news not in history:
                suggestions.add(sim_news)

        # --- (2) get news with similar category ---#
        category = news.news_category.name
        if category in CATEGORIES_MAP:
            for sim_cat_name in CATEGORIES_MAP[category]:
                sim_cat: Category | None = _get_category_from_name(sim_cat_name)
                if sim_cat is not None:
                    for sim_news in _get_news_with_same_category(sim_cat, 5):
                        if sim_news not in history:
                            suggestions.add(sim_news)

        # --- (3) get news with similar tags ---#
        news_tags = Tags.objects.filter(news_id=news.id)
        for tag in news_tags:
            for sim_news in _get_news_with_similar_tag(tag):
                if sim_news not in history:
                    suggestions.add(sim_news)

    # ----- output -----#
    for k, v in suggestions.get_sorted():
        title = k.title
        category = k.news_category
        print(f"[{category}] '{title[:7]}...{title[-10:-1]}': {v:.2f}")

    print("*" * 50)
    print(f"execution time: {time() - start}")
    print("*" * 50)
    try:
        return [n for n, _ in suggestions.get_sorted()][:limit]
    except IndexError:
        return [n for n, _ in suggestions.get_sorted()]
