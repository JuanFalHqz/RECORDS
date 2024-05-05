from random import randrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.generic import TemplateView


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def get_chart(request):
    serie = []
    counter = 0
    while counter < 3:
        serie.append(randrange(100, 400))
        counter = counter+1

    chart = {
        'xAxis': [
            {
                'type': "category",
                'data': ["Enero", "Febrero", "Marzo"]
            }
        ],
        'yAxis': [
            {
                'type': "value",
            }
        ],
        'series': [
            {
                'data': serie,
                'type': "line",

            }
        ]
    }

    return JsonResponse(chart)
