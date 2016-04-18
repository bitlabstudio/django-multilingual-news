"""Tests for tags of the ``multilingual_news``` sitemaps."""
from django.test import TestCase

from mixer.backend.django import mixer

from ..sitemaps import NewsSitemap


class NewsSitemapTestCase(TestCase):
    """Tests for the `NewsSitemap` sitemap."""
    longMessage = True

    def test_sitemap(self):
        news = mixer.blend('multilingual_news.NewsEntry')
        translation = news.translate('en')
        translation.is_published = True
        translation.save()
        sitemap = NewsSitemap()
        self.assertEqual(sitemap.items().count(), 1, msg=(
            'Should return one item.'))
        self.assertTrue(sitemap.lastmod(obj=news), msg=(
            'Should return the publication date of the news.'))
