"""Models for the ``multilingual_news`` app."""
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields, TranslationManager
from cms.models.fields import PlaceholderField
from cms.models import CMSPlugin
from cms.utils import get_language_from_request
from filer.fields.image import FilerImageField


class NewsEntryManager(TranslationManager):
    """Custom manager for the ``NewsEntry`` model."""
    def published(self, request, check_language=True):
        """
        Returns all entries, which publication date has been hit or which have
        no date and which language matches the current language.

        :param request: A Request instance.
        :param check_language: Option to disable language filtering.

        """
        qs = self.get_query_set().filter(
            models.Q(translations__is_published=True),
            models.Q(pub_date__lte=now()) | models.Q(pub_date__isnull=True)
        )
        if check_language:
            language = get_language_from_request(request)
            qs = qs.filter(translations__language_code=language)
        return qs.distinct()

    def recent(self, request, check_language=True, limit=3, exclude=None):
        """
        Returns recently published new entries.

        :param request: A Request instance.
        :param check_language: Option to disable language filtering.

        """
        qs = self.published(request, check_language=check_language)
        if check_language:
            # Filter news with current language
            language = get_language_from_request(request)
            qs = qs.filter(translations__language_code=language)
        if exclude:
            qs = qs.exclude(pk=exclude.pk)
        return qs[:limit]


class NewsEntry(TranslatableModel):
    """
    A news entry consists of a title, content and media fields.

    See ``NewsEntryTitle`` for the translateable fields of this model.

    :author: Optional FK to the User who created this entry.
    :pub_date: DateTime when this entry should be published.
    :image: Main image of the blog entry.
    :image_float: Can be set to ``none``, ``left`` or ``right`` to adjust
      floating behaviour in the blog entry template.
    :image_width: Can be set to manipulate image width
    :image_height: Can be set to manipulate image height
    :image_source_text: Text for the link to the image source
    :image_source_url: URL for the link to the image source
    :placeholders: CMS placeholders for ``exerpt`` and ``content``

    """
    IMAGE_FLOAT_VALUES = {
        'left': 'left',
        'right': 'right',
    }

    IMAGE_FLOAT_CHOICES = (
        (IMAGE_FLOAT_VALUES['left'], _('Left')),
        (IMAGE_FLOAT_VALUES['right'], _('Right')),
    )

    translations = TranslatedFields(
        title=models.CharField(
            max_length=512,
            verbose_name=_('Title'),
        ),

        slug=models.SlugField(
            max_length=512,
            verbose_name=_('Slug'),
        ),

        is_published=models.BooleanField(
            verbose_name=_('Is published'),
            default=False,
        ),
    )

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

    image_float = models.CharField(
        max_length=8,
        verbose_name=_('Image float'),
        choices=IMAGE_FLOAT_CHOICES,
        blank=True,
    )

    image_width = models.IntegerField(
        verbose_name=_('Image width'),
        null=True, blank=True,
    )

    image_height = models.IntegerField(
        verbose_name=_('Image height'),
        null=True, blank=True,
    )

    image_source_url = models.CharField(
        max_length=1024,
        verbose_name=_('Image source URL'),
        blank=True,
    )

    image_source_text = models.CharField(
        max_length=1024,
        verbose_name=_('Image source text'),
        blank=True,
    )

    excerpt = PlaceholderField(
        slotname='multilingnual_news_excerpt',
        related_name='multilingual_news_excerpts',
        blank=True, null=True,
    )

    content = PlaceholderField(
        slotname='multilingnual_news_content',
        related_name='multilingual_news_contents',
        blank=True, null=True,
    )

    objects = NewsEntryManager()

    class Meta:
        ordering = ('-pub_date', )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if not self.is_published:
            return self.get_preview_url()
        slug = self.slug
        if self.pub_date:
            return reverse('news_detail', kwargs={
                'year': self.pub_date.year, 'month': self.pub_date.month,
                'day': self.pub_date.day, 'slug': slug})
        return reverse('news_detail', kwargs={'slug': slug})

    def get_preview_url(self):
        slug = self.slug
        return reverse('news_preview', kwargs={'slug': slug})


class RecentPlugin(CMSPlugin):
    """Plugin model to display recent news."""
    limit = models.PositiveIntegerField(
        verbose_name=_('Maximum news amount'),
    )
    current_language_only = models.BooleanField(
        verbose_name=_('Only show entries for the selected language'),
    )
