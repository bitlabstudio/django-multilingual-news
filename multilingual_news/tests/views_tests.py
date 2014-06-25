"""Tests for the views of the ``multilingual_news`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import timedelta, now

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewRequestFactoryTestMixin
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


class DeleteNewsEntryViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DeleteNewsEntryView`` view class."""
    view_class = views.DeleteNewsEntryView

    def get_view_kwargs(self):
        return {'pk': self.entry.pk}

    def setUp(self):
        self.user = UserFactory()
        self.admin = UserFactory(is_superuser=True)
        self.entry = factories.NewsEntryFactory()
        self.entry2 = factories.NewsEntryFactory()

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_not_callable(user=self.user)
        self.is_not_callable(user=self.user, ajax=True)
        self.is_callable(user=self.admin)
        self.is_callable(user=self.admin, ajax=True)
        self.is_postable(user=self.admin, ajax=True)
        self.assertEqual(models.NewsEntry.objects.count(), 1, msg=(
            'After posting, there should only be one entry in the db.'))

        self.is_postable(user=self.admin, kwargs={'pk': self.entry2.pk},
                         to=reverse('news_list'))
        self.assertEqual(models.NewsEntry.objects.count(), 0, msg=(
            'After posting again for the other entry, there should be'
            ' no more entry in the database.'))


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


class NewsListViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``NewsListView`` view."""
    view_class = views.NewsListView

    def setUp(self):
        factories.NewsEntryFactory()
        self.admin = UserFactory(is_superuser=True)

    def get_view_name(self):
        return 'news_list'

    def test_view(self):
        self.is_callable()
        self.is_callable(user=self.admin)


class PublishNewsEntryViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``PublishNewsEntryView`` view class."""
    view_class = views.PublishNewsEntryView

    def get_view_kwargs(self):
        return {'pk': self.entry.pk}

    def setUp(self):
        self.user = UserFactory()
        self.admin = UserFactory(is_superuser=True)
        self.entry = factories.NewsEntryFactory()

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()

        # getting the view should not be possible
        resp = self.get(user=self.user)
        self.assertEqual(resp.status_code, 405)
        resp = self.get(user=self.admin)
        self.assertEqual(resp.status_code, 405)

        self.is_not_callable(post=True, user=self.user)
        self.is_not_callable(post=True, user=self.admin, kwargs={'pk': 999})

        self.is_postable(user=self.admin, data={'action': 'publish'},
                         to=reverse('news_detail', kwargs={
                             'slug': self.entry.slug}))
        self.assertTrue(
            models.NewsEntry.objects.get(pk=self.entry.pk).is_published)
        self.is_postable(user=self.admin, data={'action': 'unpublish'},
                         to=reverse('news_detail', kwargs={
                             'slug': self.entry.slug}))
        self.assertFalse(
            models.NewsEntry.objects.get(pk=self.entry.pk).is_published)


class TaggedNewsListViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``TaggedNewsListView`` view."""
    view_class = views.TaggedNewsListView

    def setUp(self):
        entry = factories.NewsEntryFactory()
        self.tagged_item = TaggedItemFactory(object=entry)

    def get_view_name(self):
        return 'news_archive_tagged'

    def get_view_kwargs(self):
        return {'tag': self.tagged_item.tag.slug}

    def test_view(self):
        self.is_callable()
        self.is_callable(kwargs={'tag': 'foobar'})


class NewsDateDetailViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``NewsDateDetailView`` view."""
    view_class = views.NewsDateDetailView

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
            'year': unicode(self.entry.pub_date.year),
            'month': unicode(self.entry.pub_date.month),
            'day': unicode(self.entry.pub_date.day),
        }

    def test_view(self):
        self.is_callable()
        data = {
            'slug': self.en_trans.slug,
            'year': u'9999',
            'month': unicode(self.entry.pub_date.month),
            'day': unicode(self.entry.pub_date.day),
        }
        self.is_not_callable(kwargs=data)

        data = {
            'slug': 'foo',
            'year': unicode(self.entry.pub_date.year),
            'month': unicode(self.entry.pub_date.month),
            'day': unicode(self.entry.pub_date.day),
        }
        self.is_not_callable(kwargs=data)

        data = {
            'slug': self.de_trans.slug,
            'year': unicode(self.entry.pub_date.year),
            'month': unicode(self.entry.pub_date.month),
            'day': unicode(self.entry.pub_date.day),
        }


class NewsDetailPreviewViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Test for the `NewsDetailPreviewView` view class."""
    view_class = views.NewsDetailPreviewView

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
        self.should_redirect_to_login_when_anonymous()
        self.is_not_callable(user=self.user)
        self.is_callable(user=self.admin)
