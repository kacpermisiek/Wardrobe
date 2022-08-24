from django.shortcuts import render
from stuff.models import Item, BADGE_STATUSES


def home(request):

    def _get_badge_status(status):
        return BADGE_STATUSES[status]

    def _set_badge_statuses(items):
        for item in items:
            try:
                item.badge_status = _get_badge_status(item.status)
            except KeyError:
                item.badge_status = 'dark'

        return items

    def _get_items():
        items = Item.objects.all()

        return _set_badge_statuses(items)

    context = {
        'stuff': _get_items(),
        'title': 'strona główna'
    }
    return render(request, 'stuff/home.html', context)


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'stuff/about.html', context)
