"""Tests for the views of the ``multilingual_news`` app."""
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.test import TestCase
from django.utils.translation import activate
from django.utils.timezone import timedelta, now

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer

from .. import models
from .. import views


class CategoryListViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``CategoryListView`` generic view class."""
    view_class = views.CategoryListView

    def setUp(self):
        self.category = mixer.blend('multilingual_news.Category')
        self.entry = mixer.blend(
            'multilingual_news.NewsEntry',
            author=mixer.blend('people.Person'),
            categories=[self.category],
        )

    def get_view_name(self):
        return 'news_archive_category'

    def get_view_kwargs(self):
        return {'category': self.category.slug}

    def test_view(self):
        self.is_callable()
        self.is_not_callable(kwargs={'category': 'foo'})


class DeleteNewsEntryViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DeleteNewsEntryView`` view class."""
    view_class = views.DeleteNewsEntryView

    def get_view_kwargs(self):
        return {'pk': self.entry.pk}

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.admin = mixer.blend('auth.User', is_superuser=True)
        self.entry = mixer.blend('multilingual_news.NewsEntry')
        self.entry.set_current_language('en')
        self.entry.is_published = True
        self.entry.save()

        self.entry2 = mixer.blend('multilingual_news.NewsEntry')
        self.entry2.set_current_language('en')
        self.entry2.is_published = True
        self.entry2.save()

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
                         to_url_name='news_list')
        self.assertEqual(models.NewsEntry.objects.count(), 0, msg=(
            'After posting, there should be no entry in the db.'))


class GetEntriesAjaxViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``GetEntriesAjaxView`` view class."""
    view_class = views.GetEntriesAjaxView

    def get_view_name(self):
        return 'news_get_entries'

    def test_view_with_count(self):
        self.is_callable(data={'count': 1})

    def test_view_with_category(self):
        category = mixer.blend('multilingual_news.Category')
        self.is_callable(data={'category': category.slug})


class NewsListViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``NewsListView`` view."""
    view_class = views.NewsListView

    def setUp(self):
        mixer.blend('multilingual_news.NewsEntry', author=mixer.blend('people.Person'))
        self.admin = mixer.blend('auth.User', is_superuser=True)

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
        self.user = mixer.blend('auth.User')
        self.admin = mixer.blend('auth.User', is_superuser=True)
        self.entry = mixer.blend('multilingual_news.NewsEntry')
        self.entry.set_current_language('en')
        self.entry.is_published = True
        self.entry.slug = 'foo'
        self.entry.save()

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
        entry = mixer.blend(
            'multilingual_news.NewsEntryTranslation',
            master__author=mixer.blend('people.Person'))
        self.tag = mixer.blend('multilingual_tags.Tag')
        self.tag.set_current_language('en')
        self.tag.name = 'Foo'
        self.tag.save()
        mixer.blend(
            'multilingual_tags.TaggedItem',
            tag=self.tag,
            content_type=ContentType.objects.get_for_model(models.NewsEntry),
            object_id=entry.pk)

    def get_view_name(self):
        return 'news_archive_tagged'

    def get_view_kwargs(self):
        return {'tag': self.tag.slug}

    def test_view(self):
        self.is_callable()
        self.is_callable(kwargs={'tag': 'foobar'})


class NewsDateDetailViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``NewsDateDetailView`` view."""
    view_class = views.NewsDateDetailView

    def setUp(self):
        self.entry = mixer.blend('multilingual_news.NewsEntry')
        self.entry.set_current_language('en')
        self.entry.is_published = True
        self.entry.pub_date = now() - timedelta(days=1)
        self.entry.save()
        self.entry.set_current_language('de')
        self.entry.is_published = True
        self.entry.title = 'German title'
        self.entry.slug = 'german-title'
        self.entry.save()

    def get_view_name(self):
        return 'news_detail'

    def get_view_kwargs(self):
        activate('en')
        self.is_callable()
        return {
            'slug': self.entry.slug,
            'year': str(self.entry.pub_date.year),
            'month': str(self.entry.pub_date.month),
            'day': str(self.entry.pub_date.day),
        }

    def test_view(self):
        kwargs = {
            'slug': self.entry.slug,
            'year': u'9999',
            'month': str(self.entry.pub_date.month),
            'day': str(self.entry.pub_date.day),
        }
        self.is_not_callable(kwargs=kwargs)

        kwargs = {
            'slug': 'foo',
            'year': str(self.entry.pub_date.year),
            'month': str(self.entry.pub_date.month),
            'day': str(self.entry.pub_date.day),
        }
        self.is_not_callable(kwargs=kwargs)

        kwargs = {
            'slug': 'german-title',
            'year': str(self.entry.pub_date.year),
            'month': str(self.entry.pub_date.month),
            'day': str(self.entry.pub_date.day),
        }
        activate('de')
        self.is_callable(kwargs=kwargs)


class NewsDetailPreviewViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Test for the `NewsDetailPreviewView` view class."""
    view_class = views.NewsDetailPreviewView

    def get_view_name(self):
        return 'news_preview'

    def get_view_kwargs(self):
        return {
            'slug': 'foo',
        }

    def setUp(self):
        self.entry = mixer.blend('multilingual_news.NewsEntry')
        self.entry.set_current_language('en')
        self.entry.slug = 'foo'
        self.entry.pub_date = now() - timedelta(days=1)
        self.entry.save()

        self.user = mixer.blend('auth.User')
        self.admin = mixer.blend('auth.User', is_superuser=True)

    def test_view(self):
        activate('en')
        self.is_not_callable(user=self.user)
        self.is_callable(user=self.admin)
