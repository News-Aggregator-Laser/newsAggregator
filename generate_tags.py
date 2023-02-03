"""
This scripts extract all news from database and generate tags for those which don't have any.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsAggregator.settings")

import django

django.setup()

from news.models import News, Tags


from ml_logic.tags_extractor import extract_tags


if __name__ == "__main__":
    news = News.objects.all()
    for n in news:
        tags = Tags.objects.filter(news=n)
        if not tags:
            print(f"Generating tags for {n.id}: ")
            extracted_tags = extract_tags(n.title).union(extract_tags(n.subtitle))
            print(extracted_tags, end="... ")
            for tag in extracted_tags:
                Tags.objects.create(news=n, tag=tag)
            print("Done")
