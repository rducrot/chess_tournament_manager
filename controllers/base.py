"""Define the Main Controller."""
from datetime import datetime

from tinydb import TinyDB

import constants
from views.base import View
from views.report import ReportView
from views.tournament import TournamentView
from .dataload import DataLoadController
from .swisssystem import SwissSystemController


class Controller:
    """Main controller."""

    def __init__(self, view: View,
                 tournament_view: TournamentView,
                 report_view: ReportView,
                 data_load_controller: DataLoadController,
                 tournament_controller: SwissSystemController,
                 db: TinyDB,
                 report_db: TinyDB):
        self.view = view
        self.tournament_view = tournament_view
        self.report_view = report_view
        self.data_load_controller = data_load_controller
        self.tournament_controller = tournament_controller
        self.tournament = None
        self.db = db
        self.report_db = report_db

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
            while len(self.tournament.players) < constants.NUMBER_OF_PLAYERS:
                new_player = self.view.prompt_add_a_player()
                self.tournament.players.append(new_player)
            self.tournament.save_players(self.db)

    def run_tournament(self):
        """Run the tournament."""
        if self.tournament.played_rounds == constants.BEGINNING_PLAYED_ROUNDS_NUMBER:
            self.tournament.reset_players_scores()

        for round_ in self.tournament.rounds:
            if round_ <= self.tournament.played_rounds:
                continue
            round_.set_beginning_time(str(datetime.now()))
            self.tournament_controller.make_a_round(round_,
                                                    self.tournament_view,
                                                    self.tournament)
            round_.set_ending_time(str(datetime.now()))
            self.tournament.played_rounds += 1

            if not self.tournament.all_rounds_played():
                continue_next_round = self.tournament_view.prompt_continue_next_round()
                if continue_next_round:
                    continue
                else:
                    break

        self.tournament.sort_players_by_score()
        if self.tournament.all_rounds_played():
            self.report_view.show_players(constants.SORT_BY_SCORE, self.tournament)

    def save_report(self, db):
        """Ask to save the results of the tournament in a report.
        Save it to the report database."""
        save_report = self.view.prompt_ask_save_report()
        if save_report:
            self.tournament.save(db)
            self.view.saved_report_message(constants.REPORT_DB_NAME)

    def run(self):
        """Run the application."""
        state = constants.MENU_STATE
        running = True

        self.view.initial_message()

        self.tournament = self.data_load_controller.load_tournament(self.db)
        if self.tournament is not None:
            self.tournament.players = self.data_load_controller.load_players(self.db)

        while running:
            if state == constants.MENU_STATE:
                state = self.view.menu_message(self.tournament)
                print(state)

            if state == constants.MANAGE_TOURNAMENT_STATE:
                self.manage_tournament_information()
                state = constants.MENU_STATE

            if state == constants.MANAGE_PLAYERS_LIST_STATE:
                if self.tournament is None:
                    state = constants.MANAGE_TOURNAMENT_STATE
                else:
                    self.manage_players_list()
                    state = constants.MENU_STATE

            if state == constants.RUN_TOURNAMENT_STATE:
                if self.tournament is None:
                    state = constants.MANAGE_TOURNAMENT_STATE
                elif self.tournament.players_list_is_empty():
                    state = constants.MANAGE_PLAYERS_LIST_STATE
                else:
                    self.run_tournament()
                    self.save_report(self.report_db)
                    state = constants.MENU_STATE

            if state == constants.LOAD_REPORT_STATE:
                self.tournament = self.data_load_controller.load_played_tournament(self.report_db)
                if self.tournament is not None:
                    print(self.tournament)
                else:
                    self.view.no_saved_report_message()
                    # Reload the tournament from db if there is no report_db
                    self.tournament = self.data_load_controller.load_tournament(self.db)
                    if self.tournament is not None:
                        self.tournament.players = self.data_load_controller.load_players(self.db)
                state = constants.MENU_STATE

            if state == constants.SHOW_REPORT_STATE:
                report_choice = self.report_view.show_report_menu(self.tournament)
                self.report_view.show_report(report_choice, self.tournament)
                state = constants.MENU_STATE

            if state == constants.QUIT_STATE:
                running = False
