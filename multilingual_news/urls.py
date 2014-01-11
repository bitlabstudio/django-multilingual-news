"""URLs for the ``multilingual_news`` app."""
from django.conf.urls import patterns, url

from .models import NewsEntry
from .views import NewsDateDetailView, NewsDetailView, NewsListView


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]+)/$',
        NewsDateDetailView.as_view(),
        name='news_detail'),
    url(r'^(?P<slug>[\w-]+)/$',
        NewsDetailView.as_view(),
        name='news_detail'),
    url(r'^preview/(?P<slug>[\w-]+)/$',
        NewsDetailView.as_view(queryset=NewsEntry.objects.all()),
        name='news_preview'),
    url(r'^$',
        NewsListView.as_view(),
        name='news_list'),
)
