"""Settings of the ``multilingual_news``` application."""
from django.conf import settings

PAGINATION_AMOUNT = getattr(settings, 'NEWS_PAGINATION_AMOUNT', 10)
