from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from account.forms import RegisterForm, UserForm
from account.models import Company, Address, Contact, Employee, CustomUser, Customer


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = ['name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = ['country', 'province', 'county', 'commune', 'city', 'street_name', 'street_number', 'room_number']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ['nip', 'address', 'phone_number', 'email']


@admin.register(Employee)
class Employee(admin.ModelAdmin):

    list_display = ['related_company', 'first_name', 'last_name', 'position', 'phone_number', 'email']


@admin.register(Customer)
class Customer(admin.ModelAdmin):

    list_display = ['owner', 'type', 'related_user', 'related_company']


class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = UserForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)