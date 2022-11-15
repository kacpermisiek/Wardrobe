import os.path
from django.http import Http404
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
from .forms import ItemReservationForm, SetTemplateForm, SetForm


def home(request):
    context = {
        'sets': SetTemplate.objects.all(),
        'title': 'strona główna'
    }
    if request.user.is_superuser:
        context['curr_set'] = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)
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


class ItemTemplateDeleteView(UserPassesTestMixin, DeleteView):
    model = ItemTemplate
    template_name = 'stuff/item_template/confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        messages.success(self.request, "Szablon przedmiotu został usunięty")
        return '/'


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


class SetTemplateDetailView(LoginRequiredMixin, DetailView):
    model = SetTemplate
    template_name = 'stuff/set_template/details.html'

    def get_context_data(self, **kwargs):
        context = super(SetTemplateDetailView, self).get_context_data(**kwargs)
        context['sets'] = Set.objects.filter(set_template_id=self.object.id).order_by('id')
        return context


class SetTemplateDeleteView(UserPassesTestMixin, DeleteView):
    model = SetTemplate
    template_name = 'stuff/set_template/confirm_delete.html'
    success_url = '/'

    def test_func(self):
        return self.request.user.is_superuser


class SetTemplateUpdateView(UserPassesTestMixin, UpdateView):
    model = SetTemplate
    fields = ['name']
    template_name = 'stuff/set_template/update.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return os.path.join('/set_template/', str(self.object.id))


def add_item_template_to_set_template(request, template_id):
    if request.user.is_superuser:
        set_template = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)

        if _item_template_is_already_in_set_template(template_id, set_template):
            _increment_required_item_quantity(set_template, template_id)
        else:
            _create_new_required_item(set_template, template_id)

        set_template.save()
        messages.success(request, "Przedmiot został dodany do zestawu!")
        return home(request)
    return Http404()


def set_current_set_template(request, pk):
    if request.user.is_superuser:
        user = User.objects.get(id=request.user.id)
        user.profile.set_template_curr_index(pk)
        user.save()
        messages.success(request, "Szablon zestawu został ustawiony jako aktualnie edytowany")
        return home(request)
    return Http404()


def _create_new_required_item(set_template, template_id):
    new_item_required = ItemRequired.objects.create(
        item_type_id=template_id,
        quantity_required=1
    )
    set_template.items_required.add(new_item_required)
    new_item_required.save()


def _increment_required_item_quantity(set_template, template_id):
    item_required = set_template.items_required.get(item_type_id=template_id)
    item_required.quantity_required += 1
    item_required.save()


def _item_template_is_already_in_set_template(item_template_id, set_template):
    return set_template.items_required.filter(item_type_id=item_template_id).exists()


def remove_item_template_from_set_template(request, template_id):
    set_template = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)
    item_required = set_template.items_required.filter(item_type_id=template_id).first()
    set_template.items_required.remove(item_required)
    set_template.save()
    messages.success(request, "Przedmiot został usunięty z szablonu")
    return home(request)


def decrement_required_item_quantity(request, template_id):
    if request.user.is_superuser:
        set_template = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)
        item_required = set_template.items_required.filter(item_type_id=template_id).first()
        if item_required.quantity_required <= 1:
            return remove_item_template_from_set_template(request, template_id)
        item_required.quantity_required -= 1
        item_required.save()
        messages.success(request, "Potrzebna ilość do tego szablonu została zmniejszona")
        return home(request)
    return Http404


class SetCreateView(UserPassesTestMixin, CreateView):
    model = Set
    template_name = 'stuff/set/create.html'
    success_url = '/'
    form_class = SetForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('set-template-detail', kwargs={'pk': self.object.set_template.id})

    def get_form_kwargs(self):
        kwargs = super(SetCreateView, self).get_form_kwargs()
        kwargs['set_template_id'] = self.kwargs.get('set_template_id')
        kwargs.update()
        return kwargs

    def form_valid(self, form):
        form.instance.set_template = SetTemplate.objects.get(id=self.kwargs.get('set_template_id'))
        return super(SetCreateView, self).form_valid(form)


class SetDetailView(DetailView):
    model = Set
    template_name = 'stuff/set/detail.html'


class SetDeleteView(UserPassesTestMixin, DeleteView):
    model = Set
    template_name = 'stuff/set/confirm_delete.html'

    def form_valid(self, form):
        deleted_set = self.get_object()
        items_belongs_to_set = deleted_set.items.all()
        for item in items_belongs_to_set:
            item.belongs_to_set = False
            item.save()
        return super(SetDeleteView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('set-template-detail', kwargs={'pk': self.object.set_template.id})


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
