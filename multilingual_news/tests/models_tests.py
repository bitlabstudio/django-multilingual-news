"""Tests for the models of the ``multilingual_news`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now, timedelta

from mock import Mock

from ..models import NewsEntry
from .factories import (
    NewsEntryFactory,
    NewsEntryTitleDEFactory,
    NewsEntryTitleENFactory,
)


class NewsEntryTestCase(TestCase):
    """Tests for the ``NewsEntry`` model."""
    longMessage = True

    def test_model(self):
        instance = NewsEntryFactory()
        self.assertTrue(instance.pk, msg=(
            'Should be able to instantiate and save the object.'))

    def test_is_published(self):
        title = NewsEntryTitleDEFactory()
        instance = title.entry
        result = instance.is_published()
        self.assertTrue(result, msg=('Should return True if published.'))
        instance.pub_date = now() + timedelta(days=1)
        self.assertFalse(instance.is_published(), msg=(
            'Should return False if publication date in future.'))

    def test_get_preview_url(self):
        title = NewsEntryTitleDEFactory()
        instance = title.entry
        result = instance.get_preview_url()
        slug = instance.get_slug()
        self.assertEqual(
            result, reverse('news_preview', kwargs={'slug': slug}), msg=(
                'Should return the preview url.'))

    def test_get_title(self):
        title = NewsEntryTitleDEFactory()
        instance = title.entry
        result = instance.get_title()
        self.assertIn('Ein Titel', result, msg=(
            'Should return the translated title.'))


class NewsEntryManagerTestCase(TestCase):
    """Tests for the ``NewsEntryManager`` model manager."""
    longMessage = True

    def setUp(self):
        self.en_title = NewsEntryTitleENFactory(is_published=False)
        self.de_title = NewsEntryTitleDEFactory(is_published=False)
        NewsEntryTitleENFactory(entry=self.en_title.entry)
        NewsEntryTitleDEFactory(entry=self.de_title.entry)
        NewsEntryTitleDEFactory()

    def test_manager(self):
        """Test, if the ``NewsEntryManager`` returns the right entries."""
        request = Mock(LANGUAGE_CODE='de')
        self.assertEqual(
            NewsEntry.objects.published(request).count(), 2, msg=(
                'In German, there should be two published entries.'))

        request = Mock(LANGUAGE_CODE='en')
        self.assertEqual(
            NewsEntry.objects.published(request).count(), 1, msg=(
                'In English, there should be one published entry.'))

        request = Mock(LANGUAGE_CODE=None)
        self.assertEqual(
            NewsEntry.objects.published(request).count(), 0, msg=(
                'If no language set, there should be no published entries.'))
