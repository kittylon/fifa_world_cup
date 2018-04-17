from django import forms
from django.contrib.auth.models import User
from clients.models import Client
from django.contrib.auth.forms import UserCreationForm
from dal import autocomplete

ID_CHOICES = (('CC','Cédula'), ('PA','Pasaporte'), ('CE','Cédula de extranjería'))
SEX_CHOICES = (('M','Masculino'), ('F','Femenino'))

class SignUpForm(UserCreationForm):
    name = forms.CharField(label='Nombres')
    last_name = forms.CharField(label='Apellidos')
    email = forms.EmailField(label='Correo electrónico')
    birth_date = forms.DateField(label='Fecha de nacimiento (DD/MM/AAAA)')
    sex = forms.ChoiceField(label='Sexo',choices=SEX_CHOICES)
    document_type = forms.ChoiceField(label='Tipo de documento',choices=ID_CHOICES)
    document_number = forms.CharField(label='Número de documento')
    city = forms.CharField(label='Ciudad')
    phone = forms.IntegerField(label='Teléfono')
    mobile = forms.IntegerField(label='Celular')
    address = forms.CharField(label='Dirección')
    company = forms.ModelChoiceField(label='Empresa',
        queryset=Client.objects.all(),
        widget=autocomplete.ModelSelect2(url='client-autocomplete')
    )
    job_title = forms.CharField(label='Cargo en su empresa')

    class Meta:
        model = User
        fields = ('name', 'last_name', 'email', 'birth_date',
                'sex', 'document_type','document_number',
                'city', 'phone','mobile', 'address',
                'company','job_title','username',
                'password1','password2')
