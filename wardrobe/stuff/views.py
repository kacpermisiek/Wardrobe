import os.path
from collections import namedtuple
from datetime import datetime

from django.core.mail import send_mail, BadHeaderError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.db.models import Q
from .forms import ReservationConfirmForm, SetRequestForm
from .models import (
    Item,
    Category,
    ReservationEvent,
    SetTemplate,
    Set,
    ItemTemplate,
    ItemRequired
)
from .forms import SetTemplateForm, SetForm, ReservationUpdateForm
from utils.forms_functions import request_method_is_post


SUPER_USERS_EMAILS = ["315560@uwr.edu.pl"]
if os.environ.get('RADWAS_EMAIL'):
    SUPER_USERS_EMAILS.append(os.environ.get('RADWAS_EMAIL'))


def home(request):
    if request.user.is_superuser:
        sets = SetTemplate.objects.all()
    else:
        sets = SetTemplate.objects.filter(Q(ready=True) | Q(created_by_id=request.user.id))
    context = {
        'sets': sets,
        'title': 'strona główna'
    }
    if request.user.is_staff:
        context['curr_set'] = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)
    return render(request, 'stuff/home.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = 'stuff/category/list.html'
    context_object_name = 'categories'
    ordering = ['name']


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'stuff/category/form.html'


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Category
    fields = ['name']
    template_name = 'stuff/category/create.html'
    success_url = '/category'


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']
    success_url = '/category'
    template_name = 'stuff/category/form.html'

    def test_func(self):
        return self.request.user.is_superuser


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = '/category'
    template_name = 'stuff/category/confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


class ItemTemplateCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_staff

    model = ItemTemplate
    fields = ['name', 'description', 'category', 'image']
    template_name = 'stuff/item_template/create.html'

    def get_success_url(self):
        return reverse('item-template-list')


class ItemTemplateListView(ListView):
    model = ItemTemplate
    context_object_name = 'item_templates'
    ordering = ['name']
    template_name = 'stuff/item_template/list.html'


class ItemTemplateFilterByCategoryView(ItemTemplateListView):
    template_name = 'stuff/item_template/list_filtered.html'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs.get('pk'))
        return ItemTemplate.objects.filter(category=category)


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
        messages.success(self.request, "Komponent został usunięty")
        return '/'


class ItemListView(ListView):
    model = Item
    context_object_name = 'stuff'
    ordering = ['status', 'name']
    paginate_by = 6


class ItemDetailView(DetailView):
    model = Item
    template_name = 'stuff/item/detail.html'


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
    template_name = 'reservation/list.html'
    context_object_name = 'reservations'
    paginate_by = 6

    def get_queryset(self):
        return ReservationEvent.objects.all().order_by('start_date')


class UserReservationsListView(ReservationListView):
    template_name = 'reservation/user_list.html'

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

    def get_queryset(self):
        return SetTemplate.objects.filter(ready=False)


class SetTemplateCreateView(UserPassesTestMixin, CreateView):
    model = SetTemplate
    template_name = 'stuff/set_template/create.html'
    success_url = '/'
    form_class = SetTemplateForm

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(SetTemplateCreateView, self).form_valid(form)


class SetTemplateDetailView(LoginRequiredMixin, ListView):
    model = Set
    template_name = 'stuff/set_template/details.html'
    context_object_name = 'sets'

    def get_context_data(self, **kwargs):
        context = super(SetTemplateDetailView, self).get_context_data(**kwargs)
        context['object'] = SetTemplate.objects.get(id=self.kwargs.get('pk', None))
        date_range = self.request.GET.get('date_range', None)
        if date_range:
            start_date, end_date = self._convert_date_range_into_dates(date_range)
            context['start_date'] = start_date.strftime('%d-%m-%Y')
            context['end_date'] = end_date.strftime('%d-%m-%Y')
        return context

    def get_queryset(self):
        date_range = self.request.GET.get('date_range', None)
        set_template_id = self.kwargs.get('pk', None)
        if date_range and set_template_id:
            return self._get_available_sets_in_date_range(set_template_id, date_range)
        if set_template_id and self.request.user.is_superuser:
            result = []
            sets = Set.objects.filter(set_template_id=set_template_id).all()
            for set in sets:
                result.append(set)
            return result
        return None

    def _get_available_sets_in_date_range(self, set_template_id, date_range):
        result = []
        start_date, end_date = self._convert_date_range_into_dates(date_range)
        sets = Set.objects.filter(set_template_id=set_template_id).all()

        for set in sets:
            if self.set_is_available(set, start_date, end_date):
                result.append(set)
        return result

    def _convert_date_range_into_dates(self, date_range):
        result = []
        for date_string in date_range.split(' - '):
            result.append(self._string_to_date(date_string))

        return tuple(result)

    @staticmethod
    def _string_to_date(date_string):
        return datetime.strptime(date_string, '%d-%m-%Y').date()

    def set_is_available(self, set, start_date, end_date):
        Range = namedtuple('Range', ['start', 'end'])
        r1 = Range(start_date, end_date)
        set_reservations = self._get_set_reservations(set)
        for reservation in set_reservations:
            r2 = Range(reservation.start_date, reservation.end_date)
            if self._dates_overlap(r1, r2):
                return False
        return True

    @staticmethod
    def _get_set_reservations(set):
        return ReservationEvent.objects.filter(set=set).all()

    def _dates_overlap(self, r1, r2):
        earliest_end, latest_start = self._get_timestamp(r1, r2)
        return ((earliest_end - latest_start).days + 1) > 0

    @staticmethod
    def _get_timestamp(r1, r2):
        return min(r1.end, r2.end), max(r1.start, r2.start)


class SetTemplateDeleteView(UserPassesTestMixin, DeleteView):
    model = SetTemplate
    template_name = 'stuff/set_template/confirm_delete.html'
    success_url = '/'

    def test_func(self):
        set_template_to_delete = self.get_object()
        return self.request.user.is_superuser or set_template_to_delete.created_by.id == self.request.user.id


class SetTemplateUpdateView(UserPassesTestMixin, UpdateView):
    model = SetTemplate
    fields = ['name', 'ready']
    template_name = 'stuff/set_template/update.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return os.path.join('/set_template/', str(self.object.id))


def add_item_template_to_set_template(request, template_id):
    if request.user.is_staff:
        set_template = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)

        if _item_template_is_already_in_set_template(template_id, set_template):
            _increment_required_item_quantity(set_template, template_id)
        else:
            _create_new_required_item(set_template, template_id)

        set_template.save()
        messages.success(request, "Przedmiot został dodany do zestawu!")
        return redirect('stuff-home')
    return Http404()


def set_current_set_template(request, pk):
    if request.user.is_staff:
        user = User.objects.get(id=request.user.id)
        user.profile.set_template_curr_index(pk)
        user.save()
        messages.success(request, "Szablon zestawu został ustawiony jako aktualnie edytowany")
        return redirect('stuff-home')
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
    return redirect('stuff-home')


def decrement_required_item_quantity(request, template_id):
    if request.user.is_staff:
        set_template = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)
        item_required = set_template.items_required.filter(item_type_id=template_id).first()
        if item_required.quantity_required <= 1:
            return remove_item_template_from_set_template(request, template_id)
        item_required.quantity_required -= 1
        item_required.save()
        messages.success(request, "Potrzebna ilość komponentów do tego szablonu została zmniejszona")
        return redirect('stuff-home')
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
        for item in deleted_set.items.all():
            item.item_set = None
            item.save()
        return super(SetDeleteView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('set-template-detail', kwargs={'pk': self.object.set_template.id})


class SetUpdateView(UserPassesTestMixin, UpdateView):
    model = Set
    template_name = 'stuff/set/create.html'

    form_class = SetForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super(SetUpdateView, self).get_form_kwargs()
        kwargs['set_id'] = self.kwargs.get('pk')
        kwargs.update()
        return kwargs

    def get_success_url(self):
        return reverse('set-template-detail', kwargs={'pk': self.object.set_template.id})


class ItemDetailReservationView(LoginRequiredMixin, DetailView):
    model = ReservationEvent

    template_name = 'reservation/detail.html'
    pk_url_kwarg = 'id'


class ReservationConfirmView(LoginRequiredMixin, CreateView):
    model = ReservationEvent
    template_name = 'reservation/confirm_create.html'
    form_class = ReservationConfirmForm

    def get_context_data(self, **kwargs):
        context_data = super(ReservationConfirmView, self).get_context_data(**kwargs)
        context_data['set'] = Set.objects.get(id=self.kwargs.get('set_id', None))
        context_data['start_date'] = self.kwargs.get('start_date', None)
        context_data['end_date'] = self.kwargs.get('end_date', None)
        return context_data

    def get_form_kwargs(self):
        kwargs = super(ReservationConfirmView, self).get_form_kwargs()
        kwargs['set'] = Set.objects.get(id=self.kwargs.get('set_id', None))
        kwargs['start_date'] = self.kwargs.get('start_date', None)
        kwargs['end_date'] = self.kwargs.get('end_date', None)
        kwargs.update()
        return kwargs

    def get_success_url(self):
        return reverse('set-template-detail', kwargs={'pk': self.object.set.set_template.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ReservationConfirmView, self).form_valid(form)


class ReservationListView(UserPassesTestMixin, ListView):
    model = ReservationEvent
    template_name = 'reservation/list.html'
    context_object_name = 'reservations'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return ReservationEvent.objects.all().order_by('start_date')


class UserReservationListView(ReservationListView):
    template_name = 'reservation/user_list.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def get_queryset(self):
        return ReservationEvent.objects.filter(user_id=self.request.user.id).order_by('start_date')


class ReservationDetailView(UserPassesTestMixin, DetailView):
    model = ReservationEvent
    template_name = 'reservation/detail.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.id == ReservationEvent.objects.get(id=self.kwargs.get('pk')).user.id


class ReservationUpdateView(UserPassesTestMixin, UpdateView):
    model = ReservationEvent
    template_name = 'reservation/update.html'
    form_class = ReservationUpdateForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_range'] = self._dates_to_date_range((
            context['object'].start_date,
            context['object'].end_date
        ))
        return context

    def get_form_kwargs(self):
        kwargs = super(ReservationUpdateView, self).get_form_kwargs()
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

    def get_success_url(self):
        return reverse('reservation-list')


class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReservationEvent
    template_name = 'reservation/delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('reservation-list')


def set_request(request, pk, start_date, end_date):
    if request_method_is_post(request.method):
        subject = 'wardrobe - brakujący zestaw'
        message = request.POST.get('message', None)

        context = {}
        if request.user.is_superuser:
            context['curr_set'] = SetTemplate.objects.get(id=request.user.profile.current_set_template_index)

        try:
            send_mail(subject, message, request.user.email, SUPER_USERS_EMAILS)
        except BadHeaderError:
            messages.error(request, 'Coś poszło nie tak! Wiadomość nie została wysłana')
            return render(request, 'stuff/home.html', context)
        else:
            messages.success(request, "Mail został wysłany")
            return render(request, 'stuff/home.html', context)

    context = {
        'form': SetRequestForm(pk, start_date, end_date, request.user)
    }
    return render(request, "stuff/set/request.html", context)


class ReservationFilterByUserListView(ReservationListView):
    template_name = 'users/detail.html'

    def get_queryset(self):
        user_id = get_object_or_404(User, id=self.kwargs.get('pk')).id
        print(ReservationEvent.objects.filter(user_id=user_id))
        return ReservationEvent.objects.filter(user_id=user_id)
