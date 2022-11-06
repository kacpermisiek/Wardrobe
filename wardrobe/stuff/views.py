from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import (
    Item,
    Category,
    ReservationEvent,
    SetTemplate,
    Set,
    ItemTemplate,
    ItemRequired
)
from .forms import ItemReservationForm, SetTemplateForm


def home(request):
    context = {
        'sets': Set.objects.all(),
        'title': 'strona główna'
    }
    return render(request, 'stuff/home.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = 'stuff/category/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'stuff/category/category_form.html'


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Category
    fields = ['name']
    template_name = 'stuff/category/category_create.html'
    success_url = '/category'


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']
    success_url = '/category'
    template_name = 'stuff/category/category_form.html'

    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = '/category'
    template_name = 'stuff/category/category_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


class ItemTemplateCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = ItemTemplate
    fields = ['name', 'description', 'category', 'image']
    template_name = 'stuff/item_template/create.html'

    def get_success_url(self):
        return reverse('item-template-list')


class ItemTemplateListView(ListView):
    model = ItemTemplate
    context_object_name = 'item_templates'
    paginate_by = 6
    ordering = ['name']
    template_name = 'stuff/item_template/list.html'


class ItemTemplateDetailView(LoginRequiredMixin, DetailView):
    model = ItemTemplate
    template_name = 'stuff/item_template/detail.html'


class ItemTemplateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ItemTemplate
    fields = ['name', 'description', 'category', 'image']
    template_name = 'stuff/item_template/form.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('item-template-detail', kwargs={'pk': self.object.id})


class ItemListView(ListView):
    model = Item
    context_object_name = 'stuff'
    ordering = ['status', 'name']
    paginate_by = 6


class ItemDetailView(DetailView):
    model = Item
    template_name = 'stuff/item/detail.html'


class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Item
    fields = ['name', 'description', 'category', 'status', 'image']


def item_create(request, template_id):
    if request.user.is_superuser:
        template = ItemTemplate.objects.get(id=template_id)
        item = Item(type=template, status='Dostępny')
        item.save()
        messages.success(request, "Przedmiot został utworzony!")
        context = {
            'object': template
        }
        return render(request, 'stuff/item_template/detail.html', context)
    return Http404()


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['name', 'description', 'category', 'status', 'image']

    def test_func(self):
        return self.request.user.is_superuser


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'stuff/item/confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('item-template-detail', kwargs={'pk': self.object.type.id})


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


class SetListView(ListView):
    model = Set
    context_object_name = 'stuff'
    ordering = ['set_status']
    template_name = 'stuff/home.html'
    paginate_by = 6


class SetTemplateListView(ListView):
    model = SetTemplate
    ordering = ['name']
    context_object_name = 'sets'
    template_name = 'stuff/home.html'
    paginate_by = 6


class SetTemplateCreateView(UserPassesTestMixin, CreateView):
    model = SetTemplate
    template_name = 'stuff/set_template/create.html'
    success_url = '/'
    form_class = SetTemplateForm

    def test_func(self):
        return self.request.user.is_superuser


def add_item_template_to_set_template(request, template_id):
    if request.user.is_superuser:
        item_template = ItemTemplate.objects.get(id=template_id)
        usr_set_template = request.user.profile.curr_set_template

        if _is_already_in_user_set_template(item_template, request.user):
            _increment_required_item_quantity(usr_set_template, request.user, item_template)
        else:
            _create_required_item(item_template, request, usr_set_template)
        context = {
            'object': item_template
        }
        return render(request, 'stuff/item_template/detail.html', context)
    return Http404()


def _increment_required_item_quantity(usr_set_template, user, item):
    item_required = usr_set_template.items_required.get(user=user, item_type=item)
    item_required.quantity_required += 1
    item_required.save()


def _create_required_item(item_template, request, usr_set_template):
    item_required = ItemRequired.objects.create(
        quantity_required=1,
        item_type=item_template
    )
    usr_set_template.items_required.add(item_required)
    messages.success(request, "Przedmiot został utworzony!")


def _is_already_in_user_set_template(item_template, user):
    return ItemRequired.objects.filter(item_type=item_template, user=user).exists()


class ItemDetailReservationView(DetailView):
    model = ReservationEvent

    template_name = 'reservation/reservation_detail.html'
    pk_url_kwarg = 'id'


class ItemCreateReservationView(LoginRequiredMixin, CreateView):
    model = ReservationEvent
    template_name = 'reservation/reservation_create.html'
    success_url = '/'
    form_class = ItemReservationForm

    def get_form(self, **kwargs):
        form = super(ItemCreateReservationView, self).get_form(self.form_class)
        form.instance.item = get_object_or_404(Item, id=self.kwargs.get('pk'))
        return form

    def get_form_kwargs(self):
        kwargs = super(ItemCreateReservationView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreateReservationView, self).form_valid(form)


class ItemUpdateReservationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReservationEvent
    template_name = 'reservation/reservation_update.html'
    success_url = '/item/reservations/'
    form_class = ItemReservationForm
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.is_superuser

    def get_form(self, **kwargs):
        form = super(ItemUpdateReservationView, self).get_form(self.form_class)
        form.instance.item = Item.objects.get(pk=self.kwargs.get('pk', None))
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
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.is_superuser
