
from django.db import models
# Create your models here.
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static
from django.utils import timezone

from config.settings.base import MEDIA_URL


class Customer(models.Model):
    photo = models.ImageField(upload_to='customers/%Y/%m/%d/', null=True, blank=True)
    name = models.CharField(max_length=25, verbose_name='Nombre')
    date_join = models.DateTimeField(auto_now_add=True, )
    mobile = models.BigIntegerField(null=True, blank=True)

    def to_json(self):
        return {
            'photo': self.photo.url,
            'name': self.name,
            'date_join': self.date_join,
            'mobile': self.mobile,
        }

    def __str__(self):
        return self.name

    def get_photo(self):
        if self.photo:
            return str(MEDIA_URL) + (str(self.photo))
        else:
            return static('assets/img/avatars/customer.png')

    def get_utility(self):
        return self.record_set.aggregate(tp=Sum('price'))['tp']

    def get_debts(self):
        return self.record_set.filter(is_debtor=True)

    def get_debt_amount(self):
        debt = 0
        debt = self.record_set.filter(is_debtor=True).aggregate(tp=Sum('price'))['tp']
        return debt

    def get_debt_count(self):
        debt = 0
        debt = self.record_set.filter(is_debtor=True).count()
        return debt

    # daily
    def get_customers_by_current_date(self):
        return self.record_set.filter(record__date_record__day=timezone.now().date().day,
                                      record__date_record__month=timezone.now().date().month,
                                      record__date_record__year=timezone.now().year)


class Record(models.Model):
    price = models.FloatField(verbose_name='Precio')
    is_debtor = models.BooleanField(default=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    date_record = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    def __str__(self):
        return f"Grabación de {self.customer.name} de ${self.price}"


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)

    def get_photo(self):
        if self.photo:
            return str(MEDIA_URL) + (str(self.photo))
        else:
            return static('assets/img/avatars/customer.png')


class Message(models.Model):
    receptor = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name='receptor_user')
    sender = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name='sender_user')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return self.content
