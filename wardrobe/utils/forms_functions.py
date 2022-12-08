from django.shortcuts import redirect
from django.contrib import messages


def _save_forms(forms):
    for form in forms:
        form.save()


def all_forms_are_valid(*forms):
    return all([form.is_valid() for form in forms])


def request_method_is_post(method):
    return method == 'POST'


def proceed_redirection(request, redirect_page, message, forms):
    _save_forms(forms)
    messages.success(request, message)
    return redirect(redirect_page)
