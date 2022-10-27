from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from account.models import CustomUser, Contact, Customer, Company, Address, Employee


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        owner_user = kwargs.pop('owner_user')
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = Company.objects.filter(owner=owner_user)


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'contact']

    # TODO: change contact queryset for user own only
    # def __init__(self, *args, **kwargs):
    #     owner_user = kwargs.pop('owner_user')
    #     super(CompanyForm, self).__init__(*args, **kwargs)
    #     self.fields['owner'].queryset = Company.objects.filter(owner=owner_user)


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        owner_user = kwargs.pop('owner_user')
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['related_company'].queryset = Company.objects.filter(owner=owner_user)



