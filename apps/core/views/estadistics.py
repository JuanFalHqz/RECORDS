from django.views.generic import ListView, View
from apps.core.models import Record


class EstadisticView(ListView):
    template_name = 'estadistics.html'
    queryset = Record.objects.all()
