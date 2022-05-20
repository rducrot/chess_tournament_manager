"""Define the Report View."""

from constants import *
from models.tournament import Tournament


class ReportView:

    def show_report_menu(self, tournament: Tournament):
        """Print the menu to chose a report. Return a choice."""
        print(SEPARATOR)
        print(f"Rapport du tournoi {tournament.name}")
        print("Que souhaitez-vous afficher ?")
        print(f"Liste des joueurs par ordre alphabétique ({SHOW_PLAYERS_ALPHABETIC_PROMPT})")
        print(f"Liste des joueurs par rang ({SHOW_PLAYERS_RANK_PROMPT})")
        print(f"Liste des joueurs par score ({SHOW_PLAYERS_SCORE_PROMPT})")
        print(f"Liste des tours ({SHOW_ROUNDS_LIST_PROMPT})")
        print(f"Liste des matchs ({SHOW_MATCHES_LIST_PROMPT})")
        report_choice = input()

        try:
            report_choice = int(report_choice)
        except ValueError:
            return report_choice
        report_choice = int(report_choice)

        return report_choice

    def show_players(self, sort_type: int, tournament: Tournament):
        """Show the players of the tournament by chosen sort type."""
        print(SEPARATOR)
        if sort_type == SORT_BY_NAME:
            tournament.sort_players_by_name()
            print("Liste des joueurs par ordre alphabétique : ")
        elif sort_type == SORT_BY_RANK:
            tournament.sort_players_by_rank()
            print("Liste des joueurs par rang : ")
        elif sort_type == SORT_BY_SCORE:
            tournament.sort_players_by_score()
            print("Résultats du tournoi (Liste des joueurs par score) : ")
        for player in tournament.players:
            print(player)

    def show_rounds(self, tournament: Tournament):
        """Show the rounds of the tournament."""
        print(SEPARATOR)
        print(tournament)
        for tournament_round in tournament.rounds:
            print(f"{tournament_round.name} du {tournament_round.beginning_time} au {tournament_round.ending_time}.")

    def show_matches(self, tournament: Tournament):
        """Show the results of every match of the tournament."""
        print(SEPARATOR)
        print(tournament)
        for tournament_round in tournament.rounds:
            print(f"Résultats du {tournament_round.name} :")
            for match in tournament_round.matches:
                print(match)

    def show_report(self, report_choice, tournament: Tournament):
        """Show the selected tournament report."""
        if report_choice == SHOW_PLAYERS_ALPHABETIC_PROMPT:
            self.show_players(SORT_BY_NAME, tournament)
        if report_choice == SHOW_PLAYERS_RANK_PROMPT:
            self.show_players(SORT_BY_RANK, tournament)
        if report_choice == SHOW_PLAYERS_SCORE_PROMPT:
            self.show_players(SORT_BY_SCORE, tournament)
        if report_choice == SHOW_ROUNDS_LIST_PROMPT:
            self.show_rounds(tournament)
        if report_choice == SHOW_MATCHES_LIST_PROMPT:
            self.show_matches(tournament)
