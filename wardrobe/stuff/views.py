from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from stuff.models import Item, BADGE_STATUSES


def home(request):

    def _get_badge_status(status):
        return BADGE_STATUSES[status]

    def _set_badge_statuses(items):
        for item in items:
            try:
                item.badge_status = _get_badge_status(item.status)
            except KeyError:
                item.badge_status = 'dark'

        return items

    def _get_items():
        return _set_badge_statuses(Item.objects.all())

    context = {
        'stuff': _get_items(),
        'title': 'strona główna'
    }
    return render(request, 'stuff/home.html', context)


class ItemListView(ListView):
    model = Item
    template_name = 'stuff/home.html'
    context_object_name = 'stuff'
    ordering = ['status', 'name']
    # TODO: status colors are not working since ItemListView addition


class ItemDetailView(DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Item
    fields = ['name', 'description', 'category', 'status']


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['name', 'description', 'category', 'status']

    def test_func(self):
        return self.request.user.is_superuser

    # TODO handle_no_permission is not working correctly, when user have no permission it gets 403


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'stuff/about.html', context)
