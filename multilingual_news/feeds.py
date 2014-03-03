"""RSS feeds for the `multilingual_news` app."""
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from cms.utils import get_language_from_request
from people.models import Person

from .models import NewsEntry


def is_multilingual():
    return 'django.middleware.locale.LocaleMiddleware' in \
        settings.MIDDLEWARE_CLASSES


def get_lang_name(lang):
    return _(dict(settings.LANGUAGES)[lang])


class NewsEntriesFeed(Feed):
    """A news feed, that shows all entries."""
    title_template = 'multilingual_news/feed/entries_title.html'
    description_template = 'multilingual_news/feed/entries_description.html'

    def get_object(self, request, **kwargs):
        self.language_code = get_language_from_request(request)
        self.site = get_current_site(request)
        self.any_language = kwargs.get('any_language', None)

    def feed_url(self, item):
        if is_multilingual() or self.any_language:
            return reverse('blog_rss_any', kwargs={'any_language': True})
        return reverse('blog_rss')

    def title(self, item):
        if self.any_language or not is_multilingual():
            return _(u"{0} blog entries".format(self.site.name))
        return _(u"{0} blog entries in {1}".format(self.site.name,
                 get_lang_name(self.language_code)))

    def link(self, item):
        return reverse('news_list')

    def item_link(self, item):
        return item.get_absolute_url()

    def description(self, item):
        if self.any_language or not is_multilingual():
            return _(u"{0} blog entries".format(self.site.name))
        return _(u"{0} blog entries in {1}".format(self.site.name,
                 get_lang_name(self.language_code)))

    def get_queryset(self, item):
        if not is_multilingual() or self.any_language:
            check_language = False
        else:
            check_language = True
        return NewsEntry.objects.recent(limit=10,
                                        check_language=check_language)

    def items(self, item):
        return self.get_queryset(item)

    def item_pubdate(self, item):
        return item.pub_date


class AuthorFeed(NewsEntriesFeed):
    """A news feed, that shows only entries from a certain author."""
    title_template = 'multilingual_news/feed/author_title.html'
    description_template = 'multilingual_news/feed/author_description.html'

    def get_object(self, request, **kwargs):
        super(AuthorFeed, self).get_object(request, **kwargs)
        # Needs no try. If the author does not exist, we automatically get a
        # 404 response.
        self.author = Person.objects.get(pk=kwargs.get('author'))

    def title(self, obj):
        title = super(AuthorFeed, self).title(obj)
        return _(u'{0} by {1}'.format(title, self.author))

    def feed_url(self, obj):
        if is_multilingual() or self.any_language:
            return reverse('blog_rss_any_author', kwargs={
                'author': self.author.id, 'any_language': True})
        return reverse('blog_rss_author', kwargs={'author': self.author.id})

    def link(self, obj):
        # TODO Author specific archive
        return reverse('news_list')

    def description(self, obj):
        description = super(AuthorFeed, self).description(obj)
        return _(u'{0} by {1}'.format(description, self.author))

    def get_queryset(self, obj):
        if not is_multilingual() or self.any_language:
            check_language = False
        else:
            check_language = True
        return NewsEntry.objects.recent(limit=10,
                                        check_language=check_language,
                                        kwargs={'author': self.author})
