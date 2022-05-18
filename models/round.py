"""Define the rounds."""
from itertools import count
from typing import List

from tinydb import TinyDB

from constants import *
from .match import Match


class Round:
    """Round class.
     Contains a list of matches."""
    id_iter = count()

    def __init__(self, round_number: int):
        self._id = next(self.id_iter)
        self.name = f"Round {round_number}"
        self.matches: List[Match] = []
        self.beginning_time = None
        self.ending_time = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self._id == other

    def set_beginning_time(self, time):
        self.beginning_time = time

    def set_ending_time(self, time):
        self.ending_time = time

    def save(self, db: TinyDB):
        """Save the round to the database."""
        rounds_table = db.table(DB_TABLE_ROUNDS)
        serialized_round = {DB_ROUND_BEGINNING_TIME: self.beginning_time,
                            DB_ROUND_ENDING_TIME: self.ending_time,
                            DB_ROUND_MATCHES_LIST: {}}
        match_id = 1
        for match in self.matches:
            serialized_match = match.serialize(match_id)
            serialized_round[DB_ROUND_MATCHES_LIST].update(serialized_match)
            match_id += 1
        rounds_table.insert(serialized_round)
