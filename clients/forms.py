from django import forms
from clients.models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ID_CHOICES = (('Cédula','CC'), ('Pasaporte','PA'), ('Cedula_extranjería','CE'))

class RegisterForm(UserCreationForm):
    company = forms.ModelChoiceField(queryset=Client.objects.all())
    # first_name = forms.CharField(label='Primer Nombre')
    birth_date = forms.DateField(label='Fecha de Nacimiento')
    # document_type = forms.ChoiceField(choices=ID_CHOICES)
    # document_number = forms.CharField(label='Número de documento')
    # city = forms.CharField(label='Ciudad')
    # phone = forms.IntegerField(label='Teléfono', min_value=3000000000, max_value=3999999999)
    # address = forms.CharField(label='Dirección')
    # job_title = forms.CharField(label='Cargo en su empresa')
    # email = forms.EmailField(label='correo electrónico')

    class Meta:
        model = User
        fields = (
                    'username',
                    'password1',
                    'password2',
                    # 'company',
                    # 'first_name',
                    'birth_date'
                    # 'document_type',
                    # 'document_number',
                    # 'city',
                    # 'phone',
                    # 'address',
                    # 'job_title',
                    # 'email',
                )
