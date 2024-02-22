import json
from datetime import datetime
from typing import Any

from django.contrib import messages
from django.http import JsonResponse, HttpRequest
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView

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
    _record = None
    _customers = None

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        self._customers = CustomerView()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # común para todas las clases list
        # context['url_create'] = reverse_lazy('project_create_root')
        # context['url_delete'] = reverse_lazy('project_delete_root')
        # espesíficos
        context['text_header'] = "Clientes"

        context['customers'] = self._customers.get_all()
        return context


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
            utility = customer.get_utility()
            utility_html = ''
            if utility:
                utility_html += '$ ' + str(utility)
            else:
                utility_html += '$ 0'
            get_debt_count = customer.get_debt_count()
            get_debt_count_html = ''
            if get_debt_count > 0:
                get_debt_count_html += '<span class="badge bg-danger" title="Este cliente posee deudas"> (' + str(
                    customer.get_debt_count()) + ') $' + str(customer.get_debt_amount()) + '</span>'
            count_customer_records = ''
            d = customer.record_set.count()
            if customer.record_set.count() > 0:
                count_customer_records += str(customer.record_set.count())
            else:
                count_customer_records += '0'

            new_customer_html = '<tr><td class="align-items-xxl-center"><span role="button">' \
                                '<img src="' + str(
                customer.get_photo()) + '"class="rounded-circle me-2 thumbnail" width="30" height="30" data-bs-toggle="modal" data-bs-target="#imagenModal" data-bss-tooltip="" ' \
                                        'data-img="' + str(
                customer.get_photo()) + '" alt="customer"> </span>' + customer.name + '</td>' \
                                                                                      '<td>' + str(
                count_customer_records) + '</td><td>' + str(utility_html) + str(get_debt_count_html) + '</td> ' \
                                                                                                       '<td>' + str(
                customer.date_join.strftime("%d de %B de %Y")) + '</td><td>' \
                                                                 '<button class="btn btn-primary btn-sm" data-bs-toggle="tooltip" data-bss-tooltip="" type="button" style="margin-right: 5px;" title="Permite editar los atributos de un cliente"><i class="fas fa-edit"></i></button> ' \
                                                                 '<a data-bs-toggle="tooltip" data-bss-tooltip="" class="btn btn-primary btn-sm" href="/app/customers/' + str(
                customer.pk) + '" style="margin-right: 5px;" title="Permite mostrar la información del cliente"><i class="fas fa-eye"></i></a> ' \
                               '<button class="btn btn-primary btn-sm" data-bs-toggle="tooltip" data-bss-tooltip="" type="button" title="Permite eliminar un cliente" style="margin-right: 5px;"><i class="far fa-trash-alt"></i></button></td></tr>'

            return JsonResponse(
                {'success': True, 'message': 'Cliente guardado correctamente', 'data': serialized_customer,
                 'new_customer_html': new_customer_html},
                safe=False,
                status=201)
        else:
            errors = json.loads(customer_form.errors.as_json())
            return JsonResponse({'success': False, 'errors': errors}, status=400)


class UpdateCustomer(UpdateView):
    template_name = 'customer/create.html'
    form_class = CustomerForm
    model = Customer
    success_url = reverse_lazy('customers')
    _customers = CustomerView()

    def dispatch(self, request, *args, **kwargs):
        self._customers = CustomerView()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        return context

    def form_valid(self, form):
        http = self.request.POST.get('url')
        self.success_url = http
        form = CustomerForm(self.request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Cliente editado correctamente")
            return super().form_valid(form)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f"Error en el campo {field}: {error}")
            return super().form_invalid(form)


class DeleteCustomer(DeleteView):
    model = Customer
    success_url = reverse_lazy("customers")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {
            'message': 'Elemento eliminado exitosamente'
        }
        return JsonResponse(data)
