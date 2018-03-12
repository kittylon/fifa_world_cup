from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import RegisterForm
from clients.models import Client, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Views to register a new user
class RegisterView(TemplateView):
    template_name = 'registration/register_user.html'

class OptionsView(TemplateView):
    template_name = 'clients/options.html'

# Home view for registered users
def home(request):
    return render(request, 'clients/home.html')

# Home view for registered users
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.company = form.cleaned_data.get('company')
            # user.profile.document_type = form.form.cleaned_data.get('document_type')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register_user.html', {'form': form})
    #     data = form.cleaned_data
    #     username = form.cleaned_data(str('email'))
    #     raw_password = form.cleaned_data('document_number')
    #
    #     profile = Profile.objects.create(
    #             birth_date=data['birth_date'],
    #             # document_type=data["document_type"],
    #             document_number=data['document_number'],
    #             city=data['city'],
    #             phone=data['phone'],
    #             address=data['address'],
    #             job_title=data['job_title'],
    #             company=data['company']
    #             )
    #
    #     return JsonResponse(
    #         {
    #             'document_number': profile.document_number,
    #             'company': str(profile.company.name),
    #             'birth_date': profile.birth_date,
    #         }
    #     )
    #
    # else:
    #     return render(request, 'registration/register_user.html', {'form': form})
