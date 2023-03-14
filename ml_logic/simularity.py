from news.models import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta


def simularity_coefficient(news_to_check, recent_news):
    """Returns a simularity coefficient between two phrases.

    The simularity coefficient is a number between 0 and 1. 0 means the phrases

    are completely different, 1 means they are the same.

    """
    # Prepare the news data
    news_data = [
        {
            "id": news.id,
            "title": news.title,
            "subtitle": news.subtitle,
            "content": news.content,
            "news_category__name": news.news_category.name,
            "news_author__name": news.news_author.name,
        }
        for news in recent_news
    ]
    # Add the single_news object to the news data
    news_data.append(
        {
            "id": None,
            "title": news_to_check.title,
            "subtitle": news_to_check.subtitle,
            "content": news_to_check.content,
            "news_category__name": news_to_check.news_category.name,
            "news_author__name": news_to_check.news_author.name,
        }
    )
    # Convert the news data to a Pandas DataFrame
    df = pd.DataFrame(news_data)
    # Define the vectorizer
    vectorizer = TfidfVectorizer()
    # Extract the features
    df["concatenated_fields"] = df["title"].str.cat(
        df[["subtitle", "content", "news_category__name", "news_author__name"]], sep=" "
    )
    X = vectorizer.fit_transform(df["concatenated_fields"])
    # Compute the similarity matrix
    similarity = cosine_similarity(X)
    # Get the highest similarity coefficient
    n = len(recent_news)

    indices = similarity[n].argsort()[-1:-(n + 1):-1]
    highest_coefficient = similarity[n][indices]
    print(f"{highest_coefficient[1] = }")
    return highest_coefficient[1]
