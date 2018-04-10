from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from world_cup.models import RealMatch, UserMatch, Team, UserTeam
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.contrib import messages

class FinalsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/finals_phase.html'
    winners = {'1_Finals': ''}
    losers = {'1_Finals': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, phase='Finals')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def fill_winners(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='Finals')
        for match in user_matches:
            for key, value in FinalsView.winners.items():
                if match.label == key:
                    FinalsView.winners[key] = match.winner
        return

    @staticmethod
    def fill_losers(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='Finals')
        for match in user_matches:
            for key, value in FinalsView.losers.items():
                if match.label == key:
                    FinalsView.losers[key] = match.loser
        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        TercerCuartoView.fill_winners(user)
        TercerCuartoView.fill_losers(user)
        GroupsView.score_matches(user, dict_gamble)
        TercerCuartoView.check_winners(user)
        return redirect('finals_phase')

class TercerCuartoView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/third_fourth_phase.html'
    winners = {'1_3y4': ''}
    losers = {'1_3y4': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, phase='3y4')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def check_winners(user):
        counter = 0
        for key, value in TercerCuartoView.winners.items():
            if len(str(value)) > 2:
                counter += 1
        if counter == 1:
            user.profile.trd_fth_filled = True
            user.save()
        return

    @staticmethod
    def fill_winners(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='3y4')
        for match in user_matches:
            for key, value in TercerCuartoView.winners.items():
                if match.label == key:
                    TercerCuartoView.winners[key] = match.winner
        return

    @staticmethod
    def fill_losers(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='3y4')
        for match in user_matches:
            for key, value in TercerCuartoView.losers.items():
                if match.label == key:
                    TercerCuartoView.losers[key] = match.loser
        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        FinalsView.fill_winners(user)
        FinalsView.fill_losers(user)
        GroupsView.score_matches(user, dict_gamble)
        return redirect('third_fourth_phase')

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
    def check_winners(user):
        counter = 0
        for key, value in SemiView.winners.items():
            if len(str(value)) > 2:
                counter += 1
        if counter == 2:
            SemiView.create_third_fourth(user)
            SemiView.create_final(user)
            user.profile.semi_filled = True
            user.save()
        return

    @staticmethod
    def fill_winners(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='Semi')
        for match in user_matches:
            for key, value in SemiView.winners.items():
                if match.label == key:
                    SemiView.winners[key] = match.winner

        return

    @staticmethod
    def fill_losers(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='Semi')
        for match in user_matches:
            for key, value in SemiView.losers.items():
                if match.label == key:
                    SemiView.losers[key] = match.loser

        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        SemiView.fill_winners(user)
        SemiView.fill_losers(user)
        GroupsView.score_matches(user, dict_gamble)
        SemiView.check_winners(user)
        return redirect('semi_phase')

class FourthsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/fourths_phase.html'
    winners = {'1_Fourths': '', '2_Fourths': '', '3_Fourths': '',
                    '4_Fourths': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list =  UserMatch.objects.filter(user=request.user, phase='Fourths')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def create_semi(user):
        EightsView.create_match(user, '1_Semi', 'Semi', FourthsView.winners['1_Fourths'], FourthsView.winners['2_Fourths'], '2018-07-10')
        EightsView.create_match(user, '2_Semi', 'Semi', FourthsView.winners['3_Fourths'], FourthsView.winners['4_Fourths'], '2018-07-11')
        return

    @staticmethod
    def check_winners(user):
        counter = 0
        for key, value in FourthsView.winners.items():
            if len(str(value)) > 2:
                counter += 1
        if counter == 4:
            FourthsView.create_semi(user)
            user.profile.fourths_filled = True
            user.save()
        return

    @staticmethod
    def fill_winners(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='Fourths')
        for match in user_matches:
            for key, value in FourthsView.winners.items():
                if match.label == key:
                    FourthsView.winners[key] = match.winner

        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        FourthsView.fill_winners(user)
        GroupsView.score_matches(user, dict_gamble)
        FourthsView.check_winners(user)
        return redirect('fourths_phase')

class EightsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/eights_phase.html'
    winners = {'1_Eights': '', '2_Eights': '', '3_Eights': '',
                    '4_Eights': '', '5_Eights': '', '6_Eights': '',
                    '7_Eights': '', '8_Eights': ''}
    model = UserMatch

    def get(self, request, *args, **kwargs):
        try:
            object_list = UserMatch.objects.filter(user=request.user, phase='Eights')
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

    @staticmethod
    def check_winners(user):
        counter = 0
        for key, value in EightsView.winners.items():
            if len(str(value)) > 2:
                counter += 1
        if counter == 8:
            EightsView.create_fourths(user)
            user.profile.eights_filled = True
            user.save()
        return

    @staticmethod
    def create_fourths(user):
        EightsView.create_match(user, '1_Fourths', 'Fourths', EightsView.winners['1_Eights'], EightsView.winners['2_Eights'], '2018-07-06')
        EightsView.create_match(user, '2_Fourths', 'Fourths', EightsView.winners['3_Eights'], EightsView.winners['4_Eights'], '2018-07-06')
        EightsView.create_match(user, '3_Fourths', 'Fourths', EightsView.winners['5_Eights'], EightsView.winners['6_Eights'], '2018-07-07')
        EightsView.create_match(user, '4_Fourths', 'Fourths', EightsView.winners['7_Eights'], EightsView.winners['8_Eights'], '2018-07-07')
        return

    @staticmethod
    def create_match(user, label, phase, team_one, team_two, date='2018-07-02'):
        new_match = UserMatch(user=user, label=label, phase=phase,
                            team_one=team_one, team_two=team_two, date=date)
        new_match.save()
        return

    @staticmethod
    def fill_winners(user):
        user_matches = UserMatch.objects.filter(user=user, gambled=True, phase='Eights')
        for match in user_matches:
            for key, value in EightsView.winners.items():
                if match.label == key:
                    EightsView.winners[key] = match.winner

        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        EightsView.fill_winners(user)
        GroupsView.score_matches(user, dict_gamble)
        EightsView.check_winners(user)
        return redirect('eights_phase')

class GroupsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/groups_phase.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    model = UserMatch

    def get(self, request, *args, **kwargs):
        groups = {}
        # if request.user.is_staff:
        #     return redirect('reypar_admin')
        # else:
        object_list = UserMatch.objects.filter(user=request.user, phase='Groups')

        for group in GroupsView.groups:
            x = filter(lambda match: match.group == group, object_list)
            # import pdb; pdb.set_trace()
            filter_list = list(filter(lambda match: match.group == group, object_list))
            groups[group] = filter_list
        return render(request, self.template_name, {'groups': groups, 'object_list': object_list} )


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

    @staticmethod
    def sort_groups(user):
        user_teams = UserTeam.objects.filter(user=user).order_by('group','-points','-goals_favor', 'goals_against')
        players = {}
        for group in GroupsView.groups:
            x = filter(lambda match: match.group == group, user_teams)
            # import pdb; pdb.set_trace()
            filter_list = list(filter(lambda match: match.group == group, user_teams))
            players[group] = filter_list[:2]
        GroupsView.create_eight(user, players)
        user.profile.groups_filled = True
        user.save()
        return

    @staticmethod
    def update_team(user, team, points, goals_favor, goals_against):
        team.points += int(points)
        team.goals_favor += int(goals_favor)
        team.goals_against += int(goals_against)
        team.save()
        return team.pk

    @staticmethod
    def check_phase(user, label, winner, loser):
        if "Eights" in label:
            EightsView.fill_winners(user)
        elif "Fourths" in label:
            FourthsView.fill_winners(user)
        elif "Semi" in label:
            SemiView.fill_winners(user)
            SemiView.fill_losers(user)
        elif "3y4" in label:
            TercerCuartoView.fill_winners(user)
            TercerCuartoView.fill_losers(user)
        elif "Finals" in label:
            TercerCuartoView.fill_winners(user)
            TercerCuartoView.fill_losers(user)
        else:
            print("etapa grupos, no hay orden")
        return

    @staticmethod
    def define_points(user, label, user_match):
        points_one = 0
        points_two = 0
        winner = ''
        loser = ''
        if int(user_match.team_one_score) + int(user_match.penals_team_one) == int(user_match.team_two_score) + int(user_match.penals_team_two):
            points_one = 1
            points_two = 1
            if "Groups" not in label:
                user_match.gambled = False
        elif int(user_match.team_one_score) + int(user_match.penals_team_one) > int(user_match.team_two_score) + int(user_match.penals_team_two):
            points_one = 3
            points_two = 0
            user_match.winner = user_match.team_one
            user_match.loser = user_match.team_two
        else:
            points_one = 0
            points_two = 3
            user_match.winner = user_match.team_two
            user_match.loser = user_match.team_one

        user_match.save()
        if "Groups" in label:
            GroupsView.update_team(user, user_match.team_one, points_one, user_match.team_one_score, user_match.team_two_score)
            GroupsView.update_team(user, user_match.team_two, points_two, user_match.team_two_score, user_match.team_one_score)
        else:
            GroupsView.check_phase(user, label, winner, loser)
        return user_match.pk

    @staticmethod
    def save_gamble(user, label, score_one, score_two, penals_one=0, penals_two=0):
        user_match = get_object_or_404(UserMatch, label=label, user=user)
        user_match.team_one_score = score_one
        user_match.team_two_score = score_two
        user_match.penals_team_one = penals_one
        user_match.penals_team_two = penals_two
        user_match.user = user
        user_match.gambled = True
        user_match.save()
        GroupsView.define_points(user, label, user_match)
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

            if score_one != '' and score_two != '':
                if "Groups" in label or score_one != score_two:
                    print('No hay Penales')
                    GroupsView.save_gamble(user, label, score_one, score_two)
                    score_one = ''
                    score_two = ''
                elif "Groups" not in label and score_one == score_two and penals_one != '' and penals_two != '':
                    print('Hay penales')
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
        return redirect('groups_phase')

class ReyparAdminView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/reypar_admin'

    def test_func(self):
        return test_settings(self.request.user)
