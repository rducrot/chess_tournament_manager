"""Define the players."""
from itertools import count

from tinydb import TinyDB

from constants import *


class Player:
    """Player class."""
    id_iter = count()

    def __init__(self, last_name, first_name,
                 date_of_birth, gender, rank):
        self._id = next(self.id_iter)
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank
        self.score = 0
        self.previous_opponent = None

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rank} points, score : {self.score})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self._id == other

    def get_id(self):
        return self._id

    def set_id(self, player_id):
        self._id = player_id

    def reset_score(self):
        self.score = 0

    def save(self, db: TinyDB):
        """Save the player to the database."""
        players_table = db.table(DB_TABLE_PLAYERS)
        serialized_player = {
            DB_PLAYER_ID: self.get_id(),
            DB_PLAYER_LAST_NAME: self.last_name,
            DB_PLAYER_FIRST_NAME: self.first_name,
            DB_PLAYER_DATE_OF_BIRTH: self.date_of_birth,
            DB_PLAYER_GENDER: self.gender,
            DB_PLAYER_RANK: self.rank
        }
        players_table.insert(serialized_player)
