"""Base view."""

from models.player import Player
from models.tournament import Tournament
from constants import DEFAULT_NUMBER_OF_ROUNDS


class View:

    def prompt_add_a_player(self) -> Player:
        """Prompt to add a player."""
        last_name = input("Nom du joueur : ")
        first_name = input("Prénom du joueur : ")
        date_of_birth = input("Date de naissance : ")
        gender = input("Genre : ")
        rank = input("Rang : ")

        new_player = Player(last_name, first_name, date_of_birth, gender, rank)
        return new_player

    def prompt_add_a_tournament(self):
        """Prompt to add a tournament."""
        name = input("Nom du tournois : ")
        place = None
        date = None
        time_control = None
        description = None
        number_of_rounds = input("Nombre de tours (Par défaut : 4) : ")
        if not number_of_rounds:
            number_of_rounds = DEFAULT_NUMBER_OF_ROUNDS

        new_tournament = Tournament(name, place, date, time_control, description, number_of_rounds)
        return new_tournament
