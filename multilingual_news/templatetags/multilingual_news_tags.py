"""Template tags for the ``multilingual_news`` app."""
from django import template
from django.core.exceptions import ObjectDoesNotExist
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
    Template tag to render a placeholder from an object, which has a
    placeholders many-to-many-field.

    """
    result = ''
    if context.get('request') and hasattr(obj, 'placeholders'):
        if isinstance(name, int):
            # If the user doesn't want to use a placeholder name, but a cut, we
            # need to check if the user has used the name as a number
            truncate = name
            name = False
        if name:
            # If the name of the placeholder slot is given, get, render and
            # return it!
            try:
                result = safe(obj.placeholders.get(slot=name).render(
                    context, None))
            except ObjectDoesNotExist:
                pass
        else:
            # If no name is provided get the first placeholder with content
            for placeholder in obj.placeholders.all():
                rendered = safe(placeholder.render(context, None))
                if rendered:
                    result = rendered
                    break
    if truncate:
        return truncatewords_html(result, truncate)
    return result
