from keybert import KeyBERT

kw_model = KeyBERT()


def extract_tags(text: str) -> set:
    return set(map(lambda t: t[0], kw_model.extract_keywords(text)))
