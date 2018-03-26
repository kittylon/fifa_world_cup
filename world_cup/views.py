from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from world_cup.models import RealMatch, UserMatch, Team, UserTeam
from django.contrib.auth.decorators import login_required
from django.http import Http404

class SummaryEightsView(TemplateView):
    template_name = 'world_cup/eights_summary.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='Eights')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

class EightsView(TemplateView):
    template_name = 'world_cup/eights_phase.html'
    winners = {'1_Octavos': '', '2_Octavos': '', '3_Octavos': '',
                    '4_Octavos': '', '5_Octavos': '', '6_Octavos': '',
                    '7_Octavos': '', '8_Octavos': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list = UserMatch.objects.filter(user=request.user, phase='Eights')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def create_fourths(user):
        EightsView.create_match(user, '1_Cuartos', 'Cuartos', EightsView.winners['1_Octavos'], EightsView.winners['2_Octavos'])
        EightsView.create_match(user, '2_Cuartos', 'Cuartos', EightsView.winners['3_Octavos'], EightsView.winners['4_Octavos'])
        EightsView.create_match(user, '3_Cuartos', 'Cuartos', EightsView.winners['5_Octavos'], EightsView.winners['6_Octavos'])
        EightsView.create_match(user, '4_Cuartos', 'Cuartos', EightsView.winners['7_Octavos'], EightsView.winners['8_Octavos'])
        return

    @staticmethod
    def create_match(user, label, phase, team_one, team_two):
        new_match = UserMatch(user=user, label=label, phase=phase,
                            team_one=team_one, team_two=team_two)
        new_match.save()
        return

    @staticmethod
    def set_winner(user, label, user_team):
        EightsView.winners[label] = user_team
        print(EightsView.winners)
        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        match_id = ''
        team_label = ''
        score_one = ''
        score_two = ''
        for key, value in dict_gamble.items():
            match_num, phase, team_num = key.split('_')
            if team_num == '1':
                score_one = value
            elif team_num == '2':
                score_two = value

            if score_one != '' and score_two != '':
                label = match_num +'_' + phase
                GroupsView.save_gamble(user, label, score_one, score_two)
                score_one = ''
                score_two = ''
        EightsView.create_fourths(user)
        return redirect('eights_summary')

    @staticmethod
    def create_eight(user, players):
        EightsView.create_match(user, '1_Octavos', 'Eights', players['A'][0], players['B'][1])
        EightsView.create_match(user, '2_Octavos', 'Eights', players['C'][0], players['D'][1])
        EightsView.create_match(user, '3_Octavos', 'Eights', players['E'][0], players['F'][1])
        EightsView.create_match(user, '4_Octavos', 'Eights', players['G'][0], players['H'][1])
        EightsView.create_match(user, '5_Octavos', 'Eights', players['A'][1], players['B'][0])
        EightsView.create_match(user, '6_Octavos', 'Eights', players['C'][1], players['D'][0])
        EightsView.create_match(user, '7_Octavos', 'Eights', players['E'][1], players['F'][0])
        EightsView.create_match(user, '8_Octavos', 'Eights', players['G'][1], players['H'][0])
        return

class GroupsView(TemplateView):
    template_name = 'world_cup/groups_phase.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    model = UserMatch

    def get(self, request, *args, **kwargs):
        object_list = UserMatch.objects.filter(user=request.user, phase='Groups')
        groups = {}
        for group in GroupsView.groups:
            x = filter(lambda match: match.group == group, object_list)
            # import pdb; pdb.set_trace()
            filter_list = list(filter(lambda match: match.group == group, object_list))
            groups[group] = filter_list
        return render(request, self.template_name, {'groups': groups, 'object_list': object_list} )

    @staticmethod
    def sort_groups(user):
        user_teams = UserTeam.objects.filter(user=user).order_by('group','-points','-goals_favor', 'goals_against')
        players = {}
        for group in SummaryGroupsView.groups:
            x = filter(lambda match: match.group == group, user_teams)
            # import pdb; pdb.set_trace()
            filter_list = list(filter(lambda match: match.group == group, user_teams))
            players[group] = filter_list[:2]
        EightsView.create_eight(user, players)
        return user_teams

    @staticmethod
    def update_team(user, team, points, goals_favor, goals_against):
        team.points += int(points)
        team.goals_favor += int(goals_favor)
        team.goals_against += int(goals_against)
        team.save()
        return team.pk

    @staticmethod
    def check_phase(user, label, winner):
        if "Octavos" in label:
            EightsView.set_winner(user, label, winner)
        else:
            print("otra etapa")
        return

    @staticmethod
    def define_points(user, label, user_match, score_one, score_two):
        points_one = 0
        points_two = 0
        if user_match.team_one_score == user_match.team_two_score:
            points_one = 1
            points_two = 1
            winner = None
        elif user_match.team_one_score > user_match.team_two_score:
            points_one = 3
            points_two = 0
            winner = user_match.team_one
        else:
            points_one = 0
            points_two = 3
            winner = user_match.team_two

        GroupsView.check_phase(user, label, winner)
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
        GroupsView.define_points(user, label, user_match, score_one, score_two)
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
        GroupsView.sort_groups(user)
        return redirect('groups_summary')

class SummaryGroupsView(TemplateView):
    template_name = 'world_cup/groups_summary.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='Groups')
        except:
            raise Http404
        groups = {}
        for group in SummaryGroupsView.groups:
            x = filter(lambda match: match.group == group, object_list)
            # import pdb; pdb.set_trace()
            filter_list = list(filter(lambda match: match.group == group, object_list))
            groups[group] = filter_list
        # SummaryGroupsView.sort_groups(request.user)
        return render(request, self.template_name, {'groups': groups, 'object_list': object_list} )
