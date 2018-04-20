from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import  SignUpForm
from clients.models import Client, Profile
from world_cup.models import Team, RealMatch, UserMatch, UserTeam
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from dal import autocomplete
from django.db import IntegrityError
from django.db.models import Q
from django.contrib import messages
from datetime import date, datetime

class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Client.objects.all()

        if (self.q):
            # qs = qs.filter(name__startswith = self.q)
            qs = qs.filter(Q(nit__startswith = self.q))

        return qs

# Views to register a new user
class RegisterView(TemplateView):
    template_name = 'registration/register_user.html'

    @staticmethod
    def check_unique(email, document_type, document_number, company, birthday):
        today = date.today()
        age = int(abs((today - birthday).days / 365.25))
        company2 = Client.objects.get(name=company)
        companies = Profile.objects.filter(company=company).count()
        emails = User.objects.filter(email=email).count()
        email_pro = Profile.objects.filter(email=email).count()
        documents = Profile.objects.filter(document_type=document_type, document_number=document_number).count()
        message = ''
        error = False
        if companies >= int(company2.prof):
            message = 'La empresa en la que trabajas ya ocupó los ' + str(company2.prof) + ' cupos 😧.'
            error = True
            print('1')

        elif age < 18:
            message = 'Debes ser mayor de edad para participar 👶.'
            error = True
            print('2')

        elif int(emails) > 0 or int(documents) > 0 :
            if (int(emails) > 0 and int(documents) > 0):
                message = 'El email y el documento deben ser unicos 😧.'
                error = True
                print('3')
            elif int(emails) or int(email_pro) > 0:
                message = 'El email ya esta en uso 😧.'
                error = True
                print('4')
            else:
                message = 'El documento ya esta en uso 😧.'
                error = True
                print('5')

            print('6')
        return {
                'message': message,
                'error': error
                }

class OptionsView(TemplateView):
    template_name = 'clients/options.html'

# Home view for registered users
def home(request):
    return render(request, 'clients/home.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            check = RegisterView.check_unique(form.cleaned_data.get('email'), form.cleaned_data.get('document_type'), form.cleaned_data.get('document_number'), form.cleaned_data.get('company'), form.cleaned_data.get('birth_date'))
            if check['error'] == False:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.first_name = form.cleaned_data.get('name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.profile.email = form.cleaned_data.get('email')
                user.profile.birth_date = form.cleaned_data.get('birth_date')
                user.profile.sex = form.cleaned_data.get('sex')
                user.profile.document_type = form.cleaned_data.get('document_type')
                user.profile.document_number = form.cleaned_data.get('document_number')
                user.profile.city= form.cleaned_data.get('city')
                user.profile.phone= form.cleaned_data.get('phone')
                user.profile.mobile= form.cleaned_data.get('mobile')
                user.profile.address = form.cleaned_data.get('address')
                user.profile.company= form.cleaned_data.get('company')
                user.profile.job_title = form.cleaned_data.get('job_title')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('groups_phase')
                print('all good')
            else:
                messages.warning(request, check['message'])
    else:
        form = SignUpForm()
    return render(request, 'registration/register_user.html', {'form': form})
