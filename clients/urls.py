from django.contrib import  admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from clients.views import (
RegisterView, home, OptionsView, register_user
# , ClientAutocomplete
)


urlpatterns = [
    path("", OptionsView.as_view(), name='options'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'options'}, name='logout'),
    path('home/', home, name='home'),
    path('register/', register_user, name='register_user'),
    # path(
    #     'client-autocomplete/',
    #     ClientAutocomplete.as_view(),
    #     name='client-autocomplete'
    # ),
    ##url('', include('django.contrib.auth.urls')),
    path('password_reset/', auth_views.password_reset, { 'template_name': 'registration/reset_form.html'}, name='password_reset'),
    path('password_reset/done/',auth_views.password_reset_done,
        {
            'template_name': 'registration/reset_done.html',
        }, name = 'password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'registration/reset_confirm.html',
        },
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {
            'template_name': 'registration/reset_complete.html',
        },
        name='password_reset_complete'),
]
