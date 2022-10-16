from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Item, Category, ReservationEvent, BADGE_STATUSES
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


class CategoryListView(ListView):
    model = Category
    template_name = 'stuff/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']


class CategoryDetailView(DetailView):
    model = Category


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Category
    fields = ['name']
    template_name = 'stuff/category_create.html'
    success_url = '/category'


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']
    success_url = '/category'

    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = '/category'

    def test_func(self):
        return self.request.user.is_superuser


class ItemListView(ListView):
    model = Item
    template_name = 'stuff/home.html'
    context_object_name = 'stuff'
    ordering = ['status', 'name']
    paginate_by = 6


class ItemDetailView(DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Item
    fields = ['name', 'description', 'category', 'status', 'image']


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['name', 'description', 'category', 'status', 'image']

    def test_func(self):
        return self.request.user.is_superuser


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/'

    def test_func(self):
        return self.request.user.is_superuser


class ReservationListView(ListView):
    model = ReservationEvent
    template_name = 'reservation/reservations.html'
    context_object_name = 'reservations'
    paginate_by = 6

    def get_queryset(self):
        return ReservationEvent.objects.all().order_by('start_date')


class UserReservationsListView(ReservationListView):
    template_name = 'reservation/user_reservations.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return ReservationEvent.objects.filter(user=user).order_by('-start_date')


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'stuff/about.html', context)


class ItemDetailReservationView(DetailView):
    model = ReservationEvent

    template_name = 'reservation/reservation_detail.html'


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


class ItemUpdateReservationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReservationEvent
    template_name = 'reservation/reservation_update.html'
    success_url = '/item/reservations/'
    form_class = ItemReservationForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_form(self, **kwargs):
        form = super(ItemUpdateReservationView, self).get_form(self.form_class)
        form.instance.item = Item.objects.get(pk=self.kwargs.get('id', None))
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemUpdateReservationView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_range'] = self._dates_to_date_range((
            context['object'].start_date,
            context['object'].end_date
        ))
        print(context['object'].taken)
        return context

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateReservationView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

    def _dates_to_date_range(self, dates):
        result = []
        for date in dates:
            result.append(self._date_into_string(date))
        return f"{result[0]} - {result[1]}"

    @staticmethod
    def _date_into_string(date):
        return date.strftime("%d-%m-%Y")


class ItemDeleteReservationView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReservationEvent
    success_url = '/item/reservations/'
    template_name = 'reservation/reservation_delete.html'

    def test_func(self):
        return self.request.user.is_superuser
