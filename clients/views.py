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


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Client.objects.all()

        if (self.q):
            qs = qs.filter(name__startswith = self.q)

        return qs

# Views to register a new user
class RegisterView(TemplateView):
    template_name = 'registration/register_user.html'

class OptionsView(TemplateView):
    template_name = 'clients/options.html'

# Home view for registered users
def home(request):
    return render(request, 'clients/home.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.first_name = form.cleaned_data.get('name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.document_type = form.cleaned_data.get('document_type')
            user.profile.document_number = form.cleaned_data.get('document_number')
            user.profile.city= form.cleaned_data.get('city')
            user.profile.phone= form.cleaned_data.get('phone')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.company= form.cleaned_data.get('company')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('groups_phase')

    else:
        form = SignUpForm()
    return render(request, 'registration/register_user.html', {'form': form})
