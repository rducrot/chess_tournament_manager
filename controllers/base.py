"""Define the main controller."""

from random import choice, randrange

from constants import NUMBER_OF_PLAYERS, PLAYERS_LAST_NAMES, PLAYERS_FIRST_NAMES, PLAYERS_BIRTH_DATES, GENDERS, \
    FIRST_ROUND_ID
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from views.base import View
from views.tournament import TournamentView
from .swisssystem import SwissSystem


class Controller:
    """Main controller."""
    def __init__(self, view: View, tournament_view: TournamentView, tournament_system: SwissSystem, tournament: Tournament):
        self.view = view
        self.tournament_view = tournament_view
        self.tournament_system = tournament_system
        self.tournament = tournament

    def get_players(self):
        """Add players to the tournament."""
        while len(self.tournament.players) < NUMBER_OF_PLAYERS:
            new_player = Player(choice(PLAYERS_LAST_NAMES),
                                choice(PLAYERS_FIRST_NAMES),
                                choice(PLAYERS_BIRTH_DATES),
                                choice(GENDERS),
                                randrange(980, 1400))
            self.tournament.players.append(new_player)

    def get_rounds(self):
        """Add rounds to the tournament."""
        round_number = 1
        while len(self.tournament.rounds) < self.tournament.number_of_rounds:
            self.tournament.rounds.append(Round(f"Round {round_number}"))
            round_number += 1

    def initialize_new_tournament(self):
        """Ask to initialize a new tournament."""
        new_tournament = self.view.prompt_ask_new_tournament()
        if new_tournament:
            self.view.prompt_update_current_tournament()

    def initialize_new_players_list(self):
        """Ask to initialize a new players list."""
        update_players_list = self.view.prompt_ask_update_players_list()
        if update_players_list:
            self.tournament.players = []
            while len(self.tournament.players) < NUMBER_OF_PLAYERS:
                new_player = self.view.prompt_add_a_player()
                self.tournament.players.append(new_player)

    def run(self):

        self.initialize_new_tournament()
        self.get_players()
        self.get_rounds()
        self.initialize_new_players_list()

        for tournament_round in self.tournament.rounds:
            if tournament_round == FIRST_ROUND_ID:
                self.tournament_system.sort_players_by_rank(self.tournament.players)
                matches = self.tournament_system.make_matches_list_first_round(self.tournament.players)
            else:
                self.tournament_system.sort_players_by_score(self.tournament.players)
                matches = self.tournament_system.make_matches_list(self.tournament.players)
            self.tournament_view.show_matches_list(matches)
            for match in matches:
                new_match = self.tournament_view.prompt_enter_match_score(match)
                tournament_round.matches.append(new_match)
            for player in self.tournament.players:
                self.tournament_system.update_player_score(player, tournament_round.matches)
