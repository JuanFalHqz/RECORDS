"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from apps.core.views.dashboard import Dashboard
from apps.core.views.records_panel import RecordsPanel
from apps.core.views.customer import ListCustomers
from apps.core.views.records import ListRecords
from apps.core.views.estadistics import EstadisticView

urlpatterns = [
    path('dashboard', Dashboard.as_view() , name='dashboard'),
    path('records_panel', RecordsPanel.as_view() , name='records_panel'),
    path('customers', ListCustomers.as_view() , name='customers'),
    path('records', ListRecords.as_view() , name='records'),
    path('stadistics', EstadisticView.as_view() , name='stadistics'),
]
