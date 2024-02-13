from django.urls import include, path

from apps.core.views.dashboard import Dashboard
from apps.core.views.records_panel import RecordsPanel
from apps.core.views.customer import ListCustomers, DetailCustomer, CreateCustomer
from apps.core.views.records import ListRecords, CreateRecord, UpdateRecord, DeleteRecord, get_records_by_date_range
from apps.core.views.estadistics import EstadisticView

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('records_panel', RecordsPanel.as_view(), name='records_panel'),
    path('stadistics', EstadisticView.as_view(), name='stadistics'),

    path('records', ListRecords.as_view(), name='records'),
    path('records/search/', get_records_by_date_range, name='records_search'),
    path('record/create/', CreateRecord.as_view(), name='record_create'),
    path('record/update/<int:pk>', UpdateRecord.as_view(), name='record_update'),
    path('record/delete/<int:pk>', DeleteRecord.as_view(), name='record_delete'),

    path('customers', ListCustomers.as_view(), name='customers'),
    path('customers/<int:pk>', DetailCustomer.as_view(), name='detail_customers'),
    path('customers/create/', CreateCustomer.as_view(), name='customer_create'),

]
