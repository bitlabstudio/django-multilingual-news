"""Models for the ``multilingual_news`` app."""
import re

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.generic import GenericRelation
from django.db import models
from django.utils.html import escape
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _, get_language

from cms.models.fields import PlaceholderField
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from hvad.models import TranslatableModel, TranslatedFields, TranslationManager
from multilingual_tags.models import TaggedItem


class Category(TranslatableModel):
    """
    A blog ``Entry`` can belong to one category.

    :creation_date: Date when this category was created.
    :slug: The slug for this category. The slug will be the same for all
      languages.
    :parent: Allows you to build hierarchies of categories.
    :hide_on_list: Boolean to show/hide on list view.

    """
    creation_date = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(
        max_length=512,
        verbose_name=_('Slug'),
    )

    parent = models.ForeignKey(
        'multilingual_news.Category',
        verbose_name=_('Parent'),
        null=True, blank=True,
    )

    hide_on_list = models.BooleanField(
        default=False,
        verbose_name=_('Hide on list view'),
    )

    translations = TranslatedFields(
        title=models.CharField(
            max_length=256,
            verbose_name=_('Title'),
        )
    )

    class Meta:
        ordering = ('slug', )
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.safe_translation_getter('title', self.slug)

    def get_entries(self):
        """Returns the entries for this category."""
        return self.newsentries.filter(
            translations__is_published=True, pub_date__lte=now()).order_by(
            '-pub_date').distinct()

    def get_absolute_url(self):
        return reverse('news_archive_category', kwargs={
            'category': self.slug, })


class CategoryPlugin(CMSPlugin):
    """
    Plugin, which renders entries belonging to one or more category.

    :categories: ...
    :template_argument: Char which is place within templates as True, if you
      want to alter a template.

    """
    categories = models.ManyToManyField(
        Category,
        verbose_name=_('Category'),
    )

    template_argument = models.CharField(
        max_length=20,
        verbose_name=_('Template Argument'),
        blank=True,
    )


class NewsEntryManager(TranslationManager):
    """Custom manager for the ``NewsEntry`` model."""
    def published(self, check_language=True, language=None, kwargs=None,
                  exclude_kwargs=None):
        """
        Returns all entries, which publication date has been hit or which have
        no date and which language matches the current language.

        """
        if check_language:
            qs = NewsEntry.objects.language(language or get_language()).filter(
                is_published=True)
        else:
            qs = self.get_queryset()
        qs = qs.filter(
            models.Q(pub_date__lte=now()) | models.Q(pub_date__isnull=True)
        )
        if kwargs is not None:
            qs = qs.filter(**kwargs)
        if exclude_kwargs is not None:
            qs = qs.exclude(**exclude_kwargs)
        return qs.distinct().order_by('-pub_date')

    def recent(self, check_language=True, language=None, limit=3, exclude=None,
               kwargs=None, category=None):
        """
        Returns recently published new entries.

        """
        if category:
            if not kwargs:
                kwargs = {}
            kwargs['categories__in'] = [category]
        qs = self.published(check_language=check_language, language=language,
                            kwargs=kwargs)
        if exclude:
            qs = qs.exclude(pk=exclude.pk)
        return qs[:limit]


class NewsEntry(TranslatableModel):
    """
    A news entry consists of a title, content and media fields.

    See ``NewsEntryTitle`` for the translateable fields of this model.

    :author: Optional FK to the Person, who created this NewsEntry.
    :category: The optional category this entry belongs to.
    :pub_date: DateTime when this entry should be published.
    :image: Main image of the blog entry.
    :image_float: Can be set to ``none``, ``left`` or ``right`` to adjust
      floating behaviour in the blog entry template.
    :image_width: Can be set to manipulate image width
    :image_height: Can be set to manipulate image height
    :image_source_text: Text for the link to the image source
    :image_source_url: URL for the link to the image source
    :thumbnail: Optional thumbnail to be used in list views.
    :content: CMS placeholder for ``content``
    :excerpt: CMS placeholder for ``excerpt``
    :meta_title: the title, that goes into the meta tags.
    :meta_description: the description, that goes into the meta tags.

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
        meta_title=models.CharField(
            verbose_name=_('Meta title'),
            help_text=_('Best to keep this below 70 characters'),
            max_length=128,
            blank=True, null=True,
        ),
        meta_description=models.TextField(
            verbose_name=_('Meta description'),
            help_text=_('Best to keep this below 160 characters'),
            max_length=512,
            blank=True, null=True,
        )
    )

    author = models.ForeignKey(
        'people.Person',
        verbose_name=_('Author'),
        blank=True, null=True,
    )

    categories = models.ManyToManyField(
        Category,
        verbose_name=_('Categories'),
        related_name='newsentries',
        blank=True, null=True,
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

    thumbnail = FilerImageField(
        verbose_name=_('Thumbnail'),
        null=True, blank=True,
        related_name='entries_with_thumbnails',
    )

    excerpt = PlaceholderField(
        slotname='multilingual_news_excerpt',
        related_name='multilingual_news_excerpts',
        blank=True, null=True,
    )

    content = PlaceholderField(
        slotname='multilingual_news_content',
        related_name='multilingual_news_contents',
        blank=True, null=True,
    )

    tags = GenericRelation(TaggedItem)
    objects = NewsEntryManager()

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = _('News Entry')
        verbose_name_plural = _('News Entries')

    def __unicode__(self):
        return self.safe_translation_getter('title', 'Untranslated entry')

    @property
    def category(self):
        try:
            return self.categories.all()[0]
        except IndexError:
            return None

    def get_absolute_url(self):
        if self.pub_date:
            return reverse('news_detail', kwargs={
                'year': self.pub_date.year, 'month': self.pub_date.month,
                'day': self.pub_date.day, 'slug': self.slug})
        return reverse('news_detail', kwargs={'slug': self.slug})

    def get_description(self):
        """
        Returns the first available text from either the excerpt or
        content placeholder.

        """
        content = ''
        for plugin in self.excerpt.get_plugins():
            try:
                if plugin.text.language == get_language():
                    content = plugin.text.body
            except:
                pass
            if content:
                break
        if not content:
            for plugin in self.content.get_plugins():
                try:
                    if plugin.text.language == get_language():
                        content = plugin.text.body
                except:
                    pass
                if content:
                    break

        # remove html tags and escape the rest
        pattern = re.compile('<.*?>')
        content = pattern.sub('', content)
        text = escape(content)
        return text

    def get_preview_url(self):
        slug = self.slug
        return reverse('news_preview', kwargs={'slug': slug})

    def is_public(self):
        """
        Returns True, if the entry is considered public.

        """
        return self.is_published and (
            self.pub_date is None or self.pub_date <= now())

    def save(self, *args, **kwargs):
        if self.is_published and self.pub_date is None:
            self.pub_date = now()
        super(NewsEntry, self).save(*args, **kwargs)


class RecentPlugin(CMSPlugin):
    """Plugin model to display recent news."""
    limit = models.PositiveIntegerField(
        verbose_name=_('Maximum news amount'),
    )
    current_language_only = models.BooleanField(
        verbose_name=_('Only show entries for the selected language'),
    )
