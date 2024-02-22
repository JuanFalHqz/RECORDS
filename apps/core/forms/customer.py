from django.forms import ModelForm, TextInput, FileInput

from apps.core.models import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de cliente',
                    'name': 'name',
                    'id': 'customer-name',
                }
            ),
            'mobile': TextInput(
                attrs={
                    'class': 'form-control',
                    'name': 'mobile',
                    'id': 'customer-mobile',
                    'placeholder': 'Por ej: 55555555',
                }
            ),
        }
