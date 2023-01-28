import json

from news.models import Provider


def fill():
    if not Provider.objects.all():
        with open("DataFetcher/tasks/providers.json", "r") as file:
            data = json.load(file)
        for element in data:
            provider = Provider(host=element["host"], path=element["path"], token=element["token"], requests_nb=int(element["requestNb"]),
                                dataPath_map=element["mapping"]["dataPath"], title_map=element["mapping"]["title"],
                                subTitle_map=element["mapping"]["subTitle"], content_map=element["mapping"]["content"],
                                imageUrl_map=element["mapping"]["imageUrl"], provider_map=element["mapping"]["provider"],
                                publishedAt_map=element["mapping"]["publishedAt"], source_map=element["mapping"]["source"],
                                category_map=element["mapping"]["category"], author_map=element["mapping"]["author"])
            provider.save()
