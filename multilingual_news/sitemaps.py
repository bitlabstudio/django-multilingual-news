"""Sitemaps for the `multilingual_news` app."""
from django.contrib.sitemaps import Sitemap
from .models import NewsEntry


class NewsSitemap(Sitemap):  # pragma: nocover
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return NewsEntry.objects.published()

    def lastmod(self, obj):
        return obj.pub_date
