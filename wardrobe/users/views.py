from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


def register(request):
    def _request_method_is_post(method):
        return method == 'POST'

    def _proceed_redirection(form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f'Konto stworzone dla {username}. Możesz się teraz zalogować :)')
        return redirect('login')

    if _request_method_is_post(request.method):
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            return _proceed_redirection(register_form)

    else:
        register_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': register_form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')