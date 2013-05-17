"""Models for the ``multilingual_news`` app."""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from django_libs.models_mixins import SimpleTranslationMixin
from djangocms_utils.fields import M2MPlaceholderField
from filer.fields.image import FilerImageField
from simple_translation.actions import SimpleTranslationPlaceholderActions
from simple_translation.utils import get_preferred_translation_from_lang


class NewsEntryManager(models.Manager):
    """Custom manager for the ``NewsEntry`` model."""
    def published(self, request, check_language=True):
        """
        Returns all entries, which publication date has been hit or which have
        no date and which language matches the current language.

        :param request: A Request instance.
        :param check_language: Option to disable language filtering.

        """
        results = self.get_query_set().filter(
            models.Q(newsentrytitle__is_published=True),
            models.Q(pub_date__lte=now()) | models.Q(pub_date__isnull=True)
        )
        if check_language:
            language = getattr(request, 'LANGUAGE_CODE', None)
            if not language:
                self.model.objects.none()
            results = results.filter(newsentrytitle__language=language)
        return results.distinct()


class NewsEntry(SimpleTranslationMixin, models.Model):
    """
    A news entry consists of a title, content and media fields.

    See ``NewsEntryTitle`` for the translateable fields of this model.

    :author: Optional FK to the User who created this entry.
    :pub_date: DateTime when this entry should be published.

    """
    author = models.ForeignKey(
        'auth.User',
        verbose_name=_('Author'),
        null=True, blank=True,
    )

    pub_date = models.DateTimeField(
        verbose_name=_('Publication date'),
        blank=True, null=True,
    )

    image = FilerImageField(
        verbose_name=_('Image'),
        null=True, blank=True,
    )

    placeholders = M2MPlaceholderField(
        actions=SimpleTranslationPlaceholderActions(),
        placeholders=('excerpt', 'content'),
    )

    objects = NewsEntryManager()

    class Meta:
        ordering = ('-pub_date', )

    def __unicode__(self):
        return self.get_title()

    def get_absolute_url(self):
        slug = self.get_slug()
        if self.pub_date:
            return reverse('news_detail', kwargs={
                'year': self.pub_date.year, 'month': self.pub_date.month,
                'day': self.pub_date.day, 'slug': slug})
        return reverse('news_detail', kwargs={'slug': slug})

    def get_slug(self):
        lang = get_language()
        return get_preferred_translation_from_lang(self, lang).slug

    def get_title(self):
        lang = get_language()
        return get_preferred_translation_from_lang(self, lang).title


class NewsEntryTitle(models.Model):
    """
    The translateable fields of the ``NewsEntry`` model.

    :title: The title of the entry.
    :slug: Slug to be used in the url only.
    :is_published: If ``True`` the object will be visible on it's pub_date.

    """
    title = models.CharField(
        max_length=512,
        verbose_name=_('Title'),
    )

    slug = models.SlugField(
        max_length=512,
        verbose_name=_('Slug'),
    )

    is_published = models.BooleanField(
        verbose_name=_('Is published'),
        default=False,
    )

    # Needed by simple-translation
    entry = models.ForeignKey(
        NewsEntry, verbose_name=_('News entry'))

    language = models.CharField(
        max_length=5, verbose_name=('Language'), choices=settings.LANGUAGES)
