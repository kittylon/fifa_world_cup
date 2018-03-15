from django import forms
from django.contrib.auth.models import User
from clients.models import Client
from django.contrib.auth.forms import UserCreationForm

ID_CHOICES = (('Cédula','CC'), ('Pasaporte','PA'), ('Cedula_extranjería','CE'))

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    document_type = forms.ChoiceField(choices=ID_CHOICES)
    document_number = forms.CharField(label='Número de documento')
    city = forms.CharField(label='Ciudad')
    phone = forms.IntegerField(label='Teléfono')
    address = forms.CharField(label='Dirección')
    # company = forms.ModelChoiceField(queryset=Client.objects.all())
    job_title = forms.CharField(label='Cargo en su empresa')


    class Meta:
        model = User
        fields = ('birth_date', 'document_type',
                'document_number', 'city', 'phone',
                'address', 'job_title',
                'username','password1','password2')

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('birth_date', 'document_type',
#                 'document_number', 'city', 'phone',
#                 'address', 'company', 'job_title')
