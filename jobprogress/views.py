from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, TemplateView

from account.models import Company
from jobprogress.forms import AddJobTemplate, AddOrder, EmailNotificationForm
from jobprogress.models import Job, Task


def add_job_template(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddJobTemplate(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.instance.creator = request.user
            # process the data in form.cleaned_data as required
            job_template = form.save(commit=False)
            job_template.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/account/orders')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddJobTemplate()

    return render(request, 'jobprogress/add_job_template.html', {'form': form})


def add_order(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddOrder(request.POST, owner_user=request.user)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            job = form.save(commit=False)
            job.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/account/orders')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddOrder(owner_user=request.user)

    return render(request, 'jobprogress/add_order.html', {'form': form})


def update_order(request, pk):

    order = Job.objects.get(id=pk)
    form = AddOrder(instance=order, owner_user=request.user)
    if request.method == 'POST':
        form = AddOrder(request.POST, instance=order, owner_user=request.user)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            return HttpResponseRedirect('/account/orders')

    return render(request, 'jobprogress/update_order.html', {'form': form})


def delete_order(request, pk):

    order = Job.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return HttpResponseRedirect('/account/orders')
    return render(request, 'jobprogress/delete_order.html', {'order': order})


class InvestorOrdersList(ListView):

    model = Job
    context_object_name = 'orders'
    template_name = 'jobprogress/orders.html'

    def get_queryset(self):
        result = list()
        contractors = Company.objects.filter(owner=self.request.user)
        for c in contractors:
            querryset = Job.objects.filter(contractor=c)
            result += querryset
        return result

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the orders related to owner
        orders = self.get_queryset()
        context['orders'] = orders
        return context


class OrderDetail(DetailView):

    model = Job
    context_object_name = 'order'
    template_name = 'jobprogress/order_detail.html'


class EmailNotification(FormView):

    form_class = EmailNotificationForm
    template_name = 'jobprogress/email_notification.html'
    success_url = reverse_lazy('jobprogress:success')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if kwargs:
    #         pk = kwargs['pk']

    def get_initial(self):
        initial = super(EmailNotification, self).get_initial()
        if self.request.user.is_authenticated:
            initial.update({'user': self.request.user,
                            'email_from': self.request.user.email})
            return initial

    def form_valid(self, form):

        form.cleaned_data['user'] = self.request.user
        form.cleaned_data['email_from'] = self.request.user.email
        form.send()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'jobprogress/success.html'
