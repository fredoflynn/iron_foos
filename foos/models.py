from django.core.exceptions import ValidationError
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=25, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @property
    def last_played_on(self):
        if self.game_set.all():
            return self.game_set.order_by('-created_at')[0].created_at
        else:
            return None

    @property
    def total_games(self):
        return self.player1.count() + self.player2.count()

    @property
    def wins(self):
        return self.game_set.count()

    @property
    def losses(self):
        return self.total_games - self.wins

    @property
    def tourney_wins(self):
        return self.tourney_set.filter(winner=self).count()

    @property
    def winning_pct(self):
        if not self.total_games == 0:
            return round(self.wins / self.total_games, 2)
        else:
            return 0


class Tourney(models.Model):
    name = models.CharField(max_length=30)
    players = models.ManyToManyField(Player)
    is_open = models.NullBooleanField(null=True, default=True)
    is_running = models.NullBooleanField(null=True, default=False)
    winner = models.ForeignKey(Player, related_name='winner', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @property
    def spots_open(self):
        return 8 - self.players.count()


class Game(models.Model):
    tourney = models.ForeignKey(Tourney)
    player1 = models.ForeignKey(Player, related_name='player1', null=True, blank=True)
    player2 = models.ForeignKey(Player, related_name='player2', null=True, blank=True)
    winner = models.ForeignKey(Player, null=True, blank=True)
    round_num = models.IntegerField()
    game_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Tournament: {}, Game: {}".format(self.tourney.name, self.game_num)