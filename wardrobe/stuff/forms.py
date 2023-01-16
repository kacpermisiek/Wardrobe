from collections import namedtuple
from itertools import chain
from django import forms
from datetime import datetime
from .models import ReservationEvent, Item, SetTemplate, Set


class ReservationConfirmForm(forms.ModelForm):
    set = forms.CharField(required=False)

    def __init__(self, set, start_date, end_date, *args, **kwargs):
        super(ReservationConfirmForm, self).__init__(*args, **kwargs)
        self.set = set
        self.start_date = self._string_to_date(start_date)
        self.end_date = self._string_to_date(end_date)

    class Meta:
        model = ReservationEvent
        fields = ['set', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super(ReservationConfirmForm, self).clean()

        if self._is_reserved_in_this_date_range():
            pass
        cleaned_data['set'] = self.set
        cleaned_data['start_date'] = self.start_date
        cleaned_data['end_date'] = self.end_date
        return cleaned_data

    def _is_reserved_in_this_date_range(self):
        Range = namedtuple('Range', ['start', 'end'])
        r1 = Range(self.start_date, self.end_date)
        set_reservations = ReservationEvent.objects.filter(set=self.set).all()
        for reservation in set_reservations:
            r2 = Range(reservation.start_date, reservation.end_date)
            if self._dates_overlap(r1, r2):
                return True
        return False

    @staticmethod
    def _string_to_date(str_date):
        return datetime.strptime(str_date, '%d-%m-%Y').date()

    @staticmethod
    def _get_timestamp(r1, r2):
        return min(r1.end, r2.end), max(r1.start, r2.start)

    def _dates_overlap(self, r1, r2):
        earliest_end, latest_start = self._get_timestamp(r1, r2)
        delta = (earliest_end - latest_start).days + 1
        return delta > 0


class ReservationUpdateForm(forms.ModelForm):
    date_range = forms.CharField()
    taken = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.reservation = ReservationEvent.objects.get(id=kwargs.get('pk', None))
        kwargs.pop('pk', None)
        self.set = self.reservation.set
        super(ReservationUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ReservationEvent
        fields = ['start_date', 'end_date', 'taken']

    def clean(self):
        cleaned_data = super(ReservationUpdateForm, self).clean()
        if not cleaned_data.get('taken'):
            cleaned_data['taken'] = False

        cleaned_data['start_date'], cleaned_data['end_date'] = self._convert_date_range_into_dates(
            cleaned_data['date_range'])
        del cleaned_data['date_range']
        self._validate_dates_overlap(cleaned_data)
        return cleaned_data

    def _convert_date_range_into_dates(self, date_range):
        result = []
        for date_string in date_range.split(' - '):
            result.append(self._string_to_date(date_string))

        return tuple(result)

    @staticmethod
    def _string_to_date(date_string):
        return datetime.strptime(date_string, '%d-%m-%Y').date()

    def _validate_dates_overlap(self, cleaned_data):
        Range = namedtuple('Range', ['start', 'end'])
        r1 = Range(start=cleaned_data['start_date'], end=cleaned_data['end_date'])

        reservations = self._get_reservations()
        for reservation in reservations:
            r2 = Range(start=reservation.start_date, end=reservation.end_date)
            earliest_end, latest_start = self._get_timestamp(r1, r2)
            delta = (earliest_end - latest_start).days + 1
            if delta > 0:
                print('elo')
                self.add_error('date_range', f'Nie można dokonać rezerwacji w tym terminie. '
                                             f'Ktoś zarezerwował ten przedmiot w terminie '
                                             f'{reservation.start_date} - {reservation.end_date}')

    def _get_reservations(self):
        result = ReservationEvent.objects.filter(set=Set.objects.get(id=self.set.id))
        return result.exclude(pk=self.reservation.id) if self.reservation.id else result

    @staticmethod
    def _get_timestamp(r1, r2):
        return min(r1.end, r2.end), max(r1.start, r2.start)


class SetTemplateForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = SetTemplate
        fields = ['name']


class SetForm(forms.ModelForm):

    items = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, set_template_id=None, set_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_mode = set_id is None

        if self.create_mode:
            self.set_template_id = set_template_id
            self.current_items = []
        else:
            self.set = Set.objects.get(id=set_id)
            self.set_template_id = self.set.set_template.id
            print(f"\nDEBUG\nCurrent items: {self.set.items}")
            self.current_items = self.set.items

        items_required = [val for val in SetTemplate.objects.get(id=self.set_template_id).items_required.all()]
        for item_required in items_required:
            field_name = item_required.item_type.name
            self.fields[field_name] = forms.MultipleChoiceField(
                required=True,
                widget=forms.CheckboxSelectMultiple,
                choices=self._create_choices(item_required.item_type.name),
                label=f"Wybierz {item_required.quantity_required} przedmioty typu {item_required.item_type.name}",
                initial=self._get_initial_checks(item_required.item_type.name)
            )

    def clean(self):
        cleaned_data = super(SetForm, self).clean()
        cleaned_data['items'] = []
        to_delete = []
        for arg in cleaned_data.items():
            if self._is_item_field(arg[0]):
                cleaned_data['items'].extend(arg[1])
                to_delete.append(arg[0])

        for arg in to_delete:
            del cleaned_data[arg]

        cleaned_data['set_template'] = SetTemplate.objects.get(id=self.set_template_id)
        return cleaned_data

    class Meta:
        model = Set
        exclude = ['set_template', 'set_status']

    def _create_choices(self, item_name):
        available_items = Item.objects.filter(type__name=item_name, item_set__isnull=True).all()
        if not self.create_mode:
            available_items = list(chain(available_items, self.current_items.filter(type__name=item_name)))

        return tuple([(item.id, item) for item in available_items])

    def _get_initial_checks(self, item_name):
        return [] if self.create_mode else [item.id for item in self.current_items.filter(type__name=item_name).all()]

    def get_items_fields(self):
        for field_name in self.fields:
            if self._is_item_field(field_name):
                yield field_name

    @staticmethod
    def _is_item_field(field_name):
        return field_name not in ['items']

    def save(self, **kwargs):
        items_for_set = [Item.objects.get(id=item_id) for item_id in self.cleaned_data['items']]

        output = super(SetForm, self).save(**kwargs)
        self._remove_sets_from_previous_items(self.current_items)
        self._add_sets_for_new_items(items_for_set, self.instance.id)
        return output

    @staticmethod
    def _remove_sets_from_previous_items(current_items):
        for item in current_items:
            item.item_set = None
            item.save()

    @staticmethod
    def _add_sets_for_new_items(items_for_set, id_of_set):
        set_to_set = Set.objects.get(id=id_of_set)
        print(set_to_set.id)
        print(items_for_set)
        for item in items_for_set:
            item.item_set = set_to_set
            item.save()


class SetRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

    def __init__(self, pk, start_date, end_date, user):
        self.set_template = SetTemplate.objects.get(id=pk)
        self.start_date = start_date
        self.end_date = end_date
        self.user = user
        super(SetRequestForm, self).__init__()
        self.initial['message'] = self.get_msg_template()

    def generate_message(self):
        return f'xd {self.start_date}'

    def get_msg_template(self):
        return f"""
Szanowny Panie,
    zwracam się do Pana z prośbą o możliwość udostępnienia zestawu {self.set_template.name} 
    w terminie {self.start_date} - {self.end_date}.

Pozdrawiam serdecznie,
{self.user.first_name} {self.user.last_name}
{self.user.email}
        """

    class Meta:
        fields = ['message']
