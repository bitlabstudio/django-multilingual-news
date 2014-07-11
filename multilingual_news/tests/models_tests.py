"""Tests for the models of the ``multilingual_news`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from .. import models
from . import factories


class CategoryTestCase(TestCase):
    """Tests for the ``Category`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Category`` model."""
        category = factories.CategoryFactory()
        self.assertTrue(category.pk)


class NewsEntryTestCase(TestCase):
    """Tests for the ``NewsEntry`` model."""
    longMessage = True

    def test_model(self):
        instance = factories.NewsEntryFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_get_preview_url(self):
        instance = factories.NewsEntryFactory()
        result = instance.get_preview_url()
        slug = instance.slug
        self.assertEqual(
            result, reverse('news_preview', kwargs={'slug': slug}), msg=(
                'Should return the preview url.'))

    def test_category(self):
        instance = factories.NewsEntryFactory()
        self.assertIsNone(instance.category, msg=(
            'Should return None if entry has no category.'))


class NewsEntryManagerTestCase(TestCase):
    """Tests for the ``NewsEntryManager`` model manager."""
    longMessage = True

    def setUp(self):
        self.published_en = factories.NewsEntryFactory(is_published=True)
        factories.NewsEntryFactory(language_code='de', is_published=True)
        factories.NewsEntryFactory(language_code='de', is_published=True)

    def test_published(self):
        self.assertEqual(
            models.NewsEntry.objects.published(language='de').count(), 2, msg=(
                'In German, there should be two published entries.'))

        self.assertEqual(
            models.NewsEntry.objects.published(language='en').count(), 1, msg=(
                'In English, there should be one published entry.'))

        self.assertEqual(
            models.NewsEntry.objects.published().count(), 1, msg=(
                'If no language set, we get the ones for the default'
                ' language.'))

    def test_recent(self):
        result = models.NewsEntry.objects.recent()
        self.assertEqual(result.count(), 1, msg=(
            'Should return recent objects for the default language'))

        result = models.NewsEntry.objects.recent(language='de')
        self.assertEqual(result.count(), 2, msg=(
            'Should return recent objects for the German language'))

        result = models.NewsEntry.objects.recent(check_language=False)
        self.assertEqual(result.count(), 3, msg=(
            'Should return recent objects for all languages'))

        result = models.NewsEntry.objects.recent(
            check_language=False, exclude=self.published_en)
        self.assertEqual(result.count(), 2, msg=(
            'Should exclude the given object'))
