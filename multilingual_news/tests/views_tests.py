"""Tests for the views of the ``multilingual_news`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta, now

from django_libs.tests.mixins import ViewTestMixin

from . import factories
from .. import models


class NewsListViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsListView`` view."""
    def setUp(self):
        factories.NewsEntryFactory()

    def get_view_name(self):
        return 'news_list'

    def test_view(self):
        self.should_be_callable_when_anonymous()


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
