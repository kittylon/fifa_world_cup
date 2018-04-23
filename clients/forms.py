from django import forms
from django.contrib.auth.models import User
from clients.models import Client
from django.contrib.auth.forms import UserCreationForm
from dal import autocomplete
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#Choices for the registration form (sex and id type)
ID_CHOICES = (('CC','Cédula'), ('PA','Pasaporte'), ('CE','Cédula de extranjería'))
SEX_CHOICES = (('M','Masculino'), ('F','Femenino'))

#Verifies if the value if correct
def validate_even(value):
    try:
        int(SignUpForm.value)
        print(SignUpForm.value)
    except Exception as e:
        raise ValidationError(
        _('%(value)s No es un número.'),
            params={'value': value},
        )

#Form for the new user
class SignUpForm(UserCreationForm):
    name = forms.CharField(label='Nombres')
    last_name = forms.CharField(label='Apellidos')
    email = forms.EmailField(label='Correo electrónico')
    birth_date = forms.DateField(label='Fecha de nacimiento (DD/MM/AAAA)', initial='DD/MM/AAAA')
    sex = forms.ChoiceField(label='Sexo',choices=SEX_CHOICES)
    document_type = forms.ChoiceField(label='Tipo de documento',choices=ID_CHOICES)
    document_number = forms.CharField(label='Número de documento')
    city = forms.CharField(label='Ciudad')
    phone = forms.IntegerField(label='Teléfono', required=False, max_value=9999999999, min_value=0000000000)
    mobile = forms.IntegerField(label='Celular',  max_value=999999999999, min_value=000000000000)
    address = forms.CharField(label='Dirección')
    company = forms.CharField(label='NIT de la empresa')
    #     queryset=Client.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='client-autocomplete')
    # )
    job_title = forms.CharField(label='Cargo en su empresa')

#metadata for the form
    class Meta:
        model = User
        fields = ('name', 'last_name', 'email', 'birth_date',
                'sex', 'document_type','document_number',
                'city', 'phone','mobile', 'address',
                'company','job_title','username',
                'password1','password2')
        help_texts = {
            'username': "Campo requerido. 150 caracteres o menos. Letras, dígitos y los únicos símbolos permitido son @/./+/-/_."
        }
