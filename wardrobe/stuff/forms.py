from django import forms
from stuff.models import ReservationEvent


class ItemReservationForm(forms.ModelForm):
    date_of_reservation_beginning = forms.DateField()
    date_of_reservation_ending = forms.DateField()

    class Meta:
        model = ReservationEvent
        fields = ['date_of_reservation_beginning', 'date_of_reservation_ending']
