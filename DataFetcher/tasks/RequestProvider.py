import json
import time
import ast
import requests
from django.db import IntegrityError
from jsonpath_ng import parse

from news.models import News, Provider, Category


def _parse_list_str(list_str: str) -> list[str]:
    lst = [category.strip() for category in ast.literal_eval(list_str)]
    if len(lst) == 0:
        lst = ["general"]
    if len(lst) > 1 and "general" in lst:
        lst.remove("general")
    return lst


class RequestProvider:
    def __init__(self, host: str, token: str, provider: Provider) -> None:
        self._host = host
        self._token = token
        self.provider = provider
        self.retries = 3
        self.sleep_time = 2  # in seconds

    def request(self):
        print("\tRequesting...")
        return requests.get(f"http://{self._host}{self.provider.path}{self._token}")

    def handle_error(self, response_code: int, response):
        """
        Handle errors
        """
        if 500 <= response_code < 600:
            for i in range(self.retries):
                # Retry the request
                print(f"Retrying request, attempt {i + 1} of {self.retries}...")
                response = self.request()
                if response.status_code != 200:
                    time.sleep(self.sleep_time)
                else:
                    self.handle_response(response.content)
                    return
            print("Error: Request failed after all retries.")
        else:
            # Handle other types of errors (e.g. client-side errors)
            print(f"Error: Request failed with response code {response_code}.")
            print(response)

    def run(self):
        response = self.request()
        if response.status_code != 200:
            self.handle_error(response.status_code, response.content)
        else:
            self.handle_response(response.content)

    def handle_response(self, response):
        print(self._host)
        print("\tHandling...")
        # print(f"{type(response) = }")
        # print(f"{len(response) = }")
        # print(response[0 : len(response) // 4])
        response = json.loads(response.decode())
        title_expr = parse("$.." + self.provider.title_map)
        sub_title_expr = parse("$.." + self.provider.subTitle_map)
        content_expr = parse("$.." + self.provider.content_map)
        url_to_image_expr = parse("$.." + self.provider.imageUrl_map)
        provider_expr = parse("$.." + self.provider.provider_map)
        published_at_expr = parse("$.." + self.provider.publishedAt_map)
        src_expr = parse("$.." + self.provider.source_map)
        category_expr = parse("$.." + self.provider.category_map)
        author_expr = parse("$.." + self.provider.author_map)

        def get_value(expr):
            try:
                return expr.find(new)[0].value
            except IndexError:
                return None

        for new in response[self.provider.dataPath_map]:
            title = get_value(title_expr)
            sub_title = get_value(sub_title_expr)
            content = get_value(content_expr)
            url_to_image = get_value(url_to_image_expr)
            provider = get_value(provider_expr)
            published_at = get_value(published_at_expr)
            src = get_value(src_expr)
            category = get_value(category_expr)

            # if category is literal list
            print(f"{type(category) = }")
            print(f"Category before: {category}")
            if not category:
                category = "general"

            elif type(category) is str and "[" in category:
                category = _parse_list_str(category)[0]

            elif type(category) is list:
                if len(category) > 1 and "general" in category:
                    category.remove("general")

                category = category[0]

            print(f"{category = }")
            author = get_value(author_expr)

            if not all((title, sub_title, content, url_to_image, published_at, src)):
                continue

            # try:
            #     news_source_m = NewsSource.objects.get(name=provider)
            # except NewsSource.DoesNotExist:
            #     news_source_m = NewsSource(name=provider)
            #     news_source_m.save()
            try:
                category_m = Category.objects.get(name=category)
            except Category.DoesNotExist:
                category_m = Category(name=category)
                category_m.save()
            # try:
            #     author_m = Author.objects.get(name=author)
            # except Author.DoesNotExist:
            #     author_m = Author(name=author)
            #     author_m.save()
            # try:
            #     category_m = Category.objects.get(name=category)
            # except Category.DoesNotExist:
            #     pass
            provider_m = Provider.objects.get(host=self.provider.host)
            news_m = News(
                title=title,
                subtitle=sub_title,
                content=content,
                url_image=url_to_image,
                news_provider=provider_m,
                publish_date=published_at,
                source=src,
                news_category=category_m,
                news_author=author,
                news_source=provider,
            )
            try:
                news_m.save()
            except IntegrityError:
                pass
