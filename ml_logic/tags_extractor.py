import spacy
from news.models import News
from time import time

nlp = spacy.load("en_core_web_md")


def extract_tags(text: str) -> set:
    return set(nlp(text).ents)
