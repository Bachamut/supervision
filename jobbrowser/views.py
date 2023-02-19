from django.shortcuts import render
from django.views.generic import ListView
from jobprogress.models import Job
from .filters import JobFilter


class OrdersListView(ListView):

    model = Job
    context_object_name = 'browser'
    template_name = 'jobbrowser/browser.html'

    def get_filter(self, qs):
        orders_filter = JobFilter(self.request.GET, queryset=qs)
        return orders_filter

    def get_queryset(self):
        querryset = self.model.objects.all()
        return querryset

    def get_context_data(self, **kwargs):
        orders = self.get_queryset()
        orders_filter = self.get_filter(orders)
        orders = orders_filter.qs
        context = {'orders': orders,
                   'orders_filter': orders_filter}
        return context

