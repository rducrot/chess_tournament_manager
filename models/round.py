"""Define the rounds."""

from itertools import count
from typing import List
from .match import Match


class Round:
    """Round class.
     Contains a list of matches."""
    id_iter = count()

    def __init__(self, name):
        self.id = next(self.id_iter)
        self.name = name
        self.matches: List[Match] = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
