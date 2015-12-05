from django.conf.urls import url
from django.contrib import admin
from foos.views import TourneyDetail, ListTourneys

urlpatterns = [
    url(r'^setup/(?P<tourney_id>\d+)/$', 'foos.views.create_initial_games',
        name='setup'),
    url(r'^round2/(?P<player_id>\d+)/$', 'foos.views.choose_winner',
        name='round2'),
    url(r'^round3/(?P<player_id>\d+)/$', 'foos.views.final', name='round3'),
    url(r'^winner/(?P<player_id>\d+)/$', 'foos.views.winner', name='winner'),
    url(r'(?P<pk>\d+)/$', TourneyDetail.as_view(), name='tourney_detail'),
    url(r'^$', ListTourneys.as_view(), name='list_tourneys'),
]
