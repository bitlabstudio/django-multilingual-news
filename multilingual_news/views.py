"""Views for the ``multilingual_news`` app."""
from django.db.models import Q
from django.views.generic import DateDetailView, DetailView, ListView

from .app_settings import PAGINATION_AMOUNT
from .models import Category, NewsEntry


class CategoryListView(ListView):
    template_name = 'multilingual_news/newsentry_archive_category.html'
    context_object_name = 'newsentries'

    def dispatch(self, request, *args, **kwargs):
        self.category = Category.objects.get(slug=kwargs.get('category'))
        return super(CategoryListView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CategoryListView, self).get_context_data(**kwargs)
        ctx.update({'category': self.category, })
        return ctx

    def get_queryset(self):
        return self.category.get_entries()


class GetEntriesAjaxView(ListView):
    template_name = 'multilingual_news/partials/entry_list.html'
    context_object_name = 'entries'

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('category'):
            self.category = request.GET.get('category')
        else:
            self.category = None
        if request.GET.get('count'):
            self.count = int(request.GET.get('count'))
        else:
            self.count = None
        return super(GetEntriesAjaxView, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        qs = NewsEntry.objects.published(self.request)
        if self.category:
            qs = qs.filter(
                Q(category__slug=self.category) |
                Q(category__parent__slug=self.category))
        if self.count:
            return qs[:self.count]
        return qs


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
