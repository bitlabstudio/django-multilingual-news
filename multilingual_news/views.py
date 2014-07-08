"""Views for the ``multilingual_news`` app."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.generic import (
    DateDetailView,
    DeleteView,
    DetailView,
    ListView,
    View,
)

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


class DeleteNewsEntryView(DeleteView):
    """View where staff can delete entries."""
    ajax_template_name = 'multilingual_news/partials/newsentry_delete.html'
    template_name = 'multilingual_news/newsentry_delete.html'
    model = NewsEntry

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            raise Http404
        self.object = self.get_object()
        return super(DeleteNewsEntryView, self).dispatch(
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object.delete()
        if request.is_ajax():
            context = {
                'deleted': True,
                'redirect_url': self.get_success_url(),
            }
            return HttpResponse(context)
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('news_list')

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        else:
            return super(DeleteNewsEntryView, self).get_template_names()


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
        hidden_categories = Category.objects.filter(hide_on_list=True)
        kwargs = {'categories__in': hidden_categories}
        if self.request.user.is_superuser:
            return NewsEntry.objects.exclude(**kwargs)
        return NewsEntry.objects.published(exclude_kwargs=kwargs)


class PublishNewsEntryView(View):
    """View to publish a NewsEntry."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            if not self.request.user.is_superuser:
                raise Http404
            try:
                self.object = NewsEntry.objects.get(pk=kwargs.get('pk'))
            except NewsEntry.DoesNotExist:
                raise Http404
        return super(PublishNewsEntryView, self).dispatch(
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action', None)
        if action == 'publish':
            self.object.is_published = True
            self.object.save()
        if action == 'unpublish':
            self.object.is_published = False
            self.object.save()
        return redirect(reverse('news_detail', kwargs={
            'slug': self.object.slug}))


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
