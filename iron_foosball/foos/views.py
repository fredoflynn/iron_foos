import random
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from foos.forms import AddPlayerForm
from foos.models import Tourney, Game, Player
from django.db.models import Q


class TourneyDetail(DetailView):
    model = Tourney

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['tourney'] = self.object.id
        tourney = self.object
        games = tourney.game_set.all().order_by('game_num')
        context['games'] = games
        return context


class ListTourneys(ListView):
    model = Tourney


def create_initial_games(request, tourney_id):
    tourney = Tourney.objects.get(pk=tourney_id)
    player_list = []
    for player in tourney.players.all():
        player_list.append(player)
    random.shuffle(player_list)
    if len(player_list) == 8 and tourney.game_set.count() == 0:
        game_num = 1
        while len(player_list) > 0:
            Game.objects.create(tourney=tourney,
                                player1=player_list.pop(),
                                player2=player_list.pop(),
                                game_num=game_num,
                                round_num=1)
            game_num += 1

    return HttpResponseRedirect(reverse('tourney_detail',
                                        kwargs={'pk': tourney_id}))


def choose_winner(request, player_id):
    tourney_id = request.session.get('tourney')
    tourney = Tourney.objects.get(pk=tourney_id)
    winner = Player.objects.get(pk=player_id)

    game5 = tourney.game_set.filter(game_num=5)
    if game5:
        game5 = game5[0]
    game6 = tourney.game_set.filter(game_num=6)
    if game6:
        game6 = game6[0]
    game = tourney.game_set.filter(Q(player1__id=player_id) |
                                   Q(player2__id=player_id))
    game = game[0]
    game.winner = winner
    game.save()
    if game.game_num == 1:
        if game5:
            game5.player1 = winner
            game5.save()
        else:
            Game.objects.create(tourney=tourney, player1=winner,
                                round_num=2, game_num=5)
    elif game.game_num == 2:
        if game5:
            game5.player2 = winner
            game5.save()
        else:
            Game.objects.create(tourney=tourney, player2=winner,
                                round_num=2, game_num=5)
    elif game.game_num == 3:
        if game6:
            game6.player1 = winner
            game6.save()
        else:
            Game.objects.create(tourney=tourney, player1=winner,
                                round_num=2, game_num=6)
    elif game.game_num == 4:
        if game6:
            game6.player2 = winner
            game6.save()
        else:
            Game.objects.create(tourney=tourney, player2=winner,
                                round_num=2, game_num=6)

    return HttpResponseRedirect(reverse('tourney_detail',
                                        kwargs={'pk': tourney_id}))


def final(request, player_id):
    tourney_id = request.session.get('tourney')
    tourney = Tourney.objects.get(pk=tourney_id)
    winner = Player.objects.get(pk=player_id)

    game = tourney.game_set.filter(Q(player1__id=player_id) |
                                   Q(player2__id=player_id)).filter(
                                    Q(game_num=5) | Q(game_num=6))
    game = game[0]
    game.winner = winner
    game.save()
    game7 = tourney.game_set.filter(game_num=7)
    if game7:
        game7 = game7[0]
    if game.game_num == 5:
        if game7:
            game7.player1 = winner
            game7.save()
        else:
            Game.objects.create(tourney=tourney, player1=winner,
                                round_num=3, game_num=7)
    elif game.game_num == 6:
        if game7:
            game7.player2 = winner
            game7.save()
        else:
            Game.objects.create(tourney=tourney, player2=winner,
                                round_num=3, game_num=7)

    return HttpResponseRedirect(reverse('tourney_detail',
                                        kwargs={'pk': tourney_id}))


def winner(request, player_id):
    tourney_id = request.session.get('tourney')
    tourney = Tourney.objects.get(pk=tourney_id)
    winner = Player.objects.get(pk=player_id)
    game7 = tourney.game_set.get(game_num=7)
    game7.winner = winner
    game7.save()
    tourney.winner = winner
    tourney.save()

    return HttpResponseRedirect(reverse('tourney_detail',
                                        kwargs={'pk': tourney_id}))
# def add_player(request):
#     if request.method == 'POST':
#         form = AddPlayerForm(request.POST)
#
#         if form.is_valid():
#             pass


    #     if request.method == 'POST':
    #     form = ChirpForm(request.POST)
    #
    #     if form.is_valid():
    #         chirp = form.save(commit=False)
    #         chirp.author = request.user
    #         chirp.save()
    #
    #         return HttpResponseRedirect(reverse('list_chirps'))
    # else:
    #     form = ChirpForm()
    #
    # return render(request, 'chirp/chirp_create.html', {'form': form})