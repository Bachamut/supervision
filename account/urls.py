from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from account import views

urlpatterns = [
    # path('login/', views.user_login, name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    # path('<int:order_id>/', views.order, name='order'),
    re_path(r'^orders/(?P<order_id>\d+)/$', views.order, name='order')
]