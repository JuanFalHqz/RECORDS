import json
from datetime import datetime
from typing import Any

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView

from apps.core.forms.records import RecordForm
from apps.core.models import Record
from apps.core.views.customer import CustomerView


class RecordView(View):
    _all = None
    _records_by_current_day = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._all = Record.objects.all()
        self._records_by_current_day = Record.objects.filter(date_record__day=timezone.now().date().day,
                                                             date_record__month=timezone.now().date().month,
                                                             date_record__year=timezone.now().year)

    def get_all(self):
        return self._all

    def get_count(self):
        return self._all.count()

    def get_all_utility(self):
        utility = 0
        for record in self._all:
            utility += record.price
        return utility

    def get_debt_count(self):
        count = 0
        for record in self._all:
            if record.is_debtor:
                count += 1
        return count

    def get_debt_amount(self):
        amount = 0
        for record in self._all:
            if record.is_debtor:
                amount += record.price
        return amount

    def get_records_by_current_day(self):
        return self._records_by_current_day

    def get_all_utility_by_current_day(self):
        return self.get_records_by_current_day().aggregate(a=Sum('price'))['a']

    def get_debt_count_by_current_day(self):
        return self._records_by_current_day.filter(is_debtor=True).count()

    def get_debt_amount_by_current_day(self):
        return self._records_by_current_day.filter(is_debtor=True).aggregate(b=Sum('price'))['b']

    def get_records_by_date_range(self, start_date, end_date):
        if start_date and end_date:
            self._all = self._all.filter(date_record__range=(start_date, end_date))
        if start_date and not end_date:
            self._all = self._all.filter(date_record__range=(start_date, datetime.now()))
        if not start_date and end_date:
            start_date = self._all.order_by('date_record').first().date_record.date()
            self._all = self._all.filter(
                date_record__range=(start_date, end_date))
        if not start_date and not end_date:
            self._all = Record.objects.all()
        return self._all


class ListRecords(ListView):
    template_name = 'records_list.html'
    _record = RecordView()
    _customers = CustomerView()
    queryset = Record.objects.all()

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        self._record = RecordView()
        self._customers = CustomerView()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # común para todas las clases list
        # context['url_create'] = reverse_lazy('project_create_root')
        # context['url_delete'] = reverse_lazy('project_delete_root')
        # espesíficos
        context['text_header'] = "Grabaciones"

        context['records'] = self._record.get_all()
        context['all_utilitie'] = self._record.get_all_utility()
        context['all_customers'] = self._customers.get_count()
        context['count_deudas'] = self._record.get_debt_count()
        context['amount'] = self._record.get_debt_amount()
        return context


def get_records_by_date_range(request):
    start_date = request.POST.get('date-range-picker-start-date-myDateRangePickerCustomRanges')
    end_date = request.POST.get('date-range-picker-end-date-myDateRangePickerCustomRanges')
    if start_date is not '':
        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
    if end_date is not '':
        end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
    record_view = RecordView()
    customer_view = CustomerView()

    listado = record_view.get_records_by_date_range(start_date, end_date)
    list_row = []
    for record in listado:
        is_debtor_text = ''
        description = ''
        if record.is_debtor:
            is_debtor_text = '<span class ="badge bg-danger" title = "Esta grabación aún no se ha pagado"> ' + str(
                record.price) + '</span> '
        else:
            is_debtor_text = '<span class ="align-content-center text-center">' + str(record.price) + '</span>'
        if record.description:
            description = '<button class ="btn btn-primary btn-sm annotations" id = "" data-bs-toggle = "modal" ' \
                          'data-bss-tooltip = "" type = "button" data-bs-target = "#modal-show-annotation" ' \
                          'title = "Permite mostrar los elementos de la descripción" ' \
                          'data-description = "' + str(record.description) + '"> <i class ="far fa-eye"> </i> </button>'
        else:
            description = '<span> - </span>'
        record_row = '<tr class="text-start" id="' + str(record.pk) + '"><td>' \
                                                                      ' ' + str(record.date_record.strftime(
            "%d de %B de %Y")) + '</td><td class="align-items-xxl-center"><span role="button">' \
                                 '<img src="' \
                                 ' ' + str(
            record.customer.get_photo()) + '"class ="rounded-circle me-2 thumbnail" width = "30" ' \
                                           'height = "30" data-bs-toggle = "modal" ' \
                                           'data-bs-target = "#imagenModal" data-bss-tooltip = "" ' \
                                           'data-img = "' \
                                           ' ' + str(record.customer.get_photo()) + '" alt = "customer"></span> ' \
                                                                                    ' ' + str(
            record.customer.name) + ' <a class ="btn btn-secondary btn-sm" href = "' \
                                    '/app/customers/' + str(
            record.customer.pk) + '" style = "margin-left: 5px;"> <i class ="far fa-eye"> ' \
                                  '</i> </a> </td> <td>' \
                                  ' ' + str(is_debtor_text) + '</td><td>' \
                                                              ' ' + description + '</td> <td> <a href = "/app/record/update/' + str(
            record.pk) + '" class ="btn btn-primary btn-sm" role = "button" style = "margin-right: 5px;" title = "Permite editar los atributos de una grabación"> <i class ="fas fa-edit"> </i> </a> <button class ="btn btn-primary btn-sm" data-bs-toggle = "tooltip" data-bss-tooltip = "" type = "button" style = "margin-right: 5px;" title = "Permite mostrar los detalles de una grabación" > <i class ="fas fa-eye"> </i> </button> </td></tr> '
        list_row.append(record_row)
    # Enviar los datos al frontend
    response = {
        'data': list_row,
        'records_count': record_view.get_count(),
        'utility': record_view.get_all_utility(),
        'customers_count': customer_view.get_customer_count_by_date_range(start_date, end_date),
        'debt': record_view.get_debt_amount(),
        'debt_count': record_view.get_debt_count()
    }
    return JsonResponse(response, safe=True)


class CreateRecord(CreateView):
    template_name = 'records/create.html'
    form_class = RecordForm
    success_url = reverse_lazy('records_panel')
    _record = RecordView()
    _customers = CustomerView()

    def dispatch(self, request, *args, **kwargs):
        self._record = RecordView()
        self._customers = CustomerView()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_customers'] = self._customers.get_all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            # Validar que los datos no estén en blanco
            form.save()
            self.request.session['success_message_shown'] = True
            messages.success(self.request, "Grabación guardada correctamente")
            return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error en el campo {field}: {error}")
        return super().form_invalid(form)


class UpdateRecord(UpdateView):
    template_name = 'records/create.html'
    form_class = RecordForm
    model = Record
    success_url = reverse_lazy('records_panel')
    _record = RecordView()
    _customers = CustomerView()

    def dispatch(self, request, *args, **kwargs):
        self._record = RecordView()
        self._customers = CustomerView()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        http = self.request.POST.get('url')
        self.request.session['success_message_shown'] = True
        self.success_url = http
        form = RecordForm(self.request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Grabación editada correctamente")
            return super().form_valid(form)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f"Error en el campo {field}: {error}")
            return super().form_invalid(form)


class DeleteRecord(DeleteView):
    model = Record
    success_url = reverse_lazy("records_panel")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {
            'message': 'Elemento eliminado exitosamente'
        }
        return JsonResponse(data)
