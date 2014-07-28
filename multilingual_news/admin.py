"""Admin classes for the ``multilingual_news`` app."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

try:
    from cms.admin.placeholderadmin import FrontendEditableAdmin
except ImportError:
    class Object(object):
        pass
    FrontendEditableAdmin = Object

from cms.admin.placeholderadmin import PlaceholderAdmin
from document_library.admin import AttachmentInline
from hvad.admin import TranslatableAdmin
from multilingual_tags.admin import TaggedItemInline

from .models import Category, NewsEntry


class CategoryAdmin(TranslatableAdmin):
    list_display = ['get_title', 'hide_on_list', 'all_translations', ]

    def get_title(self, obj):
        return obj.title
    get_title.short_description = _('Title')


class NewsEntryAdmin(TranslatableAdmin,
                     FrontendEditableAdmin,
                     PlaceholderAdmin):
    """Admin class for the ``NewsEntry`` model."""
    inlines = [AttachmentInline, TaggedItemInline]
    list_display = [
        'get_title', 'pub_date', 'author', 'get_is_published',
        'get_categories', 'all_translations']

    def __init__(self, *args, **kwargs):
        super(NewsEntryAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ('title', )}

    def get_is_published(self, obj):
        return obj.is_published
    get_is_published.short_description = _('Is published')

    def get_title(self, obj):
        return obj.title
    get_title.short_description = _('Title')

    def get_categories(self, obj):
        return ', '.join(str(c.title) for c in obj.categories.all())
    get_title.short_description = _('Categories')


admin.site.register(Category, CategoryAdmin)
admin.site.register(NewsEntry, NewsEntryAdmin)
