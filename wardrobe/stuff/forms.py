from django import forms
from .models import ReservationEvent
from datetime import datetime


class ItemReservationForm(forms.ModelForm):
    date_range = forms.CharField()
    # start_date = forms.DateField(widget=forms.SelectDateWidget())
    # end_date = forms.DateField(widget=forms.SelectDateWidget())
    taken = False

    def clean(self):
        cleaned_data = super(ItemReservationForm, self).clean()

        cleaned_data['start_date'], cleaned_data['end_date'] = self._convert_date_range_into_dates(
            cleaned_data['date_range'])
        del cleaned_data['date_range']
        return cleaned_data

    # TODO: Need validation for existing reservations

    class Meta:
        model = ReservationEvent
        fields = ['start_date', 'end_date']

    def _convert_date_range_into_dates(self, date_range):
        result = []
        for date_string in date_range.split(' - '):
            result.append(self._string_to_date(date_string))

        return tuple(result)

    @staticmethod
    def _string_to_date(date_string):
        return datetime.strptime(date_string, '%d-%m-%Y').date()


