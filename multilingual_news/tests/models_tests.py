"""Tests for the models of the ``multilingual_news`` app."""
from django.urls import reverse
from django.test import TestCase

from mixer.backend.django import mixer

from .. import models


class CategoryTestCase(TestCase):
    """Tests for the ``Category`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Category`` model."""
        category = mixer.blend('multilingual_news.Category')
        self.assertTrue(category.pk)


class NewsEntryTestCase(TestCase):
    """Tests for the ``NewsEntry`` model."""
    longMessage = True

    def setUp(self):
        self.instance = mixer.blend('multilingual_news.NewsEntry')
        self.instance.set_current_language('en')
        self.instance.slug = 'foo'
        self.instance.save()

    def test_model(self):
        self.assertTrue(self.instance.pk, msg='Should be able to instantiate and save the object.')

    def test_get_preview_url(self):
        result = self.instance.get_preview_url()
        slug = self.instance.slug
        self.assertEqual(
            result, reverse('news_preview', kwargs={'slug': slug}), msg='Should return the preview url.')

    def test_get_absolute_url(self):
        result = self.instance.get_absolute_url()
        slug = self.instance.slug
        self.assertEqual(
            result, reverse('news_detail', kwargs={'slug': slug}), msg='Should return the detail url.')

    def test_category(self):
        self.assertIsNone(self.instance.category, msg=(
            'Should return None if entry has no category.'))


class NewsEntryManagerTestCase(TestCase):
    """Tests for the ``NewsEntryManager`` model manager."""
    longMessage = True

    def setUp(self):
        entry = mixer.blend('multilingual_news.NewsEntry')
        entry.set_current_language('en')
        entry.title = 'Foo en'
        entry.slug = 'foo-en'
        entry.is_published = True
        entry.save()
        entry.set_current_language('de')
        entry.title = 'Foo-de'
        entry.slug = 'foo-de'
        entry.is_published = True
        entry.save()

        entry = mixer.blend('multilingual_news.NewsEntry')
        entry.set_current_language('en')
        entry.title = 'Bar en'
        entry.slug = 'bar-en'
        entry.is_published = True
        entry.save()
        entry.set_current_language('de')
        entry.title = 'Bar-de'
        entry.slug = 'bar-de'
        entry.is_published = True
        entry.save()

    def test_published(self):
        self.assertEqual(
            models.NewsEntry.objects.published(language='de').count(), 2, msg=(
                'In German, there should be two published entries.'))

        self.assertEqual(
            models.NewsEntry.objects.published(language='en').count(), 2, msg=(
                'In English, there should be two published entries.'))

        self.assertEqual(
            models.NewsEntry.objects.published().count(), 2, msg=(
                'If no language set, we get the ones for the default language.'))

    def test_recent(self):
        result = models.NewsEntry.objects.recent()
        self.assertEqual(result.count(), 2, msg=(
            'Should return recent objects for the default language'))

        result = models.NewsEntry.objects.recent(language='de')
        self.assertEqual(result.count(), 2, msg=(
            'Should return recent objects for the German language'))

        result = models.NewsEntry.objects.recent(check_language=False)
        self.assertEqual(result.count(), 2, msg=(
            'Should return recent objects for all languages'))

        result = models.NewsEntry.objects.recent(
            check_language=False, exclude=models.NewsEntry.objects.published(
                language='en')[0])
        self.assertEqual(result.count(), 1, msg=(
            'Should exclude the given object'))
