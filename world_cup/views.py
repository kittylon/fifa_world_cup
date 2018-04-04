from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from world_cup.models import RealMatch, UserMatch, Team, UserTeam
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

class SummaryFinalsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/finals_summary.html'
    winner = {'1_Finals': ''}
    loser = {'1_Finals': ''}

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='Finals')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

class FinalsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/finals_phase.html'
    winner = {'1_Finals': ''}
    loser = {'1_Finals': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, phase='Finals')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def set_loser(user, label, user_team):
        FinalsView.loser[label] = user_team
        return

    @staticmethod
    def set_winner(user, label, user_team):
        FinalsView.winner[label] = user_team
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
        request.user.profile.final_filled = True
        request.user.save()
        return redirect('finals_summary')

class SummaryTercerCuartoView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/third_fourth_summary.html'
    winners = {'1_Semi': '', '2_Semi': ''}

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='3y4')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

class TercerCuartoView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/third_fourth_phase.html'
    winner = {'1_3y4': ''}
    loser = {'1_3y4': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, phase='3y4')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def set_loser(user, label, user_team):
        TercerCuartoView.loser[label] = user_team
        return

    @staticmethod
    def set_winner(user, label, user_team):
        TercerCuartoView.winner[label] = user_team
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
        request.user.profile.trd_fth_filled = True
        request.user.save()
        return redirect('third_fourth_summary')

class SummarySemiView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/semi_summary.html'
    winners = {'1_Semi': '', '2_Semi': ''}

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='Semi')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

class SemiView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/semi_phase.html'
    winners = {'1_Semi': '', '2_Semi': ''}
    losers = {'1_Semi': '', '2_Semi': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, phase='Semi')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def create_third_fourth(user):
        EightsView.create_match(user, '1_3y4', '3y4', SemiView.losers['1_Semi'], SemiView.losers['2_Semi'], '2018-07-14')
        return

    @staticmethod
    def create_final(user):
        EightsView.create_match(user, '1_Finals', 'Finals', SemiView.winners['1_Semi'], SemiView.winners['2_Semi'], '2018-07-15')
        return

    @staticmethod
    def set_loser(user, label, user_team):
        SemiView.losers[label] = user_team
        return

    @staticmethod
    def set_winner(user, label, user_team):
        SemiView.winners[label] = user_team
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
        SemiView.create_final(user)
        SemiView.create_third_fourth(user)
        request.user.profile.semi_filled = True
        request.user.save()
        return redirect('semi_summary')

class SummaryFourthsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/fourths_summary.html'
    winners = {'1_Cuartos': '', '2_Cuartos': '', '3_Cuartos': '',
                    '4_Cuartos': ''}

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='Cuartos')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

class FourthsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/fourths_phase.html'
    winners = {'1_Cuartos': '', '2_Cuartos': '', '3_Cuartos': '',
                    '4_Cuartos': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, phase='Cuartos')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def create_semi(user):
        EightsView.create_match(user, '1_Semi', 'Semi', FourthsView.winners['1_Cuartos'], FourthsView.winners['2_Cuartos'], '2018-07-10')
        EightsView.create_match(user, '2_Semi', 'Semi', FourthsView.winners['3_Cuartos'], FourthsView.winners['4_Cuartos'], '2018-07-11')
        return

    @staticmethod
    def set_winner(user, label, user_team):
        FourthsView.winners[label] = user_team
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
        FourthsView.create_semi(user)
        request.user.profile.fourths_filled = True
        request.user.save()
        return redirect('fourths_summary')

class SummaryEightsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/eights_summary.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='Eights')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

class EightsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
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
        EightsView.create_match(user, '1_Fourths', 'Cuartos', EightsView.winners['1_Octavos'], EightsView.winners['2_Octavos'], '2018-07-06')
        EightsView.create_match(user, '2_Fourths', 'Cuartos', EightsView.winners['3_Octavos'], EightsView.winners['4_Octavos'], '2018-07-06')
        EightsView.create_match(user, '3_Fourths', 'Cuartos', EightsView.winners['5_Octavos'], EightsView.winners['6_Octavos'], '2018-07-07')
        EightsView.create_match(user, '4_Fourths', 'Cuartos', EightsView.winners['7_Octavos'], EightsView.winners['8_Octavos'], '2018-07-07')
        return

    @staticmethod
    def create_match(user, label, phase, team_one, team_two, date='2018-07-02'):
        new_match = UserMatch(user=user, label=label, phase=phase,
                            team_one=team_one, team_two=team_two, date=date)
        new_match.save()
        return

    @staticmethod
    def set_winner(user, label, user_team):
        EightsView.winners[label] = user_team
        return

    @staticmethod
    def organize_scores(user, dict):
        label = ''
        score_one = ''
        score_two = ''
        penals_one = ''
        penals_two = ''
        for key, value in dict_gamble.items():
            if key == value:
                label = key[:-1]

            match_label, type_score = key.split('|')

            if len(type_score) > 2:
                type, team = type_score.split('_')
                if label == match_label and type == 'real' and team == '1':
                    score_one = value
                elif label == match_label and type == 'real' and team == '2':
                    score_two = value
                elif label == match_label and type == 'penals' and team == '1':
                    penals_one = value
                elif label == match_label and type == 'penals' and team == '2':
                    penals_two = value
                print(score_one, score_two, penals_one, penals_two)

            if score_one != '' and score_two != '' and penals_one != '' and penals_two != '':
                GroupsView.save_gamble(user, label, score_one, score_two, penals_one, penals_two)
                score_one = ''
                score_two = ''
                penals_one = ''
                penals_two = ''

        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        organize_scores(user, dict_gamble)

        # EightsView.create_fourths(user)
        # request.user.profile.eights_filled = True
        # request.user.save()
        # return redirect('eights_summary')

    @staticmethod
    def create_eight(user, players):
        EightsView.create_match(user, '1_Eights', 'Eights', players['A'][0], players['B'][1], '2018-06-30')
        EightsView.create_match(user, '2_Eights', 'Eights', players['C'][0], players['D'][1], '2018-06-30')
        EightsView.create_match(user, '3_Eights', 'Eights', players['E'][0], players['F'][1], '2018-07-02')
        EightsView.create_match(user, '4_Eights', 'Eights', players['G'][0], players['H'][1], '2018-07-02')
        EightsView.create_match(user, '5_Eights', 'Eights', players['A'][1], players['B'][0], '2018-07-01')
        EightsView.create_match(user, '6_Eights', 'Eights', players['C'][1], players['D'][0], '2018-07-01')
        EightsView.create_match(user, '7_Eights', 'Eights', players['E'][1], players['F'][0], '2018-07-03')
        EightsView.create_match(user, '8_Eights', 'Eights', players['G'][1], players['H'][0], '2018-07-03')
        return

class GroupsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/groups_phase.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    model = UserMatch

    def get(self, request, *args, **kwargs):
        groups = {}
        if request.user.is_staff:
            return redirect('reypar_admin')
        # elif request.user.profile.groups_filled == True:
        #     return redirect('groups_summary')
        else:
            object_list = UserMatch.objects.filter(user=request.user, phase='Groups')

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
        for group in GroupsView.groups:
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
    def check_phase(user, label, winner, loser):
        if "Octavos" in label:
            EightsView.set_winner(user, label, winner)
        elif "Cuartos" in label:
            FourthsView.set_winner(user, label, winner)
        elif "Semi" in label:
            SemiView.set_winner(user, label, winner)
            SemiView.set_loser(user, label, loser)
        elif "3y4" in label:
            TercerCuartoView.set_winner(user, label, winner)
            TercerCuartoView.set_loser(user, label, loser)
        elif "Finals" in label:
            TercerCuartoView.set_winner(user, label, winner)
            TercerCuartoView.set_loser(user, label, loser)
        else:
            print("etapa grupos, no hay orden")
        return

    @staticmethod
    def define_points(user, label, user_match, score_one, score_two):
        points_one = 0
        points_two = 0
        if user_match.team_one_score == user_match.team_two_score:
            points_one = 1
            points_two = 1
            winner = None
            loser = None
        elif user_match.team_one_score > user_match.team_two_score:
            points_one = 3
            points_two = 0
            winner = user_match.team_one
            loser = user_match.team_two
        else:
            points_one = 0
            points_two = 3
            winner = user_match.team_two
            loser = user_match.team_one

        GroupsView.check_phase(user, label, winner, loser)
        GroupsView.update_team(user, user_match.team_one, points_one, score_one, score_two)
        GroupsView.update_team(user, user_match.team_two, points_two, score_two, score_one)
        return user_match.pk

    @staticmethod
    def save_gamble(user, label, score_one, score_two, penals_one, penals_two):
        user_match = get_object_or_404(UserMatch, label=label, user=user)
        user_match.team_one_score = score_one
        user_match.team_two_score = score_two
        if penals_one == '' and penals_two == '':
            penals_one = 0
            penals_two = 0

        user_match.penals_team_one = penals_one
        user_match.penals_team_two = penals_two
        user_match.user = user
        user_match.gambled = True
        user_match.save()
        GroupsView.define_points(user, label, user_match, score_one, score_two)
        return user_match.pk

    @staticmethod
    def score_matches(user, dict_gamble):
        label = ''
        score_one = ''
        score_two = ''
        penals_one = ''
        penals_two = ''
        for key, value in dict_gamble.items():
            if key == value:
                label = key[:-1]
            match_label, type_score = key.split('|')

            if len(type_score) > 2:
                type, team = type_score.split('_')
                if label == match_label and type == 'real' and team == '1':
                    score_one = value
                elif label == match_label and type == 'real' and team == '2':
                    score_two = value
                elif label == match_label and type == 'penals' and team == '1':
                    penals_one = value
                elif label == match_label and type == 'penals' and team == '2':
                    penals_two = value

            if score_one != '' and score_two != '' and ((penals_one != '' and penals_two != '') or ('Groups' in label)):
                GroupsView.save_gamble(user, label, score_one, score_two, penals_one, penals_two)
                score_one = ''
                score_two = ''
                penals_one = ''
                penals_two = ''

        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        GroupsView.score_matches(user, dict_gamble)
        GroupsView.sort_groups(user)
        request.user.profile.groups_filled = True
        request.user.save()
        return redirect('groups_phase')
#
# class SummaryGroupsView(LoginRequiredMixin, TemplateView):
#     login_url = '/login/'
#     template_name = 'world_cup/groups_summary.html'
#     groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
#
#     def get(self, request, *args, **kwargs):
#         try:
#             object_list =  UserMatch.objects.filter(user=request.user, gambled=True, phase='Groups')
#         except:
#             raise Http404
#         groups = {}
#         for group in SummaryGroupsView.groups:
#             x = filter(lambda match: match.group == group, object_list)
#             # import pdb; pdb.set_trace()
#             filter_list = list(filter(lambda match: match.group == group, object_list))
#             groups[group] = filter_list
#         # SummaryGroupsView.sort_groups(request.user)
#         return render(request, self.template_name, {'groups': groups, 'object_list': object_list} )

class ReyparAdminView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/reypar_admin'

    def test_func(self):
        return test_settings(self.request.user)
