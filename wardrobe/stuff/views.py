from django.shortcuts import render


stuff_items = [
    {
        'name': 'Kabel',
        'description': 'czerwony',
        'badge_status': 'success',
        'status': 'Dostępny',
        'category': 'Części elektroniczne'
    },

    {
        'name': 'Elvis',
        'description': 'komputer',
        'badge_status': 'danger',
        'status': 'Uszkodzony',
        'category': 'lorem ipsum'
    },
    {
        'name': 'Jakaś nazwa',
        'description': 'fajna',
        'badge_status': 'info',
        'status': 'Zarezerwowany',
        'category': 'Części elektroniczne'
    },
    {
        'name': 'Niedostepny przedmiot',
        'description': 'nie ma go jeszcze na stanie',
        'badge_status': 'dark',
        'status': 'Niedostępny',
        'category': 'Części elektroniczne'
    },

    {
        'name': 'Niedostepny przedmiot',
        'description': 'nie ma go jeszcze na stanie',
        'badge_status': 'dark',
        'status': 'Niedostępny',
        'category': 'Części elektroniczne'
    },

]


def home(request):
    context = {
        'stuff': stuff_items,
        'title': 'Home page'
    }
    return render(request, 'stuff/home.html', context)


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'stuff/about.html', context)
