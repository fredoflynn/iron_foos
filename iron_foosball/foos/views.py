import random
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from foos.forms import AddPlayerForm, TourneyForm
from foos.models import Tourney, Game, Player
from django.db.models import Q


class CreateTourney(CreateView):
    model = Tourney
    form_class = TourneyForm
    success_url = reverse_lazy('list_tourneys')
    template_name = 'foos/create_tourney.html'


    # def form_valid(self, form, *args, **kwargs):
    #     player_name = self.request.POST.get('player')
    #     if Player.objects.filter(name=player_name).count() == 0:
    #         player = Player.objects.create(name=player_name)
    #     else:
    #         player = Player.objects.get(name=player_name)
    #     form.instance.players.add(player)
    #     return super().form_valid(form)


class TourneyDetail(DetailView):
    model = Tourney
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['tourney'] = self.object.id
        tourney = self.object
        games = tourney.game_set.all().order_by('game_num')
        context['games'] = games
        return context

class ListTourneys(ListView):
    model = Tourney
    queryset = Tourney.objects.order_by('-created_at')

    def post(self, catch):
        if self.request.method =='POST':
            form = AddPlayerForm(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data['player']
                id = self.request.GET.get('num')
                tourney = Tourney.objects.get(pk=id)
                if Player.objects.filter(name=name).count() == 0:
                    new_player = Player.objects.create(name=name)
                    tourney.players.add(new_player)
                    tourney.save()
                else:
                    player = Player.objects.get(name=name)
                    tourney.players.add(player)
                    tourney.save()

                if tourney.players.count() == 8:
                    tourney.is_running = True
                    tourney.save()
                    self.create_initial_games(tourney)
                    return HttpResponseRedirect(reverse('tourney_detail',
                                            kwargs={'pk': tourney.id}))
            return HttpResponseRedirect(reverse('list_tourneys'))

    @staticmethod
    def create_initial_games(tourney):
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
                                            kwargs={'pk': tourney.id}))

class ListPlayers(ListView):
    model = Player
    paginate_by = 10

    # def get_queryset(self):
    #     players = Player.objects.all()
    #     return players


# def create_initial_games(request, tourney_id):
#     tourney = Tourney.objects.get(pk=tourney_id)
#     player_list = []
#     for player in tourney.players.all():
#         player_list.append(player)
#     random.shuffle(player_list)
#     if len(player_list) == 8 and tourney.game_set.count() == 0:
#         game_num = 1
#         while len(player_list) > 0:
#             Game.objects.create(tourney=tourney,
#                                 player1=player_list.pop(),
#                                 player2=player_list.pop(),
#                                 game_num=game_num,
#                                 round_num=1)
#             game_num += 1
#
#     return HttpResponseRedirect(reverse('tourney_detail',
#                                         kwargs={'pk': tourney_id}))


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
    tourney.is_running = False
    tourney.is_open = False
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