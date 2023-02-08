"""
This scripts extract all news from database and generate tags for those which don't have any.
"""

import os

import django

from news.models import News, Tags

from ml_logic.tags_extractor import (
    extract_tags,
    _show_distinct_labels,
    _show_all_labels,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsAggregator.settings")

django.setup()


def show_distinct_labels(limit: int = 10):
    news = News.objects.all()[:limit]
    for n in news:
        _show_distinct_labels(n.title)
        _show_distinct_labels(n.subtitle)


def show_generated_tags(limit: int = 10):
    news = News.objects.all()[:limit]
    for n in news:
        print(f"- {n.id}:", end=" ")
        results_title = extract_tags(n.title)
        results_subtitle = extract_tags(n.subtitle)
        print(results_title.union(results_subtitle))


def show_all_labels(news_id: int):
    news = News.objects.filter(id=news_id).first()
    print(f"Labels of:\n\t'{news.title}'\n\t'{news.subtitle}':")
    _show_all_labels(news.title)
    _show_all_labels(news.subtitle)


def delete_all_existing_tags(are_you_suuuuure: bool):
    if are_you_suuuuure:
        inpt = input("Are you suuuuure? y/n: ")
        if inpt == "y":
            print("Deleting all tags...", end=" ")
            Tags.objects.all().delete()
            print("Done")


def generate_and_save_tags():
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


if __name__ == "__main__":
    # ----- To show all distinct labels -----#
    # show_distinct_labels(50)

    # ----- To show generated tags without modifying database -----#
    # show_generated_tags(50)

    # ----- To show all labels for a defined news  -----#
    # show_all_labels(6)

    # ----- Delete all existing Tags from DB  -----#
    # delete_all_existing_tags(are_you_suuuuure=True)

    # ----- Generate Tags for all existing News that does not have any -----#
    # generate_and_save_tags()

    pass
