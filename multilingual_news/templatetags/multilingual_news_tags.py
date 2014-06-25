"""Template tags for the ``multilingual_news`` app."""
import warnings

from django import template
from django.template.defaultfilters import safe, truncatewords_html

from ..models import NewsEntry, Category


register = template.Library()


@register.assignment_tag
def get_published_entries(object_list, language_code=None):
    return NewsEntry.objects.published(language=language_code)


@register.simple_tag
def get_newsentry_meta_description(newsentry):
    """Returns the meta description for the given entry."""
    if newsentry.meta_description:
        return newsentry.meta_description

    # If there is no seo addon found, take the info from the placeholders
    text = newsentry.get_description()

    if len(text) > 160:
        return u'{}...'.format(text[:160])
    return text


@register.simple_tag
def get_newsentry_meta_title(newsentry):
    return newsentry.meta_title or newsentry.title


@register.assignment_tag(takes_context=True)
def get_recent_news(context, check_language=True, limit=3, exclude=None,
                    category=None):
    filter_kwargs = {
        'check_language': check_language,
        'limit': limit,
        'exclude': exclude,
    }
    try:
        filter_kwargs['category'] = Category.objects.get(slug=category)
    except Category.DoesNotExist:
        pass
    qs = NewsEntry.objects.recent(**filter_kwargs)
    return qs


@register.simple_tag(takes_context=True)
def render_news_placeholder(context, obj, name=False, truncate=False):  # pragma: nocover  # NOQA
    """
    DEPRECATED: Template tag to render a placeholder from an NewsEntry object

    We don't need this any more because we don't have a placeholders M2M field
    on the model any more. Just use the default ``render_placeholder`` tag.

    """
    warnings.warn(
        "render_news_placeholder is deprecated. Use render_placeholder"
        " instead", DeprecationWarning, stacklevel=2)
    result = ''
    if context.get('request'):
        if isinstance(name, int):
            # If the user doesn't want to use a placeholder name, but a cut, we
            # need to check if the user has used the name as a number
            truncate = name
            name = False
        if name:
            # If the name of the placeholder slot is given, get, render and
            # return it!
            try:
                result = safe(getattr(obj, name).render(context, None))
            except AttributeError:
                pass
        else:
            # If no name is provided get the first placeholder with content
            for name in ['excerpt', 'content']:
                rendered = ''
                try:
                    rendered = safe(getattr(obj, name).render(context, None))
                except AttributeError:
                    pass
                if rendered:
                    result = rendered
                    break
    if truncate:
        return truncatewords_html(result, truncate)
    return result
