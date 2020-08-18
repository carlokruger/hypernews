from django.shortcuts import render, redirect
from django.views import View
import json
from hypernews.settings import NEWS_JSON_PATH
import datetime

# Create your views here.

title = ""
created = ""
link = ""
text = ""


def getdetail(url_path):
    global title
    global created
    global link
    global text
    with open(NEWS_JSON_PATH, 'r') as json_db:
        news = json.load(json_db)
    for article in news:
        if article["link"] == url_path:
            title = article["title"]
            created = article["created"]
            text = article["text"]
            link = article["link"]

    return {"title": title, "created": created, "text": text, "link": link}


class IndexView(View):
    template_name = "news/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class NewsDetailView(View):
    template_name = "news/newsdetail.html"

    def get(self, request, *args, **kwargs):
        url_path = int(request.get_full_path()[6:].strip("/"))
        context = getdetail(url_path)

        return render(request, self.template_name, context)


class NewsView(View):
    template_name = "news/news.html"

    def get(self, request, *args, **kwargs):
        with open(NEWS_JSON_PATH, 'r') as json_db:
            news = json.load(json_db)
        dates = []
        url_titles = []
        for datum in news:
            url_titles.append([datum["created"][:10], datum["link"], datum["title"]])
            if datum["created"][:10] not in dates:
                dates.append(datum["created"][:10])
        dates.sort(reverse=True)

        context = {"dates": dates, "data": url_titles}
        return render(request, self.template_name, context)


class CreateArticleView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create_article.html')

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        text = request.POST['text']
        created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with open(NEWS_JSON_PATH, 'r') as json_db:
            json_data = json.load(json_db)
        last_id = max(i['link'] for i in json_data)
        new_id = last_id + 1
        new_record = {"created": created, "text": text, "title": title, "link": new_id}
        json_data.append(new_record)
        with open(NEWS_JSON_PATH, 'w') as json_db:  # clobber
            json.dump(json_data, json_db, indent=4)

        return redirect('/news/')