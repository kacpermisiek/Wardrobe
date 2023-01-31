from PIL import Image
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from django.core.validators import MinValueValidator


BADGE_STATUSES = {'Dostępny': 'success',
                  'Uszkodzony': 'danger',
                  'Zarezerwowany': 'info'}


def _get_statuses():
    return tuple([(key, key) for key in BADGE_STATUSES.keys() if key != 'Zarezerwowany'])


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def num_of_objects(self):
        return len(Item.objects.filter(type__category=self))


class ItemTemplate(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='qwe')
    image = models.ImageField(default='default_item.png', upload_to='item_pics', blank=True, null=True)

    @property
    def quantity(self):
        return len(Item.objects.filter(type=self))

    @property
    def item_instances(self):
        return Item.objects.filter(type=self)


class ItemRequired(models.Model):
    quantity_required = models.IntegerField(validators=[MinValueValidator(1)])
    item_type = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return f'item type: {self.item_type.name}'


class SetTemplate(models.Model):
    name = models.CharField(max_length=50)
    items_required = models.ManyToManyField(ItemRequired)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ready = models.BooleanField(default=False)

    def items_list(self):
        return self.items_required.all().order_by('item_type__name')

    def __str__(self):
        return f"SetTemplate object name: {self.name}"


class Set(models.Model):
    set_template = models.ForeignKey(SetTemplate, on_delete=models.CASCADE)
    set_status = models.CharField(max_length=20, default='Dostępny')
    description = models.TextField(blank=True, null=True)

    @property
    def reservations(self):
        return ReservationEvent.objects.filter(set_id=self.id).all

    @property
    def items(self):
        return Item.objects.filter(item_set=self)

    class Meta:
        ordering = ['set_status']

    def __str__(self):
        return f'Set object'


class Item(models.Model):
    type = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=_get_statuses(), default='Dostępny')
    date_added = models.DateField(default=now)
    item_set = models.ForeignKey(Set,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)

    @property
    def badge_status(self):
        return {'Dostępny': 'success',
                'Uszkodzony': 'danger',
                'Zarezerwowany': 'info',
                'W zestawie': 'dark'}[self.final_status]

    @property
    def final_status(self):
        return 'Zarezerwowany' if self._is_reserved() else "W zestawie" if self.item_set else self.status

    def _is_reserved(self):
        if not self.item_set:
            return False
        for reservation in self.item_set.reservations():
            if reservation.is_current:
                return True
        return False

    def __str__(self):
        return f'({self.id}) {self.type.name}'


class ReservationEvent(models.Model):
    start_date = models.DateField(null=True, blank=True, default=now)
    end_date = models.DateField(null=True, blank=True, default=now)
    taken = models.BooleanField(default=False)

    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def is_current(self):
        return self.start_date <= date.today() <= self.end_date

    def __str__(self):
        return f'Rent event\t item:{self.set}\tuser: {self.user}\n' \
               f'from {self.start_date} to {self.end_date}'
