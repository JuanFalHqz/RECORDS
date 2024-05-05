from django.contrib import admin
from apps.core.models import Customer, Record, CustomUser

# Register your models here.
admin.site.register(Customer)
admin.site.register(Record)
admin.site.register(CustomUser)
