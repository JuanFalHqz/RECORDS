import json
from datetime import datetime
from typing import Any

from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView, View, DetailView, CreateView

from apps.core.forms.customer import CustomerForm
from apps.core.models import Customer, Record


class CustomerView(View):
    _all = None
    _customer_by_current_day = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._all = Customer.objects.all()
        self._customer_by_current_day = Customer.objects.filter(
            record__date_record__day=timezone.now().date().day,
            record__date_record__month=timezone.now().date().month,
            record__date_record__year=timezone.now().year).distinct('name', 'mobile')

    def get_all(self):
        return self._all

    def get_count(self):
        return self._all.count()

    def get_customer_by_current_day(self):
        return self._customer_by_current_day

    def get_customer_by_date_range(self, start_date, end_date):
        if start_date and end_date:
            self._all = self._all = Customer.objects.filter(
                record__date_record__range=(start_date, end_date)).distinct('name', 'mobile')
        if start_date and not end_date:
            self._all = self._all = Customer.objects.filter(
                record__date_record__range=(start_date, datetime.now())).distinct('name', 'mobile')
        if not start_date and end_date:
            self._all = self._all = Customer.objects.filter(
                record__date_record__range=(Record.objects.order_by('date_record').first().date_record, end_date)). \
                distinct('name', 'mobile')
        return self._all

    def get_customer_count_by_date_range(self, start_date, end_date):
        return self.get_customer_by_date_range(start_date, end_date).count()


class ListCustomers(ListView):
    template_name = 'customers_list.html'
    queryset = Customer.objects.all()


class DetailCustomer(DetailView):
    template_name = 'customer_detail.html'
    model = Customer


class CreateCustomer(CreateView):
    template_name = ''
    model = Customer
    form_class = CustomerForm

    def post(self, request, *args, **kwargs):
        customer_form = CustomerForm(request.POST, request.FILES)
        if customer_form.is_valid():
            customer = customer_form.save()  # Crear una instancia de Customer pero no guardarla todavía
            serialized_customer = {
                'pk': customer.id,
                'name': customer.name,
                'mobile': customer.mobile,
                'photo': customer.get_photo(),
            }
            # customer.save()
            return JsonResponse(
                {'success': True, 'message': 'Cliente guardado correctamente', 'data': serialized_customer},
                safe=False,
                status=201)
        else:
            errors = json.loads(customer_form.errors.as_json())
            return JsonResponse({'success': False, 'errors': errors}, status=400)
