from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from world_cup.models import RealMatch, UserMatch, Team, UserTeam
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponse
from django.contrib import messages
import json
from django.db.models import Q
from clients.models import Profile

class TermsView(TemplateView):
    template_name = 'world_cup/terms.html'

class RankingView(TemplateView):
    template_name = 'world_cup/ranking.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        try:
            object_list =  Profile.objects.filter(Q(active=True) & ~Q(user__username='polla_admin')).order_by('-total_points')[:100]
        except:
            raise Http404
        return render(request, self.template_name, {'object_list': object_list} )

class SaveMatchView(LoginRequiredMixin, TemplateView):
    model = UserMatch

    @staticmethod
    def save_team_stats(team, points, goals_favor, goals_against):
        team.points = points
        team.goals_favor = goals_favor
        team.goals_against = goals_against
        team.save()
        return

    @staticmethod
    def set_team_stats(team, user):
        points = 0
        goals_favor = 0
        goals_against = 0
        matches = UserMatch.objects.filter(Q(team_one=team, gambled=True, user=user) | Q(team_two=team, gambled=True, user=user))
        for match in matches:
            if(match.winner == None):
                points += 1
            elif(match.winner == team):
                points += 3
            if (match.team_one == team):
                goals_favor += match.team_one_score
                goals_against += match.team_two_score
            else:
                goals_favor += match.team_two_score
                goals_against += match.team_one_score
            match.save()
        SaveMatchView.save_team_stats(team, points, goals_favor, goals_against)
        return

    @staticmethod
    def save_match(label, user, dict):
        user_match = get_object_or_404(UserMatch, label=label, user=user)
        user_match.team_one_score = dict['team_1']
        user_match.team_two_score = dict['team_2']
        user_match.gambled = True
        if dict['team_1'] == dict['team_2']:
            user_match.penals_team_one = dict['penals_1']
            user_match.penals_team_two = dict['penals_2']
            if dict['penals_1'] > dict['penals_2']:
                user_match.winner = user_match.team_one
                user_match.loser = user_match.team_two
            elif dict['penals_2'] > dict['penals_1']:
                user_match.winner = user_match.team_two
                user_match.loser = user_match.team_one
            else:
                user_match.winner = None
                user_match.loser = None
        elif dict['team_1'] > dict['team_2']:
            user_match.penals_team_one = 0
            user_match.penals_team_two = 0
            user_match.winner = user_match.team_one
            user_match.loser = user_match.team_two
        else:
            user_match.penals_team_one = 0
            user_match.penals_team_two = 0
            user_match.winner = user_match.team_two
            user_match.loser = user_match.team_one
        user_match.user = user
        user_match.save()
        SaveMatchView.set_team_stats(user_match.team_one, user)
        SaveMatchView.set_team_stats(user_match.team_two, user)
        return

    def post(self, request, *args, **kwargs):
        dict = json.loads(request.body.decode('utf-8'))
        label = dict['match_label']
        user = request.user
        SaveMatchView.save_match(label, user, dict)
        response = {'status': 0}
        return HttpResponse(json.dumps(response), content_type='application/json')

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
    def check_winners(request, user):
        FinalsView.fill_winners(user)
        FinalsView.fill_losers(user)
        counter = 0
        warnings = []
        for key, value in FinalsView.winners.items():
            if value != None and value != '':
                counter += 1
            else:
                warnings += key[0]

        if len(warnings) >= 1:
            messages.warning(request, 'Partido(s) ' + ', '.join(warnings) + ' no tiene(n) un ganador 😧')
        if len(warnings) == 0 and counter == 1:
            user.profile.final_filled = True
            user.save()
        return

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
        FinalsView.fill_winners(user)
        FinalsView.fill_losers(user)
        GroupsView.score_matches(request, user, dict_gamble)
        FinalsView.check_winners(request, user)
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
    def check_winners(request, user):
        TercerCuartoView.fill_winners(user)
        TercerCuartoView.fill_losers(user)
        counter = 0
        warnings = []
        for key, value in TercerCuartoView.winners.items():
            if value != None and value != '':
                counter += 1
            else:
                warnings += key[0]

        if len(warnings) >= 1:
            messages.warning(request, 'Partido(s) ' + ', '.join(warnings) + ' no tiene(n) un ganador 😧')
        if len(warnings) == 0 and counter == 1:
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
        TercerCuartoView.fill_winners(user)
        TercerCuartoView.fill_losers(user)
        GroupsView.score_matches(request, user, dict_gamble)
        TercerCuartoView.check_winners(request, user)
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
    def check_winners(request, user):
        SemiView.fill_winners(user)
        SemiView.fill_losers(user)
        counter = 0
        warnings = []
        for key, value in SemiView.winners.items():
            if value != None and value != '':
                counter += 1
            else:
                warnings += key[0]
        if len(warnings) >= 1:
            messages.warning(request, 'Partido(s) ' + ', '.join(warnings) + ' no tiene(n) un ganador 😧')
        if len(warnings) == 0 and counter == 2:
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
        GroupsView.score_matches(request, user, dict_gamble)
        SemiView.check_winners(request, user)
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
    def check_winners(request, user):
        FourthsView.fill_winners(user)
        counter = 0
        warnings = []
        for key, value in FourthsView.winners.items():
            if value != None and value != '':
                counter += 1
            else:
                warnings += key[0]

        if len(warnings) >= 1:
            messages.warning(request, 'Partido(s) ' + ', '.join(warnings) + ' no tiene(n) un ganador 😧')
        if len(warnings) == 0 and counter == 4:
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
        GroupsView.score_matches(request, user, dict_gamble)
        FourthsView.check_winners(request, user)
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
    def check_winners(request, user):
        EightsView.fill_winners(user)
        counter = 0
        warnings = []
        for key, value in EightsView.winners.items():
            if value != None and value != '':
                counter += 1
            else:
                warnings += key[0]
        if len(warnings) >= 1:
            messages.warning(request, 'Partido(s) ' + ', '.join(warnings) + ' no tiene(n) un ganador 😧')
        elif len(warnings) == 0 and counter == 8:
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
        GroupsView.score_matches(request, user, dict_gamble)
        EightsView.check_winners(request, user)
        return redirect('eights_phase')

class GroupsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/groups_phase.html'
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    model = UserMatch

    def get(self, request, *args, **kwargs):
        groups = {}
        object_list = UserMatch.objects.filter(user=request.user, phase='Groups').order_by('group')

        for group in GroupsView.groups:
            x = filter(lambda match: match.group == group, object_list)
            # import pdb; pdb.set_trace()
            filter_list = list(filter(lambda match: match.group == group, object_list))
            groups[group] = filter_list
        return render(request, self.template_name, {'groups': sorted(groups.items()), 'object_list': object_list} )


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
            filter_list = list(filter(lambda match: match.group == group, user_teams))
            players[group] = filter_list[:2]
        user.profile.groups_filled = True
        user.save()
        GroupsView.create_eight(user, players)
        return

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
    def define_winner(user, label, user_match):
        points_one = 0
        points_two = 0
        winner = ''
        loser = ''
        if int(user_match.team_one_score) != int(user_match.team_two_score):
            if int(user_match.penals_team_one) > 0 or int(user_match.penals_team_two) > 0:
                user_match.winner = None
                user_match.loser = None
            elif int(user_match.team_one_score) > int(user_match.team_two_score):
                user_match.winner = user_match.team_one
                user_match.loser = user_match.team_two
            elif int(user_match.team_one_score) < int(user_match.team_two_score):
                user_match.winner = user_match.team_two
                user_match.loser = user_match.team_one

        elif int(user_match.team_one_score) == int(user_match.team_two_score):
            if int(user_match.penals_team_one) == int(user_match.penals_team_two):
                user_match.winner = None
                user_match.loser = None
            elif int(user_match.penals_team_one) > int(user_match.penals_team_two):
                user_match.winner = user_match.team_one
                user_match.loser = user_match.team_two
            elif int(user_match.penals_team_one) < int(user_match.penals_team_two):
                user_match.winner = user_match.team_two
                user_match.loser = user_match.team_one

        user_match.save()

        if "Groups" in label:
            SaveMatchView.set_team_stats(user_match.team_one, user)
            SaveMatchView.set_team_stats(user_match.team_two, user)
        else:
            GroupsView.check_phase(user, label, winner, loser)
        return user_match.pk

    @staticmethod
    def save_gamble(user, label, score_one, score_two, penals_one, penals_two):
        user_match = get_object_or_404(UserMatch, label=label, user=user)
        user_match.team_one_score = score_one
        user_match.team_two_score = score_two
        user_match.penals_team_one = penals_one
        user_match.penals_team_two = penals_two
        user_match.user = user
        user_match.gambled = True
        user_match.save()
        GroupsView.define_winner(user, label, user_match)
        return user_match.pk

    @staticmethod
    def score_matches(request, user, dict_gamble):
        label = ''
        score_one = ''
        score_two = ''
        penals_one = ''
        penals_two = ''
        warnings = []
        count = 0

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

            if score_one != '' and score_two != '' and penals_one != '' and penals_two != '':
                if "Groups" in label:
                    GroupsView.save_gamble(user, label, score_one, score_two, 0, 0)
                else:
                    GroupsView.save_gamble(user, label, score_one, score_two, penals_one, penals_two)
                    if score_one != score_two and (int(penals_one) > 0 or int(penals_two)) > 0:
                        warnings += label[0]
                        count += 1
                score_one = ''
                score_two = ''
                penals_one = ''
                penals_two = ''
        if count > 0:
            messages.warning(request, 'Partido(s) ' + ', '.join(warnings) + ' no necesitan penalties 🙊')
        return count

    @staticmethod
    def save_or_not(request, user, dict_counter):
        ok = True
        for key, value in dict_counter.items():
            if value > 4:
                messages.warning(request, 'En la FIFA no dejan hacer tantos empates, revisa el grupo ' + key + ' 😯')
                ok = False
                break
        if ok == True:
            GroupsView.sort_groups(user)
        return

    @staticmethod
    def check_winners(request, user):
        user_match = UserMatch.objects.filter(phase='Groups', user=user)
        dict_counter = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0,
                         'F': 0, 'G': 0, 'H': 0}
        for match in user_match:
            if match.winner == None:
                dict_counter[match.group] += 1
        GroupsView.save_or_not(request, user, dict_counter)
        return

    def post(self, request, *args, **kwargs):
        dict_gamble = dict(request.POST.items())
        dict_gamble.pop('csrfmiddlewaretoken', None)
        user = request.user
        ok = GroupsView.score_matches(request, user, dict_gamble)
        if ok == 0:
            GroupsView.sort_groups(user)
            # GroupsView.check_winners(request, user)
        return redirect('groups_phase')

class ReyparAdminView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'world_cup/reypar_admin'

    def test_func(self):
        return test_settings(self.request.user)
