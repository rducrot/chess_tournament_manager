"""Define the main controller."""

from random import choice, randrange
from typing import List

from .swisssystem import SwissSystem

from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match

from views.base import View

from constants import NUMBER_OF_PLAYERS, PLAYERS_LAST_NAMES, PLAYERS_FIRST_NAMES, PLAYERS_BIRTH_DATES, GENDERS


class Controller:
    """Main controller."""
    def __init__(self, view: View, tournament_system: SwissSystem, tournament: Tournament):
        self.view = view
        self.tournament_system = tournament_system
        self.tournament = tournament

    def get_players(self) -> List[Player]:
        """Add players to the tournament."""
        players = []
        while len(players) < NUMBER_OF_PLAYERS:
            new_player = Player(choice(PLAYERS_LAST_NAMES),
                                choice(PLAYERS_FIRST_NAMES),
                                choice(PLAYERS_BIRTH_DATES),
                                choice(GENDERS),
                                randrange(980, 1400))
            players.append(new_player)
            self.tournament.players_ids.append(new_player.id)
        return players

    def get_rounds(self):
        """Add rounds to the tournament."""
        round_number = 1
        while len(self.tournament.rounds) < self.tournament.number_of_rounds:
            self.tournament.rounds.append(Round(f"Round {round_number}"))
            round_number += 1

    def run(self):

        new_tournament = self.view.prompt_ask_new_tournament()
        if new_tournament:
            self.view.prompt_update_current_tournament()
        players = self.get_players()
        self.get_rounds()

        update_players_list = self.view.prompt_ask_update_players_list()
        if update_players_list:
            self.tournament.players = []
            while len(self.tournament.players) < NUMBER_OF_PLAYERS:
                new_player = self.view.prompt_add_a_player()
                self.tournament.players.append(new_player)

        for tournament_round in self.tournament.rounds:
            if tournament_round == 0:
                self.tournament_system.sort_players_by_rank(players)
            else:
                self.tournament_system.sort_players_by_score(players)
            matches = self.tournament_system.make_matches_players_list(players)
            self.view.show_matches_players_list(matches)
            for match in matches:
                new_match = self.view.prompt_enter_match_score(match)
                tournament_round.matches.append(new_match)
            print(tournament_round.matches)
