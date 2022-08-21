from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


BADGE_STATUSES = {'Dostępny': 'success',
                  'Uszkodzony': 'danger',
                  'Zarezerwowany': 'info',
                  'Niedostępny': 'dark'}


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def _get_badge_status(status):
    return BADGE_STATUSES[status]


def _get_statuses():
    return tuple([(key, key) for key in BADGE_STATUSES.keys()])


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=_get_statuses(), default='Dostępny')
    badge_status = 'success'

    borrower = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    date_added = models.DateField(default=now)
    date_reserved = models.DateField(null=True, blank=True)
    date_borrowed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} item from {self.category} category'
