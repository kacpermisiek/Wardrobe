from django.contrib import admin
from .models import (
    Category,
    ItemTemplate,
    ItemRequired,
    Item,
    SetTemplate,
    Set,
    ReservationEvent
)

admin.site.register(Category)
admin.site.register(ItemTemplate)
admin.site.register(ItemRequired)
admin.site.register(Item)
admin.site.register(SetTemplate)
admin.site.register(Set)
admin.site.register(ReservationEvent)
