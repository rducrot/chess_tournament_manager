"""Define the Main View."""
from typing import List

import constants
from models.player import Player
from models.tournament import Tournament


class View:
    """Main view."""

    def initial_message(self):
        """Initial message."""
        print(constants.SEPARATOR)
        print(f"Bienvenue sur {constants.APP_NAME}.")

    def menu_message(self, tournament: Tournament):
        """Print the main menu. Return a menu choice."""
        print(constants.SEPARATOR)
        print("Que souhaitez-vous faire ?")
        print(f"Gérer les informations du tournoi. ({constants.MANAGE_TOURNAMENT_STATE})")
        print(f"Gérer la liste des joueurs. ({constants.MANAGE_PLAYERS_LIST_STATE})")
        print(f"Entrer les scores du tournoi en cours. ({constants.RUN_TOURNAMENT_STATE})")
        print(f"Charger les données d'un tournoi passé/en cours. ({constants.LOAD_REPORT_STATE})")
        if tournament and tournament.all_rounds_played():
            print(f"Voir les rapports ({constants.SHOW_REPORT_STATE})")

        print(f"Quitter l'application. ({constants.QUIT_STATE})")
        state = input('')
        if state == constants.QUIT_STATE:
            return state
        try:
            state = int(state)
        except ValueError:
            return constants.MENU_STATE
        state = int(state)
        if state in constants.BASIC_STATES:
            return state
        elif state == constants.SHOW_REPORT_STATE and tournament.all_rounds_played():
            return state
        else:
            return constants.MENU_STATE

    def no_tournament_message(self):
        """Message if no tournament found."""
        print("Pas de tournoi en cours. Veuillez entrer les informations du tournois : ")

    def prompt_ask_new_tournament(self, tournament: Tournament) -> bool:
        """Ask for a new tournament."""
        print(constants.SEPARATOR)
        print("Le tournoi actuel est le suivant : ")
        print(str(tournament))
        update_tournament = input(f"Souhaitez-vous initialiser un nouveau tournoi ? "
                                  f"({constants.UPDATE_TOURNAMENT_PROMPT}/N) ")
        if update_tournament != constants.UPDATE_TOURNAMENT_PROMPT:
            return False
        return True

    def prompt_update_current_tournament(self) -> Tournament:
        """Prompt to add a tournament."""
        print(constants.SEPARATOR)
        name = input("Nom du tournoi : ")
        place = input("Lieu : ")
        date = input("Date : ")
        while True:
            time_control_prompt = input("Mode de gestion du temps - (BL)ITZ, (BU)LLET ou (R)APIDE : ")
            if time_control_prompt == constants.TIME_CONTROL_BLITZ_PROMPT:
                time_control = constants.TIME_CONTROL_BLITZ
                break
            elif time_control_prompt == constants.TIME_CONTROL_BULLET_PROMPT:
                time_control = constants.TIME_CONTROL_BULLET
                break
            elif time_control_prompt == constants.TIME_CONTROL_RAPID_PROMPT:
                time_control = constants.TIME_CONTROL_RAPID
                break
        description = input("Description : ")
        while True:
            number_of_rounds = input(f"Nombre de tours (Par défaut : {constants.DEFAULT_NUMBER_OF_ROUNDS}) : ")
            if not number_of_rounds:
                number_of_rounds = constants.DEFAULT_NUMBER_OF_ROUNDS
                break
            try:
                number_of_rounds = int(number_of_rounds)
            except ValueError:
                continue
            number_of_rounds = int(number_of_rounds)
            if type(number_of_rounds) == int:
                break

        tournament = Tournament(name, place, date, time_control, description, number_of_rounds)
        print(tournament)
        return tournament

    def empty_players_list_message(self):
        """Message if there is no players."""
        print("Aucun joueur trouvé. Veuillez renseigner les informations des joueurs : ")

    def prompt_ask_update_players_list(self, players: List[Player]) -> bool:
        """Ask to update the current players list."""
        print(constants.SEPARATOR)
        print("Les joueurs du tournoi sont les suivants : ")
        for player in players:
            print(player)
        update_players_list = input("Souhaitez-vous mettre à jour la liste des joueurs ? "
                                    f"({constants.UPDATE_PLAYERS_LIST_PROMPT}/N) ")
        if update_players_list != constants.UPDATE_PLAYERS_LIST_PROMPT:
            return False
        return True

    def prompt_add_a_player(self) -> Player:
        """Prompt to add a player."""
        print(constants.SEPARATOR)
        last_name = input("Nom du joueur : ")
        first_name = input("Prénom du joueur : ")
        date_of_birth = input("Date de naissance : ")
        while True:
            gender_prompt = input(f"Genre : ({constants.GENDER_M_PROMPT}/{constants.GENDER_W_PROMPT})")
            if gender_prompt == constants.GENDER_M_PROMPT:
                gender = constants.GENDER_M
                break
            if gender_prompt == constants.GENDER_W_PROMPT:
                gender = constants.GENDER_W
                break
        while True:
            rank = input("Rang : ")
            try:
                rank = int(rank)
            except ValueError:
                continue
            rank = int(rank)
            if type(rank) == int:
                break

        new_player = Player(last_name, first_name, date_of_birth, gender, rank)
        return new_player

    def prompt_ask_save_report(self):
        """Prompt to save a report for the current tournament."""
        print(constants.SEPARATOR)
        save_report = input("Souhaitez-vous enregistrer un rapport de tournoi ? (O/N) ")
        if save_report != constants.SAVE_RESULTS_PROMPT:
            return False
        return True

    def saved_report_message(self, db_name):
        """Notify that the report has been saved."""
        print(f"Rapport enregistré dans {db_name}")

    def no_saved_report_message(self):
        """Notify that no saved report can be loaded."""
        print(constants.SEPARATOR)
        print("Aucun rapport trouvé.")
        print("Veuillez d'abord sauvegarder les scores du tournoi.")
