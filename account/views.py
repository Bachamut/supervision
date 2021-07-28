from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from account.forms import LoginForm
from jobprogress.models import Job, Task, JobTemplate


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
            else:
                return HttpResponse('Konto jest zablokowane.')
        else:
            return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'selection': 'dashboard'})

@login_required
def orders(request):
    orders = Job.objects.filter(investor=request.user)
    # for order in orders:
    #     tasks = order.objects.task_set.all()
    tasks = Task.objects.filter()
    context = {'orders': orders, 'tasks': tasks}
    return render(request, 'account/orders.html', context)

@login_required
def order(request, order_id):
    order = Job.objects.get(id=order_id)
    tasks = order.task_set.all()
    jobtemplate = JobTemplate.objects.get(pk=order.job_type_id)
    statuses = jobtemplate.status_set.all()
    context = {'order': order,
               'tasks': tasks,
               'job_type': jobtemplate,
               'statuses': statuses
               }
    return render(request, 'account/order.html', context)



