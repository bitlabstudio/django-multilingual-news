from django.shortcuts import render

from cms.app_base import CMSAppConfig

from . import models


def render_newsentry(request, newsentry):
    if hasattr(request, "toolbar"):
        request.toolbar.set_object(newsentry)
    context = {
        "object": newsentry,
        "news_entry": newsentry,
        "detail_view": True,
    }
    return render(request, "multilingual_news/newsentry_detail.html", context)


class MultilingualNewsCMSConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_enabled_models = [(models.NewsEntry, render_newsentry)]
