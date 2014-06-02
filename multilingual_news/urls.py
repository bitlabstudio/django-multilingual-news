"""URLs for the ``multilingual_news`` app."""
from django.conf.urls import patterns, url

from .feeds import AuthorFeed, NewsEntriesFeed, TaggedFeed
from .models import NewsEntry
from . import views


urlpatterns = patterns(
    '',
    # feed urls
    url(r'^rss/any/tagged/(?P<tag>[^/]*)/$',
        TaggedFeed(), {'any_language': True},
        name='news_rss_any_tagged'),
    url(r'^rss/tagged/(?P<tag>[^/]*)/$',
        TaggedFeed(), name='news_rss_tagged'),
    url(r'^rss/any/author/(?P<author>\d+)/$',
        AuthorFeed(), {'any_language': True},
        name='news_rss_any_author'),
    url(r'^rss/author/(?P<author>\d+)/$',
        AuthorFeed(), name='news_rss_author'),
    url(r'^rss/any/$', NewsEntriesFeed(), {'any_language': True},
        name='news_rss_any'),
    url(r'^rss/$', NewsEntriesFeed(), name='news_rss'),

    # regular urls
    url(r'^category/(?P<category>[^/]*)/',
        views.CategoryListView.as_view(),
        name='news_archive_category',),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]+)/$',
        views.NewsDateDetailView.as_view(),
        name='news_detail'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.NewsDetailView.as_view(queryset=NewsEntry.objects.published()),
        name='news_detail'),
    url(r'^preview/(?P<slug>[\w-]+)/$',
        views.NewsDetailPreviewView.as_view(queryset=NewsEntry.objects.all()),
        name='news_preview'),
    url(r'^tag/(?P<tag>[\w-]+)$',
        views.TaggedNewsListView.as_view(),
        name='news_archive_tagged'),
    url(r'^delete-entry/(?P<pk>\d+)/',
        views.DeleteNewsEntryView.as_view(),
        name='news_delete',),
    url(r'^publish-entry/(?P<pk>\d+)/',
        views.PublishNewsEntryView.as_view(),
        name='news_publish',),
    url(r'^$',
        views.NewsListView.as_view(),
        name='news_list'),

    # AJAX views
    url(r'^get-entries/',
        views.GetEntriesAjaxView.as_view(),
        name='news_get_entries',),
)
