"""Tests for the views of the ``multilingual_news`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta, now

from django_libs.tests.mixins import ViewTestMixin

from .factories import NewsEntryTitleDEFactory, NewsEntryTitleENFactory


class NewsListViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsListView`` view."""
    def setUp(self):
        NewsEntryTitleENFactory()

    def get_view_name(self):
        return 'news_list'

    def test_view(self):
        self.should_be_callable_when_anonymous()


class NewsDateDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``NewsDateDetailView`` view."""
    def setUp(self):
        self.en_title = NewsEntryTitleENFactory(
            entry__pub_date=now() - timedelta(days=1))
        self.de_title = NewsEntryTitleDEFactory(entry=self.en_title.entry)
        self.entry = self.en_title.entry

    def get_view_name(self):
        return 'news_detail'

    def get_view_kwargs(self):
        return {
            'slug': self.en_title.slug,
            'year': self.entry.pub_date.year,
            'month': self.entry.pub_date.month,
            'day': self.entry.pub_date.day,
        }

    def test_view(self):
        self.should_be_callable_when_anonymous()
        data = {
            'slug': self.en_title.slug,
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
            'slug': self.de_title.slug,
            'year': self.entry.pub_date.year,
            'month': self.entry.pub_date.month,
            'day': self.entry.pub_date.day,
        }
        self.is_callable(
            kwargs=data,
            message=('Redirect, if slug is another language object.'),
            and_redirects_to=self.entry.get_absolute_url(),
        )
