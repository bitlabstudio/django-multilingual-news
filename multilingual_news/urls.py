"""URLs for the ``multilingual_news`` app."""
from django.conf.urls import patterns, url

from .views import NewsDateDetailView, NewsDetailView, NewsListView


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d+)/(?P<month>[-\w]+)/(?P<day>\d+)/(?P<slug>[\w-]+)/$',
        NewsDateDetailView.as_view(),
        name="news_detail"),
    url(r'^(?P<slug>[\w-]+)/$',
        NewsDetailView.as_view(),
        name="news_detail"),
    url(r'^$',
        NewsListView.as_view(),
        name='news_list'),
)
