"""Define the Report View."""

import constants
from models.tournament import Tournament


class ReportView:
    """View to show the reports."""

    def show_report_menu(self, tournament: Tournament):
        """Print the menu to chose a report. Return a choice."""
        print(constants.SEPARATOR)
        print(f"Rapport du tournoi {tournament.name}")
        print("Que souhaitez-vous afficher ?")
        print(f"Liste des joueurs par ordre alphabétique ({constants.SHOW_PLAYERS_ALPHABETIC_PROMPT})")
        print(f"Liste des joueurs par rang ({constants.SHOW_PLAYERS_RANK_PROMPT})")
        print(f"Liste des joueurs par score ({constants.SHOW_PLAYERS_SCORE_PROMPT})")
        print(f"Liste des tours ({constants.SHOW_ROUNDS_LIST_PROMPT})")
        print(f"Liste des matchs ({constants.SHOW_MATCHES_LIST_PROMPT})")
        report_choice = input()

        try:
            report_choice = int(report_choice)
        except ValueError:
            return report_choice
        report_choice = int(report_choice)

        return report_choice

    def show_players(self, sort_type: int, tournament: Tournament):
        """Show the players of the tournament by chosen sort type."""
        print(constants.SEPARATOR)
        if sort_type == constants.SORT_BY_NAME:
            tournament.sort_players_by_name()
            print("Liste des joueurs par ordre alphabétique : ")
        elif sort_type == constants.SORT_BY_RANK:
            tournament.sort_players_by_rank()
            print("Liste des joueurs par rang : ")
        elif sort_type == constants.SORT_BY_SCORE:
            tournament.sort_players_by_score()
            print("Résultats du tournoi (Liste des joueurs par score) : ")
        for player in tournament.players:
            print(player)

    def show_rounds(self, tournament: Tournament):
        """Show the rounds of the tournament."""
        print(constants.SEPARATOR)
        print(tournament)
        for round_ in tournament.rounds:
            print(f"{round_.name} du {round_.beginning_time} au {round_.ending_time}.")

    def show_matches(self, tournament: Tournament):
        """Show the results of every match of the tournament."""
        print(constants.SEPARATOR)
        print(tournament)
        for round_ in tournament.rounds:
            print(f"Résultats du {round_.name} :")
            for match in round_.matches:
                print(match)

    def show_report(self, report_choice, tournament: Tournament):
        """Show the selected tournament report."""
        if report_choice == constants.SHOW_PLAYERS_ALPHABETIC_PROMPT:
            self.show_players(constants.SORT_BY_NAME, tournament)
        if report_choice == constants.SHOW_PLAYERS_RANK_PROMPT:
            self.show_players(constants.SORT_BY_RANK, tournament)
        if report_choice == constants.SHOW_PLAYERS_SCORE_PROMPT:
            self.show_players(constants.SORT_BY_SCORE, tournament)
        if report_choice == constants.SHOW_ROUNDS_LIST_PROMPT:
            self.show_rounds(tournament)
        if report_choice == constants.SHOW_MATCHES_LIST_PROMPT:
            self.show_matches(tournament)
