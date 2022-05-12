"""Base view."""
from typing import List

from constants import *
from models.player import Player
from models.tournament import Tournament


class View:

    def initial_message(self):
        """Initial message."""
        print(SEPARATOR)
        print(f"Bienvenue sur {APP_NAME}.")

    def prompt_ask_new_tournament(self, tournament: Tournament) -> bool:
        """Ask for a new tournament."""
        print(SEPARATOR)
        print("Le tournois actuel est le suivant : ")
        print(str(tournament))
        update_tournament = input("Souhaitez-vous initialiser un nouveau tournoi ? (O/N) ")
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
            if number_of_rounds is int:
                break
            if not number_of_rounds:
                number_of_rounds = DEFAULT_NUMBER_OF_ROUNDS
                break
        tournament = Tournament(name, place, date, time_control, description, number_of_rounds)
        print(tournament)
        return tournament

    def prompt_ask_update_players_list(self, players: List[Player]) -> bool:
        """Ask to update the current players list."""
        print(SEPARATOR)
        print("Les joueurs du tournois sont les suivants : ")
        for player in players:
            print(player)
        update_players_list = input("Souhaitez-vous mettre à jour la liste des joueurs ? (O/N) ")
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
            gender_prompt = input("Genre : (H/F)")
            if gender_prompt == GENDER_M_PROMPT:
                gender = GENDER_M
                break
            if gender_prompt == GENDER_W_PROMPT:
                gender = GENDER_W
                break
        while True:
            rank = input("Rang : ")
            if rank is int:
                break

        new_player = Player(last_name, first_name, date_of_birth, gender, rank)
        return new_player
