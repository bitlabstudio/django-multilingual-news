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
        new_entry = self.entry1.translate('de')
        new_entry.title = 'GerTitle'
        new_entry.is_published = True
        new_entry.save()
        self.entry2 = mixer.blend('multilingual_news.NewsEntry')
        new_entry = self.entry2.translate('de')
        new_entry.title = 'GerTitle2'
        new_entry.is_published = False
        new_entry.save()

        self.object_list = [self.entry1, self.entry2]

    def test_tag(self):
        activate('de')
        # retrieve the one german entry
        self.assertEqual(
            get_published_entries(self.object_list, 'de').count(),
            1, msg=('The tag should have returned only one entry.'))
        # retrieve the two english entries
        self.assertEqual(
            get_published_entries(self.object_list).count(),
            1, msg=('The tag should have returned one entry.'))


class GetNewsEntryMetaDescriptionTestCase(TestCase):
    """Tests for the `get_newsentry_meta_description` template tag."""
    longMessage = True

    def setUp(self):
        self.newsentry_with_meta = mixer.blend(
            'multilingual_news.NewsEntry')
        en_trans = self.newsentry_with_meta.translate('en')
        en_trans.meta_description = 'Meta Description'
        en_trans.save()

        self.newsentry_with_excerpt = mixer.blend(
            'multilingual_news.NewsEntry')
        self.newsentry_with_excerpt.translate('en')
        add_plugin(self.newsentry_with_excerpt.excerpt, 'LinkPlugin', 'en')
        add_plugin(self.newsentry_with_excerpt.excerpt, 'TextPlugin', 'en',
                   body='<p>Test excerpt</p>')

        self.newsentry_with_content = mixer.blend(
            'multilingual_news.NewsEntry')
        self.newsentry_with_content.translate('en')
        add_plugin(self.newsentry_with_content.content, 'LinkPlugin', 'en')
        add_plugin(self.newsentry_with_content.content, 'TextPlugin', 'en',
                   body=(
                       '<p>Test content - lorem ipsum longer than 160 chars'
                       ' to test the cropping and the appending of the dots,'
                       ' which happens only on very long descriptions.'
                       ' When will this become longer than 160?</p>'))

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
            'multilingual_news.NewsEntryTranslation',
            title='Title',
            master__author=mixer.blend('people.PersonTranslation'),
        )
        self.entry_with_meta = mixer.blend(
            'multilingual_news.NewsEntryTranslation',
            master__author=mixer.blend('people.PersonTranslation'),
            meta_title='Meta',
            title='Title2'
        )

    def test_tag(self):
        self.assertEqual(get_newsentry_meta_title(self.entry), 'Title')
        self.assertEqual(get_newsentry_meta_title(self.entry_with_meta),
                         'Meta')


class GetRecentNewsTestCase(TestCase):
    """Tests for the ``get_recent_news`` assignment tag."""
    longMessage = True

    def setUp(self):
        self.news_entry = mixer.blend('multilingual_news.NewsEntry')
        trans = self.news_entry.translate('en')
        trans.is_published = True
        trans.save()
        self.category = mixer.blend('multilingual_news.Category')
        self.news_entry.categories.add(self.category)

        self.news_entry2 = mixer.blend('multilingual_news.NewsEntry')
        trans = self.news_entry2.translate('en')
        trans.is_published = True
        trans.save()

        for x in range(0, 2):
            entry = mixer.blend('multilingual_news.NewsEntry')
            trans = entry.translate('en')
            trans.is_published = True
            trans.save()

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
