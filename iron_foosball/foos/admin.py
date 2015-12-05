from django.contrib import admin
from foos.models import Player, Tourney, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Tourney)
class TourneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'tourney', 'player1', 'player2', 'winner', 'round_num',
                    'game_num')