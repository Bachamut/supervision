from django.urls import path

from jobbrowser import views

appname = 'jobbrowser'
urlpatterns = [
    path('browser/', views.OrdersListView.as_view(), name='browser'),
]
