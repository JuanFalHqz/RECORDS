from typing import Any
from django.views.generic import ListView,View
from apps.core.models import Customer

class CustomerView(View):
    _all = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._all = Customer.objects.all()

    def get_all(cls):
        return cls._all
    
    def get_count(cls):
        return cls._all.count()

class ListCustomers(ListView):
    template_name='customers_list.html'
    queryset=Customer.objects.all()
