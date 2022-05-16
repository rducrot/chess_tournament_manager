"""Define the main controller."""
from tinydb import TinyDB

from constants import *
from models.match import Match, Result
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
        self.tournament = None
        self.db = db

    def _get_tournament(self, db):
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

    def _save_tournament(self, db):
        """Save a tournament to the database."""
        tournament_table = db.table("tournament")
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

    def _get_players(self, db):
        """Get the players from the database."""
        players_table = db.table("players")
        serialized_players = players_table.all()

        for serialized_player in serialized_players:
            player = Player(
                last_name=serialized_player[DB_PLAYER_LAST_NAME],
                first_name=serialized_player[DB_PLAYER_FIRST_NAME],
                date_of_birth=serialized_player[DB_PLAYER_DATE_OF_BIRTH],
                gender=serialized_player[DB_PLAYER_GENDER],
                rank=serialized_player[DB_PLAYER_RANK])
            player.set_id(serialized_player[DB_PLAYER_ID])
            self.tournament.players.append(player)

    def _save_players(self, db):
        """Save the players to the database."""
        players_table = db.table("players")
        players_table.truncate()
        for player in self.tournament.players:
            serialized_player = {
                DB_PLAYER_ID: player.get_id(),
                DB_PLAYER_LAST_NAME: player.last_name,
                DB_PLAYER_FIRST_NAME: player.first_name,
                DB_PLAYER_DATE_OF_BIRTH: player.date_of_birth,
                DB_PLAYER_GENDER: player.gender,
                DB_PLAYER_RANK: player.rank
            }
            players_table.insert(serialized_player)

    def _init_rounds(self):
        """Initialize the rounds of the tournament using number_of_rounds."""
        round_number = 1
        while len(self.tournament.rounds) < self.tournament.number_of_rounds:
            self.tournament.rounds.append(Round(f"Round {round_number}"))
            round_number += 1

    def _save_rounds(self, db):
        """Save each match for each round to the database."""
        rounds_table = db.table("rounds")
        rounds_table.truncate()

        for tournament_round in self.tournament.rounds:
            serialized_round = {}
            match_id = 1
            for match in tournament_round.matches:
                serialized_match = {
                    match_id: {
                        DB_MATCH_FIRST_PLAYER_ID: match.result_first_player.player.get_id(),
                        DB_MATCH_FIRST_PLAYER_SCORE: match.result_first_player.score,
                        DB_MATCH_SECOND_PLAYER_ID: match.result_second_player.player.get_id(),
                        DB_MATCH_SECOND_PLAYER_SCORE: match.result_second_player.score,
                    }
                }
                serialized_round.update(serialized_match)
                match_id += 1

            rounds_table.insert(serialized_round)

    def _get_rounds(self, db):
        """Get the played rounds from the database."""
        rounds_table = db.table("rounds")
        serialized_rounds = rounds_table.all()

        round_number = 1
        for serialized_round in serialized_rounds:
            tournament_round = Round(f"Round {round_number}")
            for serialized_match_key, serialized_match in serialized_round.items():
                first_player = self.tournament.get_player(serialized_match[DB_MATCH_FIRST_PLAYER_ID])
                second_player = self.tournament.get_player(serialized_match[DB_MATCH_SECOND_PLAYER_ID])
                match = Match(Result(first_player, serialized_match[DB_MATCH_FIRST_PLAYER_SCORE]),
                              Result(second_player, serialized_match[DB_MATCH_SECOND_PLAYER_SCORE]))
                tournament_round.matches.append(match)
                round_number += 1

            self.tournament.rounds.append(tournament_round)

    def _get_players_scores(self):
        """Calculate the players' scores from the played matches."""
        for player in self.tournament.players:
            for tournament_round in self.tournament.rounds:
                self.tournament_controller.update_player_score(player, tournament_round.matches)

    def initialize_tournament(self):
        """Ask to initialize a new tournament or use the existing one."""
        new_tournament = self.view.prompt_ask_new_tournament(self.tournament)
        if new_tournament:
            self.tournament = self.view.prompt_update_current_tournament()
            self._save_tournament(self.db)
        self._init_rounds()

    def initialize_players_list(self):
        """Ask to initialize a new players list or use the existing one."""
        self.tournament_controller.sort_players_by_rank(self.tournament.players)
        update_players_list = self.view.prompt_ask_update_players_list(self.tournament.players)
        if update_players_list:
            self.tournament.players = []
            while len(self.tournament.players) < NUMBER_OF_PLAYERS:
                new_player = self.view.prompt_add_a_player()
                self.tournament.players.append(new_player)
            self._save_players(self.db)

    def get_played_tournament(self, db):
        """Get a tournament with its players, rounds and played matches from a database."""
        self._get_tournament(db)
        self._get_players(db)
        self._get_rounds(db)
        self._get_players_scores()
        self.tournament_controller.sort_players_by_score(self.tournament.players)

    def run(self):

        state = MENU_STATE
        self._get_tournament(self.db)
        self._get_players(self.db)
        self._init_rounds()

        self.view.initial_message()

        while True:
            if state == MENU_STATE:
                state = self.view.menu_message()
                print(state)

            if state == INIT_TOURNAMENT_STATE:
                self.initialize_tournament()
                self.initialize_players_list()
                state = MENU_STATE

            if state == TOURNAMENT_STATE:
                for tournament_round in self.tournament.rounds:
                    self.tournament_controller.make_a_round(tournament_round, self.tournament_view, self.tournament.players)
                self.tournament_controller.sort_players_by_score(self.tournament.players)
                self.tournament_view.show_tournament_results(self.tournament.players)
                state = MENU_STATE

            if state == SHOW_REPORT_STATE:
                result_db = TinyDB("results.json")
                self.get_played_tournament(result_db)
                self.tournament_view.show_tournament_results(self.tournament.players)
                state = MENU_STATE

            if state == QUIT_STATE:
                break
