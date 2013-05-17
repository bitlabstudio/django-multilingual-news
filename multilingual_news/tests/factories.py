"""Factories for the ``multilingual_news`` app."""
import factory

from cms.models import Placeholder
from cms.plugins.text.models import Text

from ..models import NewsEntry, NewsEntryTitle
from .test_app.models import DummyModel


class DummyModelFactory(factory.Factory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel


class PlaceholderFactory(factory.Factory):
    """Factory for the ``Placeholder`` model."""
    FACTORY_FOR = Placeholder


class TextPluginFactory(factory.Factory):
    """Factory for the ``Text`` model."""
    FACTORY_FOR = Text

    body = 'foo bar'
    language = 'en'
    plugin_type = 'TextPlugin'
    placeholder = factory.SubFactory(PlaceholderFactory)


class NewsEntryFactory(factory.Factory):
    """Factory for the ``NewsEntry`` model."""
    FACTORY_FOR = NewsEntry


class NewsEntryTitleFactoryBase(factory.Factory):
    """Base factory for factories for ``NewsEntryTitle`` models."""
    FACTORY_FOR = NewsEntryTitle

    entry = factory.SubFactory(NewsEntryFactory)
    is_published = True


class NewsEntryTitleENFactory(NewsEntryTitleFactoryBase):
    """Factory for english ``NewsEntryTitle`` objects."""
    title = factory.Sequence(lambda x: 'A title {0}'.format(x))
    slug = factory.Sequence(lambda x: 'a-title-{0}'.format(x))
    language = 'en'


class NewsEntryTitleDEFactory(NewsEntryTitleFactoryBase):
    """Factory for german ``NewsEntryTitle`` objects."""
    title = factory.Sequence(lambda x: 'Ein Titel {0}'.format(x))
    slug = factory.Sequence(lambda x: 'ein-titel-{0}'.format(x))
    language = 'de'
