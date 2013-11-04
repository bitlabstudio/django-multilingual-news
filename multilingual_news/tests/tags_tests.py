"""Tests for tags of the ``multilingual_news``` application."""
from django.contrib.sessions.middleware import SessionMiddleware
from django.template.context import RequestContext
from django.test import TestCase
from django.test.client import RequestFactory

from ..templatetags.multilingual_news_tags import (
    get_recent_news,
    render_news_placeholder,
)
from . import factories


class GetRecentNewsTestCase(TestCase):
    """Tests for the ``get_recent_news`` assignment tag."""
    longMessage = True

    def setUp(self):
        factories.NewsEntryFactory()
        factories.NewsEntryFactory()
        factories.NewsEntryFactory()
        factories.NewsEntryFactory()

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
        request.current_page = None
        SessionMiddleware().process_request(request)
        request.session.save()
        context = RequestContext(request)
        entry = factories.NewsEntryFactory()

        self.assertEqual(render_news_placeholder(context, entry), '', msg=(
            'Returns empty string, if there are no placeholders.'))

        self.assertEqual(render_news_placeholder(context, entry, 'foo'), '',
                         msg=('Returns empty string, if the requested slot'
                              ' does not exist.'))

        entry.exerpt = factories.PlaceholderFactory(slot='excerpt')
        self.assertEqual(render_news_placeholder(context, entry), '', msg=(
            'Returns empty string, if there is no placeholder with content.'))

        cmsplugin = factories.TextPluginFactory()
        entry.content = cmsplugin.placeholder
        self.assertEqual(render_news_placeholder(context, entry), 'foo bar',
                         msg=('Returns rendered placeholder content.'))

        self.assertEqual(render_news_placeholder(context, entry, 1), 'foo ...',
                         msg=('Returns rendered and truncated content.'))
