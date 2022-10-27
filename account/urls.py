from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_page, name='register_page'),
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/edit_profile', views.edit_profile, name='edit_profile'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_company/', views.add_company, name='add_company'),
    path('add_address/', views.add_address, name='add_address'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('employees/', views.EmployeesList.as_view(), name='employees'),
    re_path(r'^employees/(?P<pk>\d+)', views.edit_employee, name='edit_employee'),
    path('companies/', views.CompaniesList.as_view(), name='companies'),
    re_path(r'^companies/(?P<pk>\d+)', views.edit_company, name='edit_company'),
    path('customers/', views.CustomersList.as_view(), name='customers'),
    re_path(r'^customers/(?P<pk>\d+)', views.edit_customer, name='edit_customer'),
]
