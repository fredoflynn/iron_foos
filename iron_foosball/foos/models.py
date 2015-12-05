from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=25, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tourney(models.Model):
    name = models.CharField(max_length=30)
    players = models.ManyToManyField(Player)
    winner = models.ForeignKey(Player, related_name='winner', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.name


class Game(models.Model):
    tourney = models.ForeignKey(Tourney)
    player1 = models.ForeignKey(Player, related_name='player1', null=True, blank=True)
    player2 = models.ForeignKey(Player, related_name='player2', null=True, blank=True)
    winner = models.ForeignKey(Player, null=True, blank=True)
    round_num = models.IntegerField()
    game_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.game_num)