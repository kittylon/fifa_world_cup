from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from .forms import  SignUpForm
from clients.models import Client, Profile
from world_cup.models import Team, RealMatch, UserMatch, UserTeam
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
            real_matches = RealMatch.objects.all()
            all_teams = Team.objects.all()
            for team in all_teams:
                new_user_team = UserTeam(country = team.country,
                                        group = team.group,
                                        user=user)
                new_user_team.save()
            user_teams = UserTeam.objects.filter(user=user)
            team_one_user = ''
            team_two_user = ''
            for real_match in real_matches:

                    for team in user_teams:
                        if real_match.team_one.country == team.country:
                            team_one_user = team

                        elif real_match.team_two.country == team.country:
                            team_two_user = team

                        if team_one_user != '' and team_two_user != '':
                            new_user_match = UserMatch(label=real_match.label,
                                                        date=real_match.date,
                                                        phase=real_match.phase,
                                                        group=real_match.group,
                                                        team_one=team_one_user,
                                                        team_two=team_two_user,
                                                        user=user)
                            new_user_match.save()
                            team_one_user = ''
                            team_two_user = ''
            return redirect('groups_phase')

    else:
        form = SignUpForm()
    return render(request, 'registration/register_user.html', {'form': form})
