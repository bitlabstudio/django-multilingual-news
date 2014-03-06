"""Tests for the news feeds of the `multilingual_news` app."""
from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import NoReverseMatch

# Note: The feeds can't be tested with the ViewRequestFactoryTestMixin
from django_libs.tests.mixins import ViewTestMixin
from multilingual_tags.tests.factories import TaggedItemFactory
from people.tests.factories import PersonFactory

from . import factories

# the key part is only, that the LocaleMiddleware must be taken out.
NON_MULTILINGUAL_MIDDLWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)


class NewsEntriesFeedTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsEntriesFeed`` view class."""

    def setUp(self):
        factories.NewsEntryFactory()

    def get_view_name(self):
        return 'news_rss'

    def test_view_multilingual(self):
        self.is_callable()

    @override_settings(MIDDLEWARE_CLASSES=NON_MULTILINGUAL_MIDDLWARE_CLASSES)
    def test_view(self):
        self.is_callable()


class NewsEntriesFeedAnyLanguageTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsEntriesFeed`` view class."""

    def setUp(self):
        factories.NewsEntryFactory()

    def get_view_name(self):
        return 'news_rss_any'

    def get_view_kwargs(self):
        return {'any_language': True}

    def test_view(self):
        self.is_callable()


class AuthorFeedTestCase(ViewTestMixin, TestCase):
    """Tests for the ``AuthorFeed`` view class."""

    def setUp(self):
        factories.NewsEntryFactory()
        self.author = PersonFactory()

    def get_view_kwargs(self):
        # TODO ID is no pretty solution
        return {'author': self.author.id}

    def get_view_name(self):
        return 'news_rss_author'

    def test_view_multilingual(self):
        self.is_callable()

    @override_settings(MIDDLEWARE_CLASSES=NON_MULTILINGUAL_MIDDLWARE_CLASSES)
    def test_view(self):
        self.is_callable()


class AuthorFeedAnyLanguageTestCase(ViewTestMixin, TestCase):
    """Tests for the ``AuthorFeed`` view class."""

    def setUp(self):
        factories.NewsEntryFactory()
        self.author = PersonFactory()

    def get_view_name(self):
        return 'news_rss_any_author'

    def get_view_kwargs(self):
        # TODO ID is no pretty solution
        return {'author': self.author.id, 'any_language': True}

    def test_view(self):
        self.is_callable()

    def test_author_does_not_exist(self):
        self.author.delete()
        self.assertRaises(NoReverseMatch, self.is_callable)


class TaggedFeedTestCase(ViewTestMixin, TestCase):
    """Tests for the ``TaggedFeed`` view class."""

    def setUp(self):
        entry = factories.NewsEntryFactory()
        self.tagged_item = TaggedItemFactory(object=entry)

    def get_view_kwargs(self):
        return {'tag': self.tagged_item.tag.slug}

    def get_view_name(self):
        return 'news_rss_tagged'

    def test_view_multilingual(self):
        self.is_callable()

    @override_settings(MIDDLEWARE_CLASSES=NON_MULTILINGUAL_MIDDLWARE_CLASSES)
    def test_view(self):
        self.is_callable()


class TaggedFeedAnyLanguageTestCase(ViewTestMixin, TestCase):
    """Tests for the ``TaggedFeed`` view class."""

    def setUp(self):
        entry = factories.NewsEntryFactory()
        self.tagged_item = TaggedItemFactory(object=entry)

    def get_view_name(self):
        return 'news_rss_any_tagged'

    def get_view_kwargs(self):
        return {'tag': self.tagged_item.tag.slug, 'any_language': True}

    def test_view(self):
        self.is_callable()

    def test_tag_does_not_exist(self):
        self.tagged_item.tag.delete()
        self.is_not_callable()
