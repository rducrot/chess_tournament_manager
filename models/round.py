"""Define the rounds."""

from typing import List
from .match import Match


class Round:
    """Round class.
     Contains a list of matches."""

    def __init__(self, name):
        self.name = name
        self.matches: List[Match] = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
