from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from world_cup.models import RealMatch, UserMatch, Team
from django.contrib.auth.decorators import login_required
import json
# Views to register a new user

class GroupDetailView(TemplateView):
    template_name='world_cup/group_detail.html'
    model = UserMatch

    def get(self, request, *args, **kwargs):
        group = self.kwargs['query']
        object_list = UserMatch.objects.filter(group=group)
        return render(request, self.template_name, {'object_list': object_list} )


class GroupsView(TemplateView):
    template_name = 'world_cup/groups_phase.html'
    model = UserMatch

    @staticmethod
    def save_gamble(user, match, team_one, team_two):
        user_match = get_object_or_404(UserMatch, pk=match)
        user_match.team_one_score = team_one
        user_match.team_two_score = team_two
        user_match.user = user
        user_match.gambled = True
        user_match.save()
        return user_match.pk

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

    def get(self, request, *args, **kwargs):
        object_list =  UserMatch.objects.filter(user=request.user, gambled=True)
        return render(request, self.template_name, {'object_list': object_list} )
