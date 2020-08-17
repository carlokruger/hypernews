from django.shortcuts import render
from django.views import View
import json
from hypernews.settings import NEWS_JSON_PATH
import datetime

# Create your views here.


with open(NEWS_JSON_PATH, "r") as json_file:
    news = json.load(json_file)


class IndexView(View):
    template_name = "news/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class NewsDetailView(View):
    template_name = "news/newsdetail.html"

    def get(self, request, *args, **kwargs):
        global news
        title = news[0]["title"]
        created = news[0]["created"]
        text = news[0]["text"]
        link = news[0]["link"]
        vars = {"title": title, "created": created, "text": text, "link": link }
        return render(request, self.template_name, vars)


class NewsView(View):
    template_name = "news/news.html"

    def get(self, request, *args, **kwargs):
        global news
        dates = []
        url_titles = []
        for datum in news:
            url_titles.append([datum["created"][:10], datum["link"], datum["title"]])
            if datum["created"][:10] not in dates:
                dates.append(datum["created"][:10])
        dates.sort(reverse=True)

        context = {"dates": dates, "data": url_titles}
        return render(request, self.template_name, context)
