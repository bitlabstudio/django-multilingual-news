"""Views for the ``multilingual_news`` app."""
from django.http import Http404, HttpResponseRedirect
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

    def dispatch(self, request, *args, **kwargs):
        """
        We want to see the slug in the url, but the slug rests in the
        translated NewsEntryTitle model. So we kid the view and tell it to use
        a slug instead of a pk, then get the relevant NewsEntry and provide its
        pk.

        """
        if not self.queryset:
            self.queryset = NewsEntry.objects.published(request, False)
        self.kwargs = kwargs
        try:
            result = self.queryset.get(newsentrytitle__slug=self.kwargs.get(
                'slug'))
        except NewsEntry.DoesNotExist:
            raise Http404
        else:
            if result.get_slug() != self.kwargs.get('slug'):
                return HttpResponseRedirect(result.get_absolute_url())
            self.kwargs.update({'pk': result.pk})
            del self.kwargs['slug']
        return super(DetailViewMixin, self).dispatch(request, *args, **kwargs)


class NewsDateDetailView(DetailViewMixin, DateDetailView):
    """View to display one news entry with publication date."""
    date_field = 'pub_date'
    month_format = '%m'


class NewsDetailView(DetailViewMixin, DetailView):
    """View to display one news entry without publication date."""
    pass
