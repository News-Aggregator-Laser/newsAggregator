import spacy
from news.models import News
from time import time

nlp = spacy.load("en_core_web_md")

UNWANTED_LABELS = [
    "DATE",
    "MONEY",
    "CARDINAL",
    "PERCENT",
    "ORDINAL",
    "QUANTITY",
    "TIME",
    "ORG",
]


def extract_tags(text: str) -> set:
    results = [
        e.text.lower() for e in nlp(text).ents if e.label_ not in UNWANTED_LABELS
    ]
    return set(results)


distinct_labels = []


def _show_distinct_labels(text: str):
    for e in nlp(text).ents:
        if e.label_ not in distinct_labels:
            distinct_labels.append(e.label_)
            print(f"'{e.text}': {e.label_}")


def _show_all_labels(text: str):
    for e in nlp(text).ents:
        print(f"'{e.text}': {e.label_}")
