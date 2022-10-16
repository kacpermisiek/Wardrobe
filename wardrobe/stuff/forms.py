from django import forms
from .models import ReservationEvent
from datetime import date


class ItemReservationForm(forms.ModelForm):
    date_range = forms.CharField()
    # start_date = forms.DateField(widget=forms.SelectDateWidget())
    # end_date = forms.DateField(widget=forms.SelectDateWidget())
    taken = False

    def clean(self):
        cleaned_data = super(ItemReservationForm, self).clean()

        cleaned_data['start_date'], cleaned_data['end_date'] = self._split_dates(cleaned_data['date_range'])
        del cleaned_data['date_range']
        print(cleaned_data)
        return cleaned_data
        # start_date = cleaned_data.get('start_date')
        # end_date = cleaned_data.get('end_date')
        #
        # if start_date > end_date:
        #     self.add_error('end_date', 'Data końcowa musi być większa niż początkowa!')
        #
        # elif start_date < date.today():
        #     self.add_error('start_date', 'Data początkowa nie może być wcześniejsza niż aktualna!')
        #
        # elif end_date < date.today():
        #     self.add_error('start_date', 'Data końcowa nie może być wcześniejsza niż aktualna!')

    # TODO: Need validation for existing reservations

    class Meta:
        model = ReservationEvent
        fields = ['start_date', 'end_date']

    @staticmethod
    def _split_dates(date_range):
        return tuple(date_range.split(' - '))

