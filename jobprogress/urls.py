from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from jobprogress import views

urlpatterns = [

    path('add_order/', views.add_order, name='add_order'),
    path('add_template/', views.add_job_template, name='add_template'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    path('orders/', views.InvestorOrdersList.as_view(), name='orders'),
    path('orders/email_notification/<str:pk>/', views.EmailNotification.as_view(), name='email_notification'),
    path('orders/email_notification/success', views.ContactSuccessView.as_view(), name='success'),
    re_path(r'^orders/(?P<pk>\d+)', views.OrderDetail.as_view(), name='order'),
]
