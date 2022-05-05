"""Tests for tags of the ``multilingual_news``` application."""
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.translation import activate

from cms.api import add_plugin
from mixer.backend.django import mixer

from ..templatetags.multilingual_news_tags import (
    get_newsentry_meta_description,
    get_newsentry_meta_title,
    get_published_entries,
    get_recent_news,
)


class GetPublishedEntriesTestCase(TestCase):
    """Tests for the `get_published_entries` template tag."""
    longMessage = True

    def setUp(self):
        self.entry1 = mixer.blend('multilingual_news.NewsEntry')
        self.entry1.set_current_language('de')
        self.entry1.title = 'GerTitle'
        self.entry1.is_published = True
        self.entry1.save()
        self.entry2 = mixer.blend('multilingual_news.NewsEntry')
        self.entry2.set_current_language('de')
        self.entry2.title = 'GerTitle2'
        self.entry2.is_published = False
        self.entry2.save()

        self.object_list = [self.entry1, self.entry2]

    def test_tag(self):
        activate('de')
        # retrieve the one german entry
        self.assertEqual(
            get_published_entries(self.object_list, 'de').count(),
            1, msg='The tag should have returned only one entry.')
        # retrieve the two english entries
        self.assertEqual(
            get_published_entries(self.object_list).count(), 1, msg='The tag should have returned one entry.')


class GetNewsEntryMetaDescriptionTestCase(TestCase):
    """Tests for the `get_newsentry_meta_description` template tag."""
    longMessage = True

    def setUp(self):
        self.newsentry_with_meta = mixer.blend('multilingual_news.NewsEntry')
        self.newsentry_with_meta.set_current_language('en')
        self.newsentry_with_meta.meta_description = 'Meta Description'
        self.newsentry_with_meta.save()

        self.newsentry_with_excerpt = mixer.blend('multilingual_news.NewsEntry')
        self.newsentry_with_excerpt.set_current_language('en')
        self.newsentry_with_excerpt.meta_description = ''
        add_plugin(self.newsentry_with_excerpt.excerpt, 'LinkPlugin', 'en')
        add_plugin(self.newsentry_with_excerpt.excerpt, 'TextPlugin', 'en', body='<p>Test excerpt</p>')
        self.newsentry_with_excerpt.save()

        self.newsentry_with_content = mixer.blend('multilingual_news.NewsEntry')
        self.newsentry_with_content.set_current_language('en')
        self.newsentry_with_content.meta_description = ''
        add_plugin(self.newsentry_with_content.content, 'LinkPlugin', 'en')
        add_plugin(self.newsentry_with_content.content, 'TextPlugin', 'en',
                   body=(
                       '<p>Test content - lorem ipsum longer than 160 chars'
                       ' to test the cropping and the appending of the dots,'
                       ' which happens only on very long descriptions.'
                       ' When will this become longer than 160?</p>'))
        self.newsentry_with_content.save()

    def test_tag(self):
        activate('en')
        self.assertEqual(
            get_newsentry_meta_description(self.newsentry_with_meta),
            'Meta Description',
        )
        self.assertEqual(
            get_newsentry_meta_description(self.newsentry_with_excerpt),
            'Test excerpt',
            msg='Should have returned the content of the excerpt placeholder.',
        )
        self.assertIn(
            'Test content',
            get_newsentry_meta_description(self.newsentry_with_content),
            msg='Should have returned the content of the content placeholder.',
        )
        self.assertIn(
            '...',
            get_newsentry_meta_description(self.newsentry_with_content),
            msg='Should have appended "...".',
        )


class GetNewsEntryMetaTitleTestCase(TestCase):
    """Tests for the `get_newsentry_meta_title` template tag."""
    longMessage = True

    def setUp(self):
        self.entry = mixer.blend(
            'multilingual_news.NewsEntry',
            author=mixer.blend('people.Person'),
        )
        self.entry.set_current_language('en')
        self.entry.title = 'Title'
        self.entry.save()
        self.entry_with_meta = mixer.blend(
            'multilingual_news.NewsEntry',
            author=mixer.blend('people.Person'),
        )
        self.entry_with_meta.set_current_language('en')
        self.entry_with_meta.meta_title = 'Meta'
        self.entry_with_meta.title = 'Title2'
        self.entry_with_meta.save()

    def test_tag(self):
        self.assertEqual(get_newsentry_meta_title(self.entry), 'Title')
        self.assertEqual(get_newsentry_meta_title(self.entry_with_meta), 'Meta')


class GetRecentNewsTestCase(TestCase):
    """Tests for the ``get_recent_news`` assignment tag."""
    longMessage = True

    def setUp(self):
        self.news_entry = mixer.blend('multilingual_news.NewsEntry')
        self.news_entry.set_current_language('en')
        self.news_entry.is_published = True
        self.news_entry.save()
        self.category = mixer.blend('multilingual_news.Category')
        self.news_entry.categories.add(self.category)

        self.news_entry2 = mixer.blend('multilingual_news.NewsEntry')
        self.news_entry2.set_current_language('en')
        self.news_entry2.is_published = True
        self.news_entry2.save()

        for x in range(0, 2):
            entry = mixer.blend('multilingual_news.NewsEntry')
            entry.set_current_language('en')
            entry.is_published = True
            entry.save()

    def test_tag(self):
        activate('en')
        req = RequestFactory().get('/')
        context = {'request': req, }
        result = get_recent_news(context)
        self.assertEqual(result.count(), 3, msg=(
            'Should return last three recent news'))
        result = get_recent_news(context, category='foo')
        self.assertEqual(result.count(), 3, msg=(
            'Should return last three recent news, if category is invalid.'))
        result = get_recent_news(context, category=self.category.slug)
        self.assertEqual(result.count(), 1, msg=(
            'Should only return recent news from chosen category'))
        self.news_entry2.categories.add(self.category)
        result = get_recent_news(context, category=self.category.slug)
        self.assertEqual(result.count(), 2, msg=(
            'Should only return recent news from chosen category'))
