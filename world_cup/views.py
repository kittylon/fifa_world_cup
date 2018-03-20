from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from world_cup.models import UserGuess, Match, Team
from django.contrib.auth.decorators import login_required
import json
# Views to register a new user

class GroupDetailView(TemplateView):
    template_name='world_cup/group_detail.html'
    model = Team

    def get(self, request, *args, **kwargs):
        query = self.kwargs['query']
        object_list =  Team.objects.filter(group=query)
        matches = []
        for team in object_list:
            matches += Match.objects.filter(team_one=team)
        return render(request, self.template_name, {'matches': matches, 'object_list': object_list} )


class GroupsView(TemplateView):
    template_name = 'world_cup/groups_phase.html'
    model = Match

    @staticmethod
    def save_gamble(user, match, team_one, team_two):
        obj_match = get_object_or_404(Match, pk=match)
        gamble = UserGuess(match=obj_match, team_one_score=team_one,
                        team_two_score=team_two, user=user)
        gamble.save()
        return gamble.pk

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        match_id = ''
        team_label = ''
        team_one = ''
        team_two = ''
        print(dict_gamble)
        for key, value in dict_gamble.items():
            match_id = key[0]
            team_label = key[-3:]
            if team_label == 'one':
                team_one = value
            elif team_label =='two':
                team_two = value

            if team_one != '' and team_two != '':
                GroupsView.save_gamble(user, match_id, team_one, team_two)
                team_one = ''
                team_two = ''

        return redirect('summary')

class SummaryView(TemplateView):
    template_name = 'world_cup/summary.html'

    # def get(self, request, *args, **kwargs):
    #     current_user = request.user
    #     print(current_user.id)
        # User = get_object_or_404(Guest, mail=mail)
        # gifts = Gift.objects.filter(guest_id=guest).count()
