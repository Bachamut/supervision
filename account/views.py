from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from account.decorators import unauthenticated_user
from account.forms import LoginForm, UserForm, RegisterForm, ContactForm, CustomerForm, CompanyForm, AddressForm, \
    EmployeeForm
from account.models import CustomUser, Employee, Company, Customer, Address, Contact
from jobprogress.models import Job, Task, JobTemplate
from django.contrib import messages


@method_decorator(login_required)
def dispatch(self, request, *args, **kwargs):
    return super(self.__class__, self).dispatch(request, *args, **kwargs)


@unauthenticated_user
def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            message = f'Account was created for {user}'
            messages.success(request, message)
            return HttpResponseRedirect('/account/login')

    return render(request, 'registration/register1.html', {'form': form})


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/account')
                else:
                    message = f'Account has been blocked'
            else:
                message = f'Username or password is incorrect'
                # return HttpResponse('Konto jest zablokowane.')
        # else:
        #     message = f'Username or password is incorrect'

            # return HttpResponseRedirect('/account/login')
        messages.success(request, message)
    else:
        form = LoginForm()
    return render(request, 'registration/login1.html', {'form': form})


class Dashboard(View):

    @method_decorator(login_required)
    def get(self, request):
        template_name = 'account/dashboard.html'
        return render(request, template_name)

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj

    def get_queryset(self):
        return Job.objects.filter(investor=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of related data to object
        order = kwargs['object']
        tasks = order.task_set.all()
        jobtemplate = JobTemplate.objects.get(pk=order.job_type_id)
        statuses = jobtemplate.status_set.all()
        context = {'order': order,
                   'tasks': tasks,
                   'job_type': jobtemplate,
                   'statuses': statuses
                   }
        return context


class Profile(View):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        template_name = 'account/profile.html'
        context = {'user': user}
        return render(request, template_name, context)


def edit_profile(request):

    user = CustomUser.objects.get(id=request.user.id)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect('/account/profile')

    return render(request, 'account/edit_profile.html', {'form': form})


def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return HttpResponseRedirect('/account/orders')
    else:
        form = ContactForm()
    return render(request, 'account/add_contact.html', {'contact_form': form})


def edit_contact(request, pk):

    contact = Contact.objects.get(id=pk)
    form = ContactForm(instance=contact)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return HttpResponseRedirect('/account/companies')

    return render(request, 'account/edit_contact.html', {'form': form})


class CustomersList(ListView):

    model = Customer
    context_object_name = 'customers'
    template_name = 'account/customers.html'

    def get_queryset(self):
        result=list()
        companies = Company.objects.filter(owner=self.request.user)
        for c in companies:
            querryset = Customer.objects.filter(owner=c)
            result += querryset
        return result

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the customers related to owner
        customers = self.get_queryset()
        context['customers'] = customers
        return context


def add_customer(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST, owner_user=request.user)
        # check whether it's valid:
        if form.is_valid():

            customer = form.save(commit=False)
            customer.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/account/customers')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm(owner_user=request.user)

    return render(request, 'account/add_customer.html', {'form': form})


def edit_customer(request, pk):

    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer, owner_user=request.user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer, owner_user=request.user)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return HttpResponseRedirect('/account/customers')

    return render(request, 'account/edit_customer.html', {'form': form})


def add_address(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddressForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            address = form.save(commit=False)
            address.owner = request.user
            address.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/account/companies')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddressForm()

    return render(request, 'account/add_company.html', {'form': form})


def edit_address(request, pk):

    address = Address.objects.get(id=pk)
    form = AddressForm(instance=address)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.save()
            return HttpResponseRedirect('/account/companies')

    return render(request, 'account/edit_address.html', {'form': form})


class EmployeesList(ListView):

    model = Employee
    context_object_name = 'employees'
    template_name = 'account/employees.html'

    def get_queryset(self):
        result=list()
        companies = Company.objects.filter(owner=self.request.user)
        for c in companies:
            querryset = Employee.objects.filter(related_company=c)
            result += querryset
        return result

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the orders related to owner
        employees = self.get_queryset()
        context['employees'] = employees
        return context


def add_employee(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmployeeForm(request.POST, owner_user=request.user)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            employee = form.save(commit=False)
            # employee.owner = request.user
            employee.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/account/orders')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmployeeForm(owner_user=request.user)

    return render(request, 'account/add_company.html', {'form': form})


def edit_employee(request, pk):

    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(instance=employee, owner_user=request.user)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee, owner_user=request.user)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return HttpResponseRedirect('/account/orders')

    return render(request, 'account/edit_employee.html', {'form': form})


class CompaniesList(ListView):

    model = Company
    context_object_name = 'companies'
    template_name = 'account/companies.html'

    def get_queryset(self):
        result = Company.objects.filter(owner=self.request.user)
        return result

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the orders related to owner
        companies = self.get_queryset()
        context['companies'] = companies
        return context


def add_company(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CompanyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/account/orders')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CompanyForm()

    return render(request, 'account/add_company.html', {'form': form})


def edit_company(request, pk):

    company = Company.objects.get(id=pk)
    form = CompanyForm(instance=company)

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            return HttpResponseRedirect('/account/companies')

    return render(request, 'account/edit_company.html', {'form': form})
