"""cmsplugins for the ``multilingual_news`` app."""
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.utils import get_language_from_request

from simple_translation.utils import get_translation_filter_language

from .models import NewsEntry, RecentPlugin


class CMSRecentPlugin(CMSPluginBase):
    """django-cms plugin to display recent news."""
    model = RecentPlugin
    name = _('Recent News')
    render_template = "multilingual_news/recent.html"

    def render(self, context, instance, placeholder):
        qs = NewsEntry.objects.published(context['request'])

        if instance.current_language_only:
            # Filter news with current language
            language = get_language_from_request(context['request'])
            kwargs = get_translation_filter_language(NewsEntry, language)
            qs = qs.filter(**kwargs)

        context.update({'object_list': qs[:instance.limit]})
        return context

plugin_pool.register_plugin(CMSRecentPlugin)
