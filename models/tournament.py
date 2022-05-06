"""Define the Tournament."""

from typing import List
from player import Player
from round import Round

TIME_CONTROL_BULLET = 0
TIME_CONTROL_BLITZ = 1
TIME_CONTROL_RAPID = 2
DEFAULT_NUMBER_OF_ROUNDS = 4


class Tournament:
    """Tournament class."""

    def __init__(self, name, place, date, time_control,
                 description, number_of_rounds=DEFAULT_NUMBER_OF_ROUNDS):
        self.name = name
        self.place = place
        self.date = date
        self.time_control = time_control
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.rounds: List[Round] = []
        self.players: List[Player] = []

    def __str__(self):
        return f"Tournois {self.name} du {self.date} à {self.place}"

    def __repr__(self):
        return str(self)