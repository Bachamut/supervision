from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def user_group_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        allowed_user_group = []