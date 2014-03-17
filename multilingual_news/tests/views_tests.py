"""Tests for the views of the ``multilingual_news`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta, now

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import (
    ViewRequestFactoryTestMixin,
    ViewTestMixin,
)
from multilingual_tags.tests.factories import TaggedItemFactory

from . import factories
from .. import models
from .. import views


class CategoryListViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``CategoryListView`` generic view class."""
    view_class = views.CategoryListView

    def setUp(self):
        self.category = factories.CategoryFactory()
        self.entry = factories.NewsEntryFactory(category=self.category)

    def get_view_name(self):
        return 'news_archive_category'

    def get_view_kwargs(self):
        return {'category': self.category.slug}

    def test_view(self):
        self.is_callable()


class GetEntriesAjaxViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``GetEntriesAjaxView`` view class."""
    view_class = views.GetEntriesAjaxView

    def get_view_name(self):
        return 'news_get_entries'

    def test_view_with_count(self):
        self.is_callable(data={'count': 1})

    def test_view_with_category(self):
        category = factories.CategoryFactory()
        self.is_callable(data={'category': category.slug})


class NewsListViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsListView`` view."""
    def setUp(self):
        factories.NewsEntryFactory()

    def get_view_name(self):
        return 'news_list'

    def test_view(self):
        self.should_be_callable_when_anonymous()


class TaggedNewsListViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsListView`` view."""

    def setUp(self):
        entry = factories.NewsEntryFactory()
        self.tagged_item = TaggedItemFactory(object=entry)

    def get_view_name(self):
        return 'news_archive_tagged'

    def get_view_kwargs(self):
        return {'tag': self.tagged_item.tag.slug}

    def test_view(self):
        self.should_be_callable_when_anonymous()
        self.is_callable(kwargs={'tag': 'foobar'})


class NewsDateDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsDateDetailView`` view."""
    def setUp(self):
        self.entry = factories.NewsEntryFactory(
            pub_date=now() - timedelta(days=1))
        self.en_trans = self.entry.translations.get(language_code='en')
        self.entry.translate('de')
        self.entry.title = 'German title'
        self.entry.slug = 'german-title'
        self.entry.save()
        self.de_trans = self.entry.translations.get(language_code='de')
        self.entry = models.NewsEntry.objects.language('en').get(
            pk=self.entry.pk)

    def get_view_name(self):
        return 'news_detail'

    def get_view_kwargs(self):
        return {
            'slug': self.en_trans.slug,
            'year': self.entry.pub_date.year,
            'month': self.entry.pub_date.month,
            'day': self.entry.pub_date.day,
        }

    def test_view(self):
        self.should_be_callable_when_anonymous()
        data = {
            'slug': self.en_trans.slug,
            'year': 9999,
            'month': self.entry.pub_date.month,
            'day': self.entry.pub_date.day,
        }
        self.is_not_callable(kwargs=data, message=(
            "If date doesn't match an object, raise a 404"))

        data = {
            'slug': 'foo',
            'year': self.entry.pub_date.year,
            'month': self.entry.pub_date.month,
            'day': self.entry.pub_date.day,
        }
        self.is_not_callable(kwargs=data, message=(
            "If slug doesn't match an object, raise a 404"))

        data = {
            'slug': self.de_trans.slug,
            'year': self.entry.pub_date.year,
            'month': self.entry.pub_date.month,
            'day': self.entry.pub_date.day,
        }


class NewsDetailPreviewViewTestCase(ViewTestMixin, TestCase):
    """Test for the `NewsDetailPreviewView` view class."""

    def get_view_name(self):
        return 'news_preview'

    def get_view_kwargs(self):
        return {
            'slug': self.en_trans.slug,
        }

    def setUp(self):
        self.entry = factories.NewsEntryFactory(
            pub_date=now() - timedelta(days=1))
        self.en_trans = self.entry.translations.get(language_code='en')

        self.user = UserFactory()
        self.admin = UserFactory(is_superuser=True)

    def test_view(self):
        self.is_not_callable()
        self.is_not_callable(user=self.user)
        self.is_callable(user=self.admin)
