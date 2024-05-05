from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import ListView, View
from apps.core.models import Record, Customer
from apps.core.views.customer import CustomerView
from apps.core.views.records import RecordView


class RecordsPanel(LoginRequiredMixin, ListView):
    """
    Toda la información es diaria.

    Tengo una relación de uno a muchos donde un customer tiene muchos record. Necesito todos los customer que tienen
    records en el día actual. Esto usando django y su orm. Dame el código.
    """
    template_name = 'records_panel.html'
    queryset = Record.objects.filter(date_record__day=timezone.now().date().day,
                                     date_record__month=timezone.now().date().month,
                                     date_record__year=timezone.now().year)
    _record = RecordView()
    _customers = CustomerView()

    def dispatch(self, request, *args, **kwargs):
        self._record = RecordView()
        self._customers = CustomerView()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['utility'] = self._record.get_all_utility_by_current_day()
        context['debit_count'] = self._record.get_debt_count_by_current_day()
        context['debit_amount'] = self._record.get_debt_amount_by_current_day()
        # context['customers'] = [record.customer for record in self.queryset]
        context['customers'] = self._customers.get_customer_by_current_day()
        context['all_customers'] = self._customers.get_all()
        return context
