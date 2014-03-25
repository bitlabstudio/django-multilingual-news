"""Views for the ``multilingual_news`` app."""
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
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
        qs = NewsEntry.objects.published()
        if self.category:
            qs = qs.filter(
                Q(categories__slug=self.category) |
                Q(categories__parent__slug=self.category))
        if self.count:
            return qs[:self.count]
        return qs


class NewsListView(ListView):
    """View to display all published and visible news entries."""
    paginate_by = PAGINATION_AMOUNT
    template_name = 'multilingual_news/newsentry_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return NewsEntry.objects.all()
        return NewsEntry.objects.published()


class TaggedNewsListView(ListView):
    """
    View to display all published and visible news entries for a specific tag.

    """
    paginate_by = PAGINATION_AMOUNT
    template_name = 'multilingual_news/newsentry_list.html'

    def get_queryset(self):
        return NewsEntry.objects.language(get_language()).filter(
            tags__tag__slug=self.kwargs.get('tag'))


class DetailViewMixin(object):
    """Mixin to handle different DetailView variations."""
    model = NewsEntry
    slug_field = 'slug'

    def get_queryset(self, **kwargs):
        return NewsEntry.objects.language(get_language())


class NewsDateDetailView(DetailViewMixin, DateDetailView):
    """View to display one news entry with publication date."""
    date_field = 'pub_date'
    month_format = '%m'


class NewsDetailView(DetailViewMixin, DetailView):
    """View to display one news entry without publication date."""
    pass


class NewsDetailPreviewView(NewsDetailView):
    """View to display one news entry that is not public yet."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            raise Http404
        return super(NewsDetailPreviewView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(NewsDetailPreviewView, self).get_context_data(**kwargs)
        ctx.update({'preview': 1})
        return ctx
