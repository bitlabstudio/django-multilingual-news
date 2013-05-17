"""Registration of models for simple-translation."""
from simple_translation.translation_pool import translation_pool

from .models import NewsEntry, NewsEntryTitle


translation_pool.register_translation(NewsEntry, NewsEntryTitle)
