from django.contrib import  admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from clients.views import (
RegisterView, home, OptionsView, register_user
)


urlpatterns = [
    path("", OptionsView.as_view(), name='options'),
    path('login/', auth_views.login, name='login'),
    path('home/', home, name='home'),
    path('register/', register_user, name='register_user')
]
