"""Template tags for the ``multilingual_news`` app."""
import warnings

from django import template
from django.template.defaultfilters import safe, truncatewords_html

from ..models import NewsEntry


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_recent_news(context, check_language=True, limit=3, exclude=None):
    qs = NewsEntry.objects.recent(
        context['request'],
        check_language=check_language,
        limit=limit,
        exclude=exclude)
    return qs


@register.simple_tag(takes_context=True)
def render_news_placeholder(context, obj, name=False, truncate=False):
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
