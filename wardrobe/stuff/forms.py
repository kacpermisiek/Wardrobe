from collections import namedtuple
from django import forms
from datetime import datetime
from .models import ReservationEvent, Item, SetTemplate, ItemRequired


class ItemReservationForm(forms.ModelForm):
    date_range = forms.CharField()
    taken = forms.BooleanField(required=False)

    def __init__(self, pk, id=None, *args, **kwargs):
        super(ItemReservationForm, self).__init__(*args, **kwargs)
        self.item_id = pk
        self.reservation_id = id

    class Meta:
        model = ReservationEvent
        fields = ['start_date', 'end_date', 'taken']

    def clean(self):
        cleaned_data = super(ItemReservationForm, self).clean()
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
                self.add_error('date_range', f'Nie można dokonać rezerwacji w tym terminie. '
                                             f'Ktoś zarezerwował ten przedmiot w terminie '
                                             f'{reservation.start_date} - {reservation.end_date}')

    def _get_reservations(self):
        result = ReservationEvent.objects.filter(item=Item.objects.get(id=self.item_id))
        return result.exclude(pk=self.reservation_id) if self.reservation_id else result

    @staticmethod
    def _get_timestamp(r1, r2):
        return min(r1.end, r2.end), max(r1.start, r2.start)


class SetTemplateForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = SetTemplate
        fields = ['name']
