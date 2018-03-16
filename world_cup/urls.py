from django.contrib import  admin
from django.urls import path
from django.views.generic import TemplateView
from world_cup.views import (
GroupsView, SummaryView
)

urlpatterns = [
    path('groups_phase/', GroupsView.as_view(), name='groups_phase'),
    path('summary/', SummaryView.as_view(), name='summary'),
]
