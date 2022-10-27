from django.contrib.auth.models import AbstractUser, User
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Address(models.Model):

    province_choices = [
        ('1', 'dolnośląskie'),
        ('2', 'kujawsko-pomorskie'),
        ('3', 'łódzkie'),
        ('4', 'lubelskie'),
        ('5', 'lubuskie'),
        ('6', 'małopolskie'),
        ('7', 'mazowieckie'),
        ('8', 'opolskie'),
        ('9', 'podkarpackie'),
        ('10', 'podlaskie'),
        ('11', 'pomorskie'),
        ('12', 'śląskie'),
        ('13', 'świętokrzyskie'),
        ('14', 'warmińsko-mazurskie'),
        ('15', 'wielkopolskie'),
        ('16', 'zachodniopomorskie'),
    ]

    country = models.CharField(verbose_name='kraj', max_length=30)
    province = models.CharField(verbose_name='województwo', max_length=30, choices=province_choices)
    county = models.CharField(verbose_name='powiat', max_length=30)
    commune = models.CharField(verbose_name='gmina', max_length=30)
    city = models.CharField(verbose_name='miasto', max_length=30)
    street_name = models.CharField(verbose_name='ulica', max_length=30)
    street_number = models.CharField(verbose_name='numer budynku', max_length=4)
    room_number = models.CharField(verbose_name='numer lokalu', max_length=4)

    def __str__(self):
        return f'{self.city}, {self.get_province_display()}'


class Contact(models.Model):

    nip = models.CharField(verbose_name='NIP', max_length=12)
    address = models.ForeignKey(Address, verbose_name='adres', on_delete=models.CASCADE)
    phone_number = PhoneNumberField(verbose_name='telefon kontaktowy')
    email = models.EmailField(verbose_name='email')

    def __str__(self):
        return self.nip


class Company(models.Model):

    owner = models.ForeignKey(CustomUser, verbose_name='właściciel', on_delete=models.PROTECT, null=True)
    name = models.CharField('company name', max_length=90)
    contact = models.ForeignKey(Contact, verbose_name='dane kontaktowe', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):

    related_user = models.ForeignKey(CustomUser, verbose_name='użytkownik', on_delete=models.PROTECT, null=True, blank=True)
    related_company = models.ForeignKey(Company, verbose_name='pracownik firmy', on_delete=models.CASCADE, null=True)
    first_name = models.CharField(verbose_name='imię', max_length=20)
    last_name = models.CharField(verbose_name='nazwisko', max_length=30)
    position = models.CharField(verbose_name='stanowisko', max_length=120)
    phone_number = PhoneNumberField(verbose_name='telefon służbowy')
    email = models.EmailField(verbose_name='business email', unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Customer(models.Model):

    customer_type = [
        ('retail', 'retail'),
        ('company', 'company')
    ]

    owner = models.ForeignKey(Company, related_name='customer', verbose_name='klient firmy', on_delete=models.CASCADE, null=True)
    type = models.CharField('rodzaj', max_length=10, choices=customer_type)
    related_user = models.ForeignKey(CustomUser, related_name='user', verbose_name='użytkownik', on_delete=models.PROTECT, null=True, blank=True)
    related_company = models.ForeignKey(Company, related_name='company', verbose_name='firma', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.related_user:
            name = self.related_user.email
        elif self.related_company:
            name = self.related_company.name
        else:
            name = 'customer'
        return name


