"""URLs for the ``multilingual_news`` app."""

from django.urls import re_path

from .feeds import AuthorFeed, NewsEntriesFeed, TaggedFeed
from .models import NewsEntry
from . import views


urlpatterns = [
    # feed urls
    re_path(
        r"^rss/any/tagged/(?P<tag>[^/]*)/$",
        TaggedFeed(),
        {"any_language": True},
        name="news_rss_any_tagged",
    ),
    re_path(r"^rss/tagged/(?P<tag>[^/]*)/$", TaggedFeed(), name="news_rss_tagged"),
    re_path(
        r"^rss/any/author/(?P<author>\d+)/$",
        AuthorFeed(),
        {"any_language": True},
        name="news_rss_any_author",
    ),
    re_path(r"^rss/author/(?P<author>\d+)/$", AuthorFeed(), name="news_rss_author"),
    re_path(
        r"^rss/any/$", NewsEntriesFeed(), {"any_language": True}, name="news_rss_any"
    ),
    re_path(r"^rss/$", NewsEntriesFeed(), name="news_rss"),
    # regular urls
    re_path(
        r"^category/(?P<category>[^/]*)/",
        views.CategoryListView.as_view(),
        name="news_archive_category",
    ),
    re_path(
        r"^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]+)/$",
        views.NewsDateDetailView.as_view(),
        name="news_detail",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/$",
        views.NewsDetailView.as_view(queryset=NewsEntry.objects.published()),
        name="news_detail",
    ),
    re_path(
        r"^preview/(?P<slug>[\w-]+)/$",
        views.NewsDetailPreviewView.as_view(queryset=NewsEntry.objects.all()),
        name="news_preview",
    ),
    re_path(
        r"^tag/(?P<tag>[\w-]+)$",
        views.TaggedNewsListView.as_view(),
        name="news_archive_tagged",
    ),
    re_path(
        r"^delete-entry/(?P<pk>\d+)/",
        views.DeleteNewsEntryView.as_view(),
        name="news_delete",
    ),
    re_path(
        r"^publish-entry/(?P<pk>\d+)/",
        views.PublishNewsEntryView.as_view(),
        name="news_publish",
    ),
    re_path(r"^$", views.NewsListView.as_view(), name="news_list"),
    # AJAX views
    re_path(
        r"^get-entries/",
        views.GetEntriesAjaxView.as_view(),
        name="news_get_entries",
    ),
]
