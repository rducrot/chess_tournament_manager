"""Define the main controller."""
from datetime import datetime

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
                 db: TinyDB,
                 report_db: TinyDB):
        self.view = view
        self.tournament_view = tournament_view
        self.tournament_controller = tournament_controller
        self.tournament = None
        self.db = db
        self.report_db = report_db

    def _load_tournament(self, db) -> bool:
        """Load the tournament from the database."""
        tournament_table = db.table(DB_TABLE_TOURNAMENT)
        try:
            serialized_tournament = tournament_table.all()[0]
        except IndexError:
            return False
        except AttributeError:
            return False

        tournament = Tournament(
            name=serialized_tournament[DB_TOURNAMENT_NAME],
            place=serialized_tournament[DB_TOURNAMENT_PLACE],
            date=serialized_tournament[DB_TOURNAMENT_DATE],
            time_control=serialized_tournament[DB_TOURNAMENT_TIME_CONTROL],
            description=serialized_tournament[DB_TOURNAMENT_DESCRIPTION],
            number_of_rounds=serialized_tournament[DB_TOURNAMENT_NUMBER_OF_ROUNDS],
            played_rounds=serialized_tournament[DB_TOURNAMENT_PLAYED_ROUNDS])

        if tournament.played_rounds == BEGINNING_PLAYED_ROUNDS_NUMBER:
            tournament.init_rounds()

        self.tournament = tournament

        return True

    def _load_players(self, db):
        """Load the players from the database."""
        players_table = db.table(DB_TABLE_PLAYERS)
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

    def _load_rounds(self, db):
        """Load the played rounds from the database."""
        rounds_table = db.table(DB_TABLE_ROUNDS)
        serialized_rounds = rounds_table.all()

        for serialized_round in serialized_rounds:
            tournament_round = Round(serialized_round[DB_ROUND_ID])
            tournament_round.set_beginning_time(serialized_round[DB_ROUND_BEGINNING_TIME])
            tournament_round.set_ending_time(serialized_round[DB_ROUND_ENDING_TIME])

            for serialized_match in serialized_round[DB_ROUND_MATCHES_LIST].values():
                first_player = self.tournament.get_player(serialized_match[DB_MATCH_FIRST_PLAYER_ID])
                second_player = self.tournament.get_player(serialized_match[DB_MATCH_SECOND_PLAYER_ID])
                match = Match(Result(first_player, serialized_match[DB_MATCH_FIRST_PLAYER_SCORE]),
                              Result(second_player, serialized_match[DB_MATCH_SECOND_PLAYER_SCORE]))
                tournament_round.matches.append(match)

            tournament_round.set_beginning_time(serialized_round[DB_ROUND_BEGINNING_TIME])
            tournament_round.set_ending_time(serialized_round[DB_ROUND_ENDING_TIME])

            self.tournament.rounds.append(tournament_round)

    def _calculate_players_scores(self):
        """Calculate the players' scores from the played matches."""
        for player in self.tournament.players:
            player.reset_score()
            for tournament_round in self.tournament.rounds:
                self.tournament_controller.update_player_score(player, tournament_round.matches)

    def load_played_tournament(self, db):
        """Load a tournament with its players, rounds and played matches from a database."""
        self._load_tournament(db)
        self._load_players(db)
        self._load_rounds(db)
        self._calculate_players_scores()
        self.tournament.sort_players_by_score()

    def manage_tournament_information(self):
        """Ask to initialize a new tournament or use the existing one."""
        if self.tournament is None:
            self.view.no_tournament_message()
            new_tournament = True
        else:
            new_tournament = self.view.prompt_ask_new_tournament(self.tournament)
        if new_tournament:
            self.tournament = self.view.prompt_update_current_tournament()
            self.tournament.save_basic_information(self.db)
        self.tournament.init_rounds()

    def manage_players_list(self):
        """Ask to initialize a new players list or use the existing one."""
        if self.tournament.players_list_is_empty():
            self.view.empty_players_list_message()
            update_players_list = True
        else:
            self.tournament.sort_players_by_rank()
            update_players_list = self.view.prompt_ask_update_players_list(self.tournament.players)
        if update_players_list:
            self.tournament.reset_players_list()
            while len(self.tournament.players) < NUMBER_OF_PLAYERS:
                new_player = self.view.prompt_add_a_player()
                self.tournament.players.append(new_player)
            self.tournament.save_players(self.db)

    def save_report(self, db):
        save_report = self.view.prompt_ask_save_report()
        if save_report:
            self.tournament.save(db)
            self.view.saved_report_message(REPORT_DB_NAME)

    def run_tournament(self):
        """Run the tournament.
        Ask to write the results in a report."""
        if self.tournament.played_rounds == BEGINNING_PLAYED_ROUNDS_NUMBER:
            self.tournament.reset_players_scores()

        for tournament_round in self.tournament.rounds:
            if tournament_round <= self.tournament.played_rounds:
                continue
            tournament_round.set_beginning_time(str(datetime.now()))
            self.tournament_controller.make_a_round(tournament_round,
                                                    self.tournament_view,
                                                    self.tournament)
            tournament_round.set_ending_time(str(datetime.now()))
            self.tournament.played_rounds += 1
            if not self.tournament.all_rounds_played():
                continue_next_round = self.tournament_view.prompt_continue_next_round()
                if continue_next_round:
                    continue
                else:
                    break

        self.tournament.sort_players_by_score()
        if self.tournament.all_rounds_played():
            self.view.show_players(SORT_BY_SCORE, self.tournament)

        self.save_report(self.report_db)

    def show_report(self):
        """Show the selected tournament report."""
        report_choice = self.view.show_report_message(self.tournament)
        if report_choice == SHOW_PLAYERS_ALPHABETIC_PROMPT:
            self.view.show_players(SORT_BY_NAME, self.tournament)
        if report_choice == SHOW_PLAYERS_RANK_PROMPT:
            self.view.show_players(SORT_BY_RANK, self.tournament)
        if report_choice == SHOW_PLAYERS_SCORE_PROMPT:
            self.view.show_players(SHOW_PLAYERS_SCORE_PROMPT, self.tournament)
        if report_choice == SHOW_ROUNDS_LIST_PROMPT:
            self.view.show_rounds(self.tournament)
        if report_choice == SHOW_MATCHES_LIST_PROMPT:
            self.view.show_matches(self.tournament)

    def run(self):
        state = MENU_STATE
        running = True

        self.view.initial_message()

        tournament_loaded = self._load_tournament(self.db)
        if tournament_loaded:
            self._load_players(self.db)

        while running:
            if state == MENU_STATE:
                state = self.view.menu_message(self.tournament)
                print(state)

            if state == MANAGE_TOURNAMENT_STATE:
                self.manage_tournament_information()
                state = MENU_STATE

            if state == MANAGE_PLAYERS_LIST_STATE:
                self.manage_players_list()
                state = MENU_STATE

            if state == RUN_TOURNAMENT_STATE:
                if self.tournament is None:
                    state = MANAGE_TOURNAMENT_STATE
                elif self.tournament.players_list_is_empty():
                    state = MANAGE_PLAYERS_LIST_STATE
                else:
                    self.run_tournament()
                    state = MENU_STATE

            if state == LOAD_REPORT_STATE:
                self.load_played_tournament(self.report_db)
                print(self.tournament)
                state = MENU_STATE

            if state == SHOW_REPORT_STATE:
                self.show_report()
                state = MENU_STATE

            if state == QUIT_STATE:
                running = False
