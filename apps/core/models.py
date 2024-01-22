from django.db import models
# Create your models here.
from django.db.models import ManyToManyField
from django.contrib.auth.models import User


class Customer(models.Model):
    # photo = models.ImageField(upload_to='/%d/%m/%Y/', null=True, blank=True)
    name = models.CharField(max_length=25)
    date_join = models.DateTimeField(auto_now_add=True,)
    
    def __str__(self):
        return self.name


class Annotation(models.Model):
    to_deleted = models.CharField(max_length=25)
    to_records = models.CharField(max_length=25)
    
    def __str__(self):
        return self.to_records


class Record(models.Model):
    price = models.FloatField()
    is_deudor = models.BooleanField(default=False)
    annotation = models.OneToOneField(Annotation,on_delete=models.RESTRICT, null=True, blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.RESTRICT)
    
    def __str__(self):
        return f"Grabación de {self.customer.name} de ${self.price}"


class Message(models.Model):

    receptor = models.ForeignKey(User,on_delete=models.RESTRICT, related_name='receptor_user')
    sender = models.ForeignKey(User,on_delete=models.RESTRICT,related_name='sender_user')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return self.content