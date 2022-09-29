from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from stuff.models import Item, User, ReservationEvent, BADGE_STATUSES
from .forms import ItemReservationForm


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
    paginate_by = 6


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


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/'

    def test_func(self):
        return self.request.user.is_superuser


class ItemCreateReservationView(LoginRequiredMixin, CreateView):
    model = ReservationEvent
    template_name = 'reservation/reservation_create.html'
    success_url = '/'
    form_class = ItemReservationForm

    def get_form(self, **kwargs):
        form = super(ItemCreateReservationView, self).get_form(self.form_class)
        form.instance.item = Item.objects.get(pk=self.kwargs.get('pk', None))
        return form
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreateReservationView, self).form_valid(form)


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'stuff/about.html', context)
