from django.contrib import  admin
from django.urls import path
from django.views.generic import TemplateView
from world_cup.views import (
GroupsView, EightsView, FourthsView,
SemiView, TercerCuartoView,
FinalsView, ReyparAdminView, SaveMatchView,
RankingView
)

urlpatterns = [
    path('fase_grupos/', GroupsView.as_view(), name='groups_phase'),
    path('fase_octavos/', EightsView.as_view(), name='eights_phase'),
    path('fase_cuartos/', FourthsView.as_view(), name='fourths_phase'),
    path('fase_semifinal/', SemiView.as_view(), name='semi_phase'),
    path('fase_tercer_cuarto/', TercerCuartoView.as_view(), name='third_fourth_phase'),
    path('fase_final/', FinalsView.as_view(), name='finals_phase'),
    path('reypar_admin/', ReyparAdminView.as_view(), name='reypar_admin'),
    path('guardar_partido/', SaveMatchView.as_view(), name='save_match'),
    path('ranking/', RankingView.as_view(), name='ranking')
]
