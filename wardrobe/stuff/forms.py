from collections import namedtuple
from django import forms
from datetime import datetime
from .models import ReservationEvent, Item


class ItemReservationForm(forms.ModelForm):
    date_range = forms.CharField()
    taken = forms.BooleanField(required=False)

    def __init__(self, id=None, pk=None, *args, **kwargs):
        super(ItemReservationForm, self).__init__(*args, **kwargs)
        self.item_id = id
        self.pk = pk

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

        reservations = ReservationEvent.objects.filter(item=Item.objects.get(pk=self.item_id)).exclude(pk=self.pk)
        for reservation in reservations:
            r2 = Range(start=reservation.start_date, end=reservation.end_date)
            latest_start = max(r1.start, r2.start)
            earliest_end = min(r1.end, r2.end)
            delta = (earliest_end - latest_start).days + 1
            if delta > 0:
                self.add_error('date_range', f'Nie można dokonać rezerwacji w tym terminie. '
                                             f'Ktoś zarezerwował ten przedmiot w terminie '
                                             f'{reservation.start_date} - {reservation.end_date}')




