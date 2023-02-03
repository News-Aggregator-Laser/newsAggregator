import spacy

nlp = spacy.load("en_core_web_md")


def extract_tags(text: str) -> set:
    return set(nlp(text).ents)
