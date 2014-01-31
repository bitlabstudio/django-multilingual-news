"""Views for the ``multilingual_news`` app."""
from django.views.generic import DateDetailView, DetailView, ListView

from .app_settings import PAGINATION_AMOUNT
from .models import NewsEntry


class NewsListView(ListView):
    """View to display all published and visible news entries."""
    paginate_by = PAGINATION_AMOUNT

    def get_queryset(self):
        return NewsEntry.objects.published(self.request)


class DetailViewMixin(object):
    """Mixin to handle different DetailView variations."""
    model = NewsEntry
    slug_field = 'translations__slug'

    def get_queryset(self):
        return NewsEntry.objects.published(self.request, False)


class NewsDateDetailView(DetailViewMixin, DateDetailView):
    """View to display one news entry with publication date."""
    date_field = 'pub_date'
    month_format = '%m'


class NewsDetailView(DetailViewMixin, DetailView):
    """View to display one news entry without publication date."""
    pass
