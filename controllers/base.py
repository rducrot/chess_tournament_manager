"""Define the main controller."""
from tinydb import TinyDB

from constants import *
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from views.base import View
from views.tournament import TournamentView
from .swisssystem import SwissSystemController


class Controller:
    """Main controller."""
    def __init__(self, view: View,
                 tournament_view: TournamentView,
                 tournament_controller: SwissSystemController,
                 db: TinyDB):
        self.view = view
        self.tournament_view = tournament_view
        self.tournament_controller = tournament_controller
        self.db = db

    def _get_tournament(self):
        """Get the tournament from the database."""
        tournament_table = self.db.table("tournament")
        serialized_tournament = tournament_table.all()[0]
        tournament = Tournament(
            name=serialized_tournament[DB_TOURNAMENT_NAME],
            place=serialized_tournament[DB_TOURNAMENT_PLACE],
            date=serialized_tournament[DB_TOURNAMENT_DATE],
            time_control=serialized_tournament[DB_TOURNAMENT_TIME_CONTROL],
            description=serialized_tournament[DB_TOURNAMENT_DESCRIPTION],
            number_of_rounds=serialized_tournament[DB_TOURNAMENT_NUMBER_OF_ROUNDS])
        self.tournament = tournament

    def _save_new_tournament(self):
        """Save a new tournament to the database."""
        tournament_table = self.db.table("tournament")
        tournament_table.truncate()
        serialized_tournament = {
            DB_TOURNAMENT_NAME: self.tournament.name,
            DB_TOURNAMENT_PLACE: self.tournament.place,
            DB_TOURNAMENT_DATE: self.tournament.date,
            DB_TOURNAMENT_TIME_CONTROL: self.tournament.time_control,
            DB_TOURNAMENT_DESCRIPTION: self.tournament.description,
            DB_TOURNAMENT_NUMBER_OF_ROUNDS: self.tournament.number_of_rounds
        }
        tournament_table.insert(serialized_tournament)

    def save_tournament_with_results(self):
        tournament_table = self.db.table("tournament")

    def _get_players(self):
        """Get the players from the database."""
        players_table = self.db.table("players")
        serialized_players = players_table.all()

        for serialized_player in serialized_players:
            player = Player(
                last_name=serialized_player[DB_PLAYER_LAST_NAME],
                first_name=serialized_player[DB_PLAYER_FIRST_NAME],
                date_of_birth=serialized_player[DB_PLAYER_DATE_OF_BIRTH],
                gender=serialized_player[DB_PLAYER_GENDER],
                rank=serialized_player[DB_PLAYER_RANK])
            self.tournament.players.append(player)

    def _save_players(self):
        """Save the players to the database."""
        players_table = self.db.table("players")
        players_table.truncate()
        for player in self.tournament.players:
            serialized_player = {
                DB_PLAYER_LAST_NAME: player.last_name,
                DB_PLAYER_FIRST_NAME: player.first_name,
                DB_PLAYER_DATE_OF_BIRTH: player.date_of_birth,
                DB_PLAYER_GENDER: player.gender,
                DB_PLAYER_RANK: player.rank
            }
            players_table.insert(serialized_player)

    def _init_rounds(self):
        """Add rounds to the tournament."""
        round_number = 1
        while len(self.tournament.rounds) < self.tournament.number_of_rounds:
            self.tournament.rounds.append(Round(f"Round {round_number}"))
            round_number += 1

    def initialize_new_tournament(self):
        """Ask to initialize a new tournament."""
        self._get_tournament()
        new_tournament = self.view.prompt_ask_new_tournament(self.tournament)
        if new_tournament:
            self.view.prompt_update_current_tournament()
            self._save_new_tournament()
        self._init_rounds()

    def initialize_new_players_list(self):
        """Ask to initialize a new players list."""
        self._get_players()
        self.tournament_controller.sort_players_by_rank(self.tournament.players)
        update_players_list = self.view.prompt_ask_update_players_list(self.tournament.players)
        if update_players_list:
            self.tournament.players = []
            while len(self.tournament.players) < NUMBER_OF_PLAYERS:
                new_player = self.view.prompt_add_a_player()
                self.tournament.players.append(new_player)
            self._save_players()

    def run(self):

        self.view.initial_message()
        self.initialize_new_tournament()
        self.initialize_new_players_list()

        for tournament_round in self.tournament.rounds:
            self.tournament_controller.make_a_round(tournament_round, self.tournament_view, self.tournament.players)

        self.tournament_controller.sort_players_by_score(self.tournament.players)
        self.tournament_view.show_tournament_results(self.tournament.players)
