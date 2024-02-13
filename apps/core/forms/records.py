from django.forms import ModelForm, NumberInput, CheckboxInput, Select, TextInput, Textarea

from apps.core.models import Record


class RecordForm(ModelForm):
    field_order = ('customer', 'price', 'is_debtor', 'description')

    class Meta:
        model = Record
        fields = '__all__'

        widgets = {
            'price': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Por ej. 100',
                    'name': 'price',
                    'id': 'price',
                    'title': 'Precio de la grabación. Puede ser un número decimal por ej. 100.99',
                }
            ),
            'is_debtor': CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'name': 'is_debtor',
                    'id': 'formCheck-1',
                }
            ),
            'customer': Select(attrs={
                'id': 'single-select-field',
                'name': 'customer',
                'data-placeholder': 'Seleccione un cliente',
                'data-bs-toggle': 'tooltip',
                'data-bss-tooltip': '',
                'title': 'Clientes del sistema',
            }
            ),
            'description': Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'description',
                    'name': 'description',
                    'title': 'Anote los archivos a borrar y grabar',
                    'rows': 3,
                }
            ),
        }
