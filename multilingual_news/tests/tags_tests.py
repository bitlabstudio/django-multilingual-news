"""Tests for tags of the ``multilingual_news``` application."""
from mock import Mock

from django.contrib.sessions.middleware import SessionMiddleware
from django.template.context import RequestContext
from django.test import TestCase
from django.test.client import RequestFactory

from ..templatetags.multilingual_news_tags import (
    get_recent_news,
    render_news_placeholder,
)
from .factories import (
    NewsEntryFactory,
    NewsEntryTitleENFactory,
    PlaceholderFactory,
    TextPluginFactory,
)


class GetRecentNewsTestCase(TestCase):
    """Tests for the ``get_recent_news`` assignment tag."""
    longMessage = True

    def setUp(self):
        NewsEntryTitleENFactory()
        NewsEntryTitleENFactory()
        NewsEntryTitleENFactory()
        NewsEntryTitleENFactory()

    def test_tag(self):
        req = RequestFactory().get('/')
        context = {'request': req, }
        result = get_recent_news(context)
        self.assertEqual(result.count(), 3, msg=(
            'Should return last three recent news'))


class RenderNewsPlaceholderTestCase(TestCase):
    """Tests for the ``render_news_placeholder`` tag."""
    longMessage = True

    def test_tag(self):
        # create context mock
        request = RequestFactory().get('/')
        SessionMiddleware().process_request(request)
        request.session.save()
        context = RequestContext(request)
        entry = NewsEntryFactory()

        self.assertEqual(render_news_placeholder(context, entry), '', msg=(
            'Returns empty string, if there are no placeholders.'))

        self.assertEqual(render_news_placeholder(context, entry, 'foo'), '',
                         msg=('Returns empty string, if the requested slot'
                              ' does not exist.'))

        entry.placeholders.add(PlaceholderFactory(slot='excerpt'))
        self.assertEqual(render_news_placeholder(context, entry), '', msg=(
            'Returns empty string, if there is no placeholder with content.'))

        cmsplugin = TextPluginFactory()
        entry.placeholders.add(cmsplugin.placeholder)
        self.assertEqual(render_news_placeholder(context, entry), 'foo bar',
                         msg=('Returns rendered placeholder content.'))

        self.assertEqual(render_news_placeholder(context, entry, 1), 'foo ...',
                         msg=('Returns rendered and truncated content.'))
