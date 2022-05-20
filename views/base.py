"""Define the Base View."""
from typing import List

from constants import *
from models.player import Player
from models.tournament import Tournament


class View:

    def initial_message(self):
        """Initial message."""
        print(SEPARATOR)
        print(f"Bienvenue sur {APP_NAME}.")

    def menu_message(self, tournament: Tournament):
        """Print the main menu. Return a menu choice."""
        print(SEPARATOR)
        print("Que souhaitez-vous faire ?")
        print(f"Gérer les informations du tournois. ({MANAGE_TOURNAMENT_STATE})")
        print(f"Gérer la liste des joueurs. ({MANAGE_PLAYERS_LIST_STATE})")
        print(f"Entrer les scores du tournois en cours. ({RUN_TOURNAMENT_STATE})")
        print(f"Charger les données d'un tournois passé/en cours. ({LOAD_REPORT_STATE})")
        if tournament and tournament.all_rounds_played():
            print(f"Voir les rapports ({SHOW_REPORT_STATE})")

        print(f"Quitter l'application. ({QUIT_STATE})")
        state = input('')
        if state == QUIT_STATE:
            return state
        try:
            state = int(state)
        except ValueError:
            return MENU_STATE
        state = int(state)
        if state in BASIC_STATES:
            return state
        elif state == SHOW_REPORT_STATE and tournament.all_rounds_played():
            return state
        else:
            return MENU_STATE

    def no_tournament_message(self):
        """Message if no tournament found."""
        print("Pas de tournois en cours. Veuillez entrer les informations du tournois : ")

    def prompt_ask_new_tournament(self, tournament: Tournament) -> bool:
        """Ask for a new tournament."""
        print(SEPARATOR)
        print("Le tournois actuel est le suivant : ")
        print(str(tournament))
        update_tournament = input(f"Souhaitez-vous initialiser un nouveau tournoi ? ({UPDATE_TOURNAMENT_PROMPT}/N) ")
        if update_tournament != UPDATE_TOURNAMENT_PROMPT:
            return False
        return True

    def prompt_update_current_tournament(self) -> Tournament:
        """Prompt to add a tournament."""
        print(SEPARATOR)
        name = input("Nom du tournois : ")
        place = input("Lieu : ")
        date = input("Date : ")
        while True:
            time_control_prompt = input("Mode de gestion du temps - (BL)ITZ, (BU)LLET ou (R)APIDE : ")
            if time_control_prompt == TIME_CONTROL_BLITZ_PROMPT:
                time_control = TIME_CONTROL_BLITZ
                break
            elif time_control_prompt == TIME_CONTROL_BULLET_PROMPT:
                time_control = TIME_CONTROL_BULLET
                break
            elif time_control_prompt == TIME_CONTROL_RAPID_PROMPT:
                time_control = TIME_CONTROL_RAPID
                break
        description = input("Description : ")
        while True:
            number_of_rounds = input(f"Nombre de tours (Par défaut : {DEFAULT_NUMBER_OF_ROUNDS}) : ")
            if not number_of_rounds:
                number_of_rounds = DEFAULT_NUMBER_OF_ROUNDS
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
        print(SEPARATOR)
        print("Les joueurs du tournois sont les suivants : ")
        for player in players:
            print(player)
        update_players_list = input("Souhaitez-vous mettre à jour la liste des joueurs ? "
                                    f"({UPDATE_PLAYERS_LIST_PROMPT}/N) ")
        if update_players_list != UPDATE_PLAYERS_LIST_PROMPT:
            return False
        return True

    def prompt_add_a_player(self) -> Player:
        """Prompt to add a player."""
        print(SEPARATOR)
        last_name = input("Nom du joueur : ")
        first_name = input("Prénom du joueur : ")
        date_of_birth = input("Date de naissance : ")
        while True:
            gender_prompt = input(f"Genre : ({GENDER_M_PROMPT}/{GENDER_W_PROMPT})")
            if gender_prompt == GENDER_M_PROMPT:
                gender = GENDER_M
                break
            if gender_prompt == GENDER_W_PROMPT:
                gender = GENDER_W
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
        print(SEPARATOR)
        save_report = input("Souhaitez-vous enregistrer un rapport de tournois ? (O/N) ")
        if save_report != SAVE_RESULTS_PROMPT:
            return False
        return True

    def saved_report_message(self, db_name):
        """Notify that the report has been saved."""
        print(f"Rapport enregistré dans {db_name}")

    def no_saved_report_message(self):
        """Notify that no saved report can be loaded."""
        print(SEPARATOR)
        print("Aucun rapport trouvé.")
        print("Veuillez d'abord sauvegarder les scores du tournois.")
