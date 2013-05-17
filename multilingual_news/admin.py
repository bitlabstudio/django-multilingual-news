"""Admin classes for the ``multilingual_news`` app."""
from django.conf import settings
from django.contrib import admin
from django.forms import CharField
from django.http import HttpResponse
from django.template.defaultfilters import title
from django.utils.text import capfirst
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from cms.forms.widgets import PlaceholderPluginEditorWidget
from cms.models.pluginmodel import CMSPlugin
from simple_translation.admin import PlaceholderTranslationAdmin
from simple_translation.utils import get_preferred_translation_from_lang

from .models import NewsEntry


class M2MPlaceholderAdmin(PlaceholderTranslationAdmin):
    """Custom PlaceholderAdmin to handle m2m placeholders."""
    def get_form(self, request, obj=None, **kwargs):
        """Get placeholder form and prepare placeholder fields."""
        form = super(M2MPlaceholderAdmin, self).get_form(request, obj,
                                                         **kwargs)
        if obj:
            # Get or create placeholder instances
            for placeholder_name in obj._meta.get_field(
                    'placeholders').placeholders:

                placeholder, created = obj.placeholders.get_or_create(
                    slot=placeholder_name)

                defaults = {'label': capfirst(placeholder_name),
                            'help_text': ''}
                defaults.update(kwargs)

                widget = PlaceholderPluginEditorWidget(
                    request, self.placeholder_plugin_filter)
                widget.choices = []
                form.base_fields[placeholder.slot] = CharField(widget=widget,
                                                               required=False)
                form.base_fields[placeholder.slot].initial = placeholder.pk
        return form

    def get_fieldsets(self, request, obj=None):
        """
        Add fieldsets of placeholders to the list of already existing
        fieldsets.

        """
        given_fieldsets = super(M2MPlaceholderAdmin, self).get_fieldsets(
            request, obj=None)

        if obj:
            for placeholder_name in obj._meta.get_field(
                    'placeholders').placeholders:
                given_fieldsets += [(title(placeholder_name),
                                     {'fields': [placeholder_name],
                                      'classes': ['plugin-holder']})]
        return given_fieldsets

    def move_plugin(self, request):
        """Function to handle drag & drop of plugins within placeholders."""
        # def get_placeholder(plugin, request):
        #     return plugin.placeholder

        # only allow POST
        if request.method != "POST" or not 'ids' in request.POST:
            return HttpResponse(str("error"))

        if 'plugin_id' in request.POST:
            # Get plugin and aimed placeholder
            plugin = CMSPlugin.objects.get(pk=int(request.POST['plugin_id']))
            if 'placeholder' in request.POST:
                obj = plugin.placeholder._get_attached_model().objects.get(
                    placeholders__cmsplugin=plugin)
                placeholder = obj.placeholders.get(
                    slot=request.POST["placeholder"])
            else:
                placeholder = plugin.placeholder
            # plugin positions are 0 based, so just using count here should
            # give us 'last_position + 1'
            position = CMSPlugin.objects.filter(
                placeholder=placeholder).count()
            plugin.placeholder = placeholder
            plugin.position = position
            plugin.save()

        # Update plugin positions
        pos = 0
        for id in request.POST['ids'].split("_"):
            plugin = CMSPlugin.objects.get(pk=id)
            if plugin.position != pos:
                plugin.position = pos
                plugin.save()
            pos += 1
        return HttpResponse(str("ok"))


class NewsEntryAdmin(M2MPlaceholderAdmin):
    """Admin class for the ``NewsEntry`` model."""
    list_display = ['title', 'author', 'pub_date', 'is_published']

    def title(self, obj):
        lang = get_language()
        return get_preferred_translation_from_lang(obj, lang).title
    title.short_description = _('Title')

    def is_published(self, obj):
        lang = get_language()
        return get_preferred_translation_from_lang(obj, lang).is_published
    title.short_description = _('Is published')

    class Media:
        js = (
            settings.STATIC_URL + 'multilingual_blog/js/news.js',
            settings.STATIC_URL + 'admin/js/urlify.js',
        )


admin.site.register(NewsEntry, NewsEntryAdmin)
