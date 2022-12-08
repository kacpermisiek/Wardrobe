from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import PasswordResetView
from utils.forms_functions import proceed_redirection, request_method_is_post, all_forms_are_valid


def _get_user_and_profile_update_forms(request):
    return (UserUpdateForm(request.POST, instance=request.user),
            ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile))


def register(request):
    if request_method_is_post(request.method):
        register_form = UserRegistrationForm(request.POST)
        # username = register_form.cleaned_data.get('username')
        if all_forms_are_valid(register_form):
            return proceed_redirection(
                request=request,
                redirect_page='login',
                message=f'Konto stworzone. Możesz się teraz zalogować :)',
                forms=[register_form],
            )

    else:
        register_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': register_form})


@login_required
def profile(request):
    if request_method_is_post(request.method):
        user_update_form, profile_update_form = _get_user_and_profile_update_forms(request)

        if all_forms_are_valid(user_update_form, profile_update_form):
            proceed_redirection(
                request=request,
                redirect_page='profile',
                message='Twoje konto zostało zaktualizowane!',
                forms=[user_update_form, profile_update_form]
            )
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }
    return render(request, 'users/profile.html', context)
