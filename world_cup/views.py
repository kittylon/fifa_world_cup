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
        object_list = UserMatch.objects.filter(group=group, user=request.user)
        return render(request, self.template_name, {'object_list': object_list} )


class GroupsView(TemplateView):
    template_name = 'world_cup/groups_phase.html'
    model = UserMatch

    @staticmethod
    def update_team(user, team, points, goals_favor, goals_against):
        team.points += int(points)
        team.goals_favor += int(goals_favor)
        team.goals_against += int(goals_against)
        team.save()
        return team.pk

    @staticmethod
    def define_points(user, user_match, score_one, score_two):
        points_one = 0
        points_two = 0
        if user_match.team_one_score == user_match.team_two_score:
            points_one = 1
            points_two = 1
        elif user_match.team_one_score > user_match.team_two_score:
            points_one = 3
            points_two = 0
        else:
            points_one = 0
            points_two = 3

        GroupsView.update_team(user, user_match.team_one, points_one, score_one, score_two)
        GroupsView.update_team(user, user_match.team_two, points_two, score_two, score_one)
        return user_match.pk

    @staticmethod
    def save_gamble(user, label, score_one, score_two):
        user_match = get_object_or_404(UserMatch, label=label, user=user)
        user_match.team_one_score = score_one
        user_match.team_two_score = score_two
        user_match.user = user
        user_match.gambled = True
        user_match.save()
        GroupsView.define_points(user, user_match, score_one, score_two)
        return user_match.pk

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        match_id = ''
        team_label = ''
        score_one = ''
        score_two = ''
        for key, value in dict_gamble.items():
            match_num, phase, group, team_num = key.split('_')
            if team_num == '1':
                score_one = value
            elif team_num == '2':
                score_two = value

            if score_one != '' and score_two != '':
                label = match_num +'_' + phase + '_' + group
                GroupsView.save_gamble(user, label, score_one, score_two)
                score_one = ''
                score_two = ''

        return redirect('summary')

class SummaryView(TemplateView):
    template_name = 'world_cup/summary.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def get(self, request, *args, **kwargs):
        SummaryView.sort_groups(request.user)
        object_list =  UserMatch.objects.filter(user=request.user, gambled=True)
        groups = SummaryView.sort_groups(request.user)
        # for group in SummaryView.groups:
        #     # import pdb; pdb.set_trace()
        #     filter_list = list(filter(lambda match: match.group == group, object_list))
        #     groups[group] = filter_list

        # SummaryView.sort_groups()
        return render(request, self.template_name, {'groups': groups, 'object_list': object_list} )

    @staticmethod
    def sort_groups(user):
        object_list =  UserMatch.objects.filter(user=user, gambled=True)
        groups = {}
        for group in SummaryView.groups:
            filter_list = list(filter(lambda match: match.group == group, object_list))
            groups[group] = filter_list
        SummaryView.order_group(user, groups)
        return groups

    @staticmethod
    def order_group(user, groups):
        for group, team in groups.items():
            print(group)
            print(team)
            # import pdb; pdb.set_trace()
            # filter_list = list(filter(lambda match: match.group == group, object_list))
            # groups[group] = filter_list

        return groups
        # object_list =  UserMatch.objects.filter(user=request.user, gambled=True)
        # object_list.sort(key=lambda team: team.points, reverse=True)
        # ordered_teams = sorted(ut, key=lambda x: x.count, reverse=True)
