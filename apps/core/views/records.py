from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, View
from apps.core.models import Record
from apps.core.views.customer import CustomerView

class RecordView(View):
    _all = None
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._all = Record.objects.all()
        
    def get_all(cls):
        print(cls._all)
        return cls._all

    def get_count(cls):
        return cls._all.count()
    
    def get_all_utilitie(cls):
        utilitie = 0
        for record in cls._all:
            utilitie +=record.price
        return utilitie

    def get_count_deuda(cls):
        count = 0
        for record in cls._all:
            if record.is_deudor:
                count+=1
        return count
    
    def get_amount_deuda(cls):
        amount = 0
        for record in cls._all:
            if record.is_deudor:
                amount+=record.price
        return amount


class ListRecords(ListView):
    template_name='records_list.html'
    _record = RecordView()
    _customers = CustomerView()
    queryset= Record.objects.all()

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self._record = RecordView()
        self._customers = CustomerView()
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # comun para todas las clases list
        #context['url_create'] = reverse_lazy('project_create_root')
        #context['url_delete'] = reverse_lazy('project_delete_root')
        # espesíficos
        context['records'] = self._record.get_all()
        context['all_utilitie'] = self._record.get_all_utilitie()
        context['all_customers'] = self._customers.get_count()
        context['count_deudas'] = self._record.get_count_deuda()
        context['amount'] = self._record.get_amount_deuda()
        
        return context
