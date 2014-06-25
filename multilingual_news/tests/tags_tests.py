"""Tests for tags of the ``multilingual_news``` application."""
from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import add_plugin
from cms.models import Placeholder

from ..templatetags.multilingual_news_tags import (
    get_newsentry_meta_description,
    get_newsentry_meta_title,
    get_published_entries,
    get_recent_news,
)
from . import factories


class GetPublishedEntriesTestCase(TestCase):
    """Tests for the `get_published_entries` template tag."""
    longMessage = True

    def setUp(self):
        self.entry1 = factories.NewsEntryFactory(language_code='en')
        new_entry = self.entry1.translate('de')
        new_entry.title = 'GerTitle'
        new_entry.is_published = True
        new_entry.save()
        self.entry2 = factories.NewsEntryFactory(language_code='en')
        new_entry = self.entry2.translate('de')
        new_entry.title = 'GerTitle2'
        new_entry.is_published = False
        new_entry.save()

        self.object_list = [self.entry1, self.entry2]

    def test_tag(self):
        # retrieve the one german entry
        self.assertEqual(
            get_published_entries(self.object_list, 'de').count(),
            1, msg=('The tag should have returned only one entry.'))
        # retrieve the two english entries
        self.assertEqual(
            get_published_entries(self.object_list).count(),
            2, msg=('The tag should have returned two entries.'))


class GetNewsEntryMetaDescriptionTestCase(TestCase):
    """Tests for the `get_newsentry_meta_description` template tag."""
    longMessage = True

    def setUp(self):
        self.newsentry_with_meta = factories.NewsEntryFactory(
            meta_description='Meta Description')
        placeholder_excerpt = Placeholder.objects.create(
            slot='multilingual_news_excerpt')
        placeholder_content = Placeholder.objects.create(
            slot='multilingual_news_content')

        # adding two other plugins, to cause an exception, when trying to acces
        # the plugin.text attribute
        add_plugin(placeholder_excerpt, 'LinkPlugin', 'en')
        add_plugin(placeholder_content, 'LinkPlugin', 'en')

        # adding the correct plugins
        add_plugin(placeholder_excerpt, 'TextPlugin', 'en',
                   body='<p>Test excerpt</p>')
        add_plugin(placeholder_content, 'TextPlugin', 'en',
                   body=(
                       '<p>Test content - lorem ipsum longer than 160 chars'
                       ' to test the cropping and the appending of the dots,'
                       ' which happens only on very long descriptions.'
                       ' When will this become longer than 160?</p>'))

        self.newsentry_with_excerpt = factories.NewsEntryFactory()
        self.newsentry_with_excerpt.excerpt = placeholder_excerpt
        self.newsentry_with_excerpt.save()

        self.newsentry_with_content = factories.NewsEntryFactory()
        self.newsentry_with_content.content = placeholder_content
        self.newsentry_with_content.save()

    def test_tag(self):
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
        self.entry = factories.NewsEntryFactory(
            title='Title',
        )
        self.entry_with_meta = factories.NewsEntryFactory(
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
        self.news_entry = factories.NewsEntryFactory()
        self.category = factories.CategoryFactory()
        self.news_entry.categories.add(self.category)
        self.news_entry_2 = factories.NewsEntryFactory()
        factories.NewsEntryFactory()
        factories.NewsEntryFactory()

    def test_tag(self):
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
        self.news_entry_2.categories.add(self.category)
        result = get_recent_news(context, category=self.category.slug)
        self.assertEqual(result.count(), 2, msg=(
            'Should only return recent news from chosen category'))
