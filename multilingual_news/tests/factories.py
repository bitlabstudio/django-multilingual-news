"""Factories for the ``multilingual_news`` app."""
import factory

from cms.models import Placeholder

from django_libs.tests.factories import HvadFactoryMixin
from djangocms_text_ckeditor.models import Text

from .. import models
from .test_app.models import DummyModel


class DummyModelFactory(factory.DjangoModelFactory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel


class CategoryFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    """Factory for the ``Category`` model."""
    FACTORY_FOR = models.Category

    slug = factory.Sequence(lambda n: 'slug-{0}'.format(n))
    title = factory.Sequence(lambda n: 'title {0}'.format(n))
    language_code = 'en'


class PlaceholderFactory(factory.DjangoModelFactory):
    """Factory for the ``Placeholder`` model."""
    FACTORY_FOR = Placeholder


class TextPluginFactory(factory.DjangoModelFactory):
    """Factory for the ``Text`` model."""
    FACTORY_FOR = Text

    body = 'foo bar'
    language = 'en'
    plugin_type = 'TextPlugin'
    placeholder = factory.SubFactory(PlaceholderFactory)


class NewsEntryFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    """Factory for the ``NewsEntry`` model."""
    FACTORY_FOR = models.NewsEntry

    language_code = 'en'
    title = factory.Sequence(lambda x: 'A title {0}'.format(x))
    slug = factory.Sequence(lambda x: 'a-title-{0}'.format(x))
    is_published = True
