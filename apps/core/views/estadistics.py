from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from apps.core.models import Record


class StatisticView(LoginRequiredMixin, ListView):
    template_name = 'statistics.html'
    queryset = Record.objects.all()
