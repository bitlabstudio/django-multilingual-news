"""CMS apphook for the ``multilingual_news`` app."""
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class MultilingualNewsApphook(CMSApp):
    name = _("Multilingual News Apphook")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["multilingual_news.urls"]


apphook_pool.register(MultilingualNewsApphook)
