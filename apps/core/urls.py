from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from apps.core.views.dashboard import Dashboard, get_chart
from apps.core.views.login import LoginViewCustom, CustomLogoutView
from apps.core.views.records_panel import RecordsPanel
from apps.core.views.customer import ListCustomers, DetailCustomer, CreateCustomer, UpdateCustomer, DeleteCustomer
from apps.core.views.records import ListRecords, CreateRecord, UpdateRecord, DeleteRecord, get_records_by_date_range
from apps.core.views.estadistics import StatisticView
from apps.core.views.user import UserList

urlpatterns = [
    path('', RedirectView.as_view(url='dashboard/')),


    path('login/', LoginViewCustom.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('usuarios/', UserList.as_view(), name='users'),


    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('dashboard/get_chart/', get_chart, name='chart'),
    path('records_panel/', RecordsPanel.as_view(), name='records_panel'),
    path('stadistics/', StatisticView.as_view(), name='stadistics'),

    path('records', ListRecords.as_view(), name='records'),
    path('records/search/', get_records_by_date_range, name='records_search'),
    path('record/create/', CreateRecord.as_view(), name='record_create'),
    path('record/update/<int:pk>', UpdateRecord.as_view(), name='record_update'),
    path('record/delete/<int:pk>', DeleteRecord.as_view(), name='record_delete'),

    path('customers', ListCustomers.as_view(), name='customers'),
    path('customers/<int:pk>', DetailCustomer.as_view(), name='detail_customers'),
    path('customers/create/', CreateCustomer.as_view(), name='customer_create'),
    path('customers/update/<int:pk>', UpdateCustomer.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>', DeleteCustomer.as_view(), name='customer_delete'),

]
