from django.views.generic import ListView

from apps.core.models import CustomUser


class UserList(ListView):
    template_name = 'users.html'
    queryset = CustomUser.objects.all()
