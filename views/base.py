"""Base view."""
from models.player import Player
from models.tournament import Tournament
from constants import DEFAULT_NUMBER_OF_ROUNDS, UPDATE_TOURNAMENT_PROMPT, UPDATE_PLAYERS_LIST_PROMPT


class View:

    def prompt_ask_new_tournament(self):
        """Ask for a new tournament"""
        update_tournament = input("Souhaitez-vous initialiser un nouveau tournoi ? (O/N)")
        if update_tournament != UPDATE_TOURNAMENT_PROMPT:
            return False
        return True

    def prompt_update_current_tournament(self) -> Tournament:
        """Prompt to add a tournament."""
        name = input("Nom du tournois : ")
        place = input("Lieu : ")
        date = input("Date : ")
        time_control = input("Mode de gestion du temps : ")
        description = input(" Description : ")
        number_of_rounds = input("Nombre de tours (Par défaut : 4) : ")
        if not number_of_rounds:
            number_of_rounds = DEFAULT_NUMBER_OF_ROUNDS

        tournament = Tournament(name, place, date, time_control, description, number_of_rounds)
        return tournament

    def prompt_ask_update_players_list(self):
        update_players_list = input("Souhaitez-vous mettre à jour la liste des joueurs ? (O/N)")
        if update_players_list != UPDATE_PLAYERS_LIST_PROMPT:
            return False
        return True

    def prompt_add_a_player(self) -> Player:
        """Prompt to add a player."""
        last_name = input("Nom du joueur : ")
        first_name = input("Prénom du joueur : ")
        date_of_birth = input("Date de naissance : ")
        gender = input("Genre : ")
        rank = input("Rang : ")

        new_player = Player(last_name, first_name, date_of_birth, gender, rank)
        return new_player
