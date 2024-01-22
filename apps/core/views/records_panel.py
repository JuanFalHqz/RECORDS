from django.views.generic import ListView, View
from apps.core.models import Record

class RecordsPanel(ListView):
    template_name= 'records_panel.html'
    queryset = Record.objects.all()