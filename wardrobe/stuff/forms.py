from django import forms
from stuff.models import ReservationEvent
from datetime import date


class ItemReservationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())
    taken = True

    def clean(self):
        cleaned_data = super(ItemReservationForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date > end_date:
            self.add_error('end_date', 'Data końcowa musi być większa niż początkowa!')

        elif start_date < date.today():
            self.add_error('start_date', 'Data początkowa nie może być wcześniejsza niż aktualna!')

        elif end_date < date.today():
            self.add_error('start_date', 'Data końcowa nie może być wcześniejsza niż aktualna!')

        return cleaned_data

    class Meta:
        model = ReservationEvent
        fields = ['start_date', 'end_date', 'taken']

