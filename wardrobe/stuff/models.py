from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from datetime import date
from PIL import Image


BADGE_STATUSES = {'Dostępny': 'success',
                  'Uszkodzony': 'danger',
                  'Zarezerwowany': 'info',
                  'Niedostępny': 'dark'}


def _get_statuses():
    return tuple([(key, key) for key in BADGE_STATUSES.keys() if key != 'Zarezerwowany'])


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def num_of_objects(self):
        return len(Item.objects.filter(category=self))


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(default='default_item.png', upload_to='item_pics')

    status = models.CharField(max_length=20, choices=_get_statuses(), default='Dostępny')
    date_added = models.DateField(default=now)

    @property
    def badge_status(self):
        return {'Dostępny': 'success',
                'Uszkodzony': 'danger',
                'Zarezerwowany': 'info',
                'Zabrany': 'dark',
                'Niedostępny': 'dark'}[self.final_status]

    @property  # TODO: bad variable name, should be better
    def final_status(self):
        return 'Zabrany' if self._is_taken() else 'Zarezerwowany' if self._is_between_dates() else self.status

    @property
    def reservations(self):
        return ReservationEvent.objects.filter(item=self)

    def save(self, *args, **kwargs):
        super(Item, self).save()
        image = Image.open(self.image).convert('RGB')

        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.convert('RGB')

        image.save(self.image.path)
        image.close()

    def __str__(self):
        return f'{self.name} item from {self.category} category'

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})

    def _is_between_dates(self):
        for reservation in self.reservations:
            if reservation.is_current:
                return True
        return False

    def _is_taken(self):
        for reservation in self.reservations:
            if reservation.taken:
                return True
        return False


class ReservationEvent(models.Model):
    start_date = models.DateField(null=True, blank=True, default=now)
    end_date = models.DateField(null=True, blank=True, default=now)
    taken = models.BooleanField(default=False)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def is_current(self):
        return self.start_date <= date.today() <= self.end_date

    def __str__(self):
        return f'Rent event\t item:{self.item}\tuser: {self.user}\n' \
               f'from {self.start_date} to {self.end_date}'
