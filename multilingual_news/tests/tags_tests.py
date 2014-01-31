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
