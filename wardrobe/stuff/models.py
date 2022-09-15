from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse


BADGE_STATUSES = {'Dostępny': 'success',
                  'Uszkodzony': 'danger',
                  'Zarezerwowany': 'info',
                  'Niedostępny': 'dark'}


def _get_statuses():
    return tuple([(key, key) for key in BADGE_STATUSES.keys()])


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=_get_statuses(), default='Dostępny')

    date_added = models.DateField(default=now)

    def __str__(self):
        return f'{self.name} item from {self.category} category'

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})


class ReservationEvent(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    taken = models.BooleanField(default=False)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rent event\t item:{self.item}\tuser: {self.user}\n' \
               f'from {self.start_date} to {self.end_date}'
