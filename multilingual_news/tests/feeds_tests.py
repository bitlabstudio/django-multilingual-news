"""Tests for the news feeds of the `multilingual_news` app."""
from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import NoReverseMatch

# Note: The feeds can't be tested with the ViewRequestFactoryTestMixin
from django_libs.tests.mixins import ViewTestMixin
from mixer.backend.django import mixer

from ..models import NewsEntry


# the key part is only, that the LocaleMiddleware must be taken out.
NON_MULTILINGUAL_MIDDLWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)


class NewsEntriesFeedTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsEntriesFeed`` view class."""

    def setUp(self):
        self.entry = mixer.blend(
            'multilingual_news.NewsEntryTranslation',
            master__author=mixer.blend('people.PersonTranslation'))

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
        mixer.blend(
            'multilingual_news.NewsEntryTranslation',
            master__author=mixer.blend('people.PersonTranslation'))

    def get_view_name(self):
        return 'news_rss_any'

    def get_view_kwargs(self):
        return {'any_language': True}

    def test_view(self):
        self.is_callable()


class AuthorFeedTestCase(ViewTestMixin, TestCase):
    """Tests for the ``AuthorFeed`` view class."""

    def setUp(self):
        author_trans = mixer.blend('people.PersonTranslation',
                                   language_code='en')
        self.author = author_trans.master
        mixer.blend('multilingual_news.NewsEntryTranslation',
                    master__author=author_trans, language_code='en')

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
        author_trans = mixer.blend('people.PersonTranslation',
                                   language_code='en')
        self.author = author_trans.master
        mixer.blend('multilingual_news.NewsEntryTranslation',
                    master__author=author_trans, language_code='en')

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
        entry = mixer.blend(
            'multilingual_news.NewsEntryTranslation',
            language_code='en',
            master__author=mixer.blend('people.PersonTranslation',
                                       language_code='en'))
        self.tag = mixer.blend('multilingual_tags.TagTranslation',
                               language_code='en').master
        mixer.blend(
            'multilingual_tags.TaggedItem',
            tag=self.tag,
            content_type=ContentType.objects.get_for_model(NewsEntry),
            object_id=entry.pk)

    def get_view_kwargs(self):
        return {'tag': self.tag.slug}

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
        entry = NewsEntry()
        entry.translate('en')
        entry.save()
        self.tag = mixer.blend('multilingual_tags.TagTranslation',
                               language_code='en').master
        mixer.blend(
            'multilingual_tags.TaggedItem',
            tag=self.tag,
            content_type=ContentType.objects.get_for_model(NewsEntry),
            object_id=entry.pk)

    def get_view_name(self):
        return 'news_rss_any_tagged'

    def get_view_kwargs(self):
        return {'tag': self.tag.slug, 'any_language': True}

    def test_view(self):
        self.is_callable()

    def test_tag_does_not_exist(self):
        self.tag.delete()
        self.is_not_callable()
