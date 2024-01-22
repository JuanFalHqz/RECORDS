from django.contrib import admin
from apps.core.models import Annotation, Customer, Record

# Register your models here.
admin.site.register(Annotation)
admin.site.register(Customer)
admin.site.register(Record)
