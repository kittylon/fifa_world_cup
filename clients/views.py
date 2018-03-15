from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import  SignUpForm
from clients.models import Client, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# from django.db import transaction
# from django.utils.translation import gettext as _

# Views to register a new user
class RegisterView(TemplateView):
    template_name = 'registration/register_user.html'

class OptionsView(TemplateView):
    template_name = 'clients/options.html'

# Home view for registered users
def home(request):
    return render(request, 'clients/home.html')

# Home view for registered users
# @transaction.atomic
# def register_user(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = ProfileForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             # return redirect('home')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm()
#         profile_form = ProfileForm()
#     return render(request, 'registration/register_user.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
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
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register_user.html', {'form': form})
