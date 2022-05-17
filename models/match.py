"""Define the matches."""
from typing import NamedTuple

from constants import *
from models.player import Player


class Result(NamedTuple):
    """Result Model.
    Score of a player for a match."""
    player: Player
    score: float

    def __str__(self):
        if self.score == WIN_SCORE:
            return f"{self.player.last_name} {self.player.first_name} a gagné !"
        elif self.score == LOSE_SCORE:
            return f"{self.player.last_name} {self.player.first_name} a perdu !"
        elif self.score == DRAW_SCORE:
            return f"{self.player.last_name} {self.player.first_name} a fait match nul."

    def __repr__(self):
        return str(self)


class Match(NamedTuple):
    """Match model."""
    result_first_player: Result
    result_second_player: Result

    def __str__(self):
        return f"Premier joueur : {self.result_first_player}, Second joueur : {self.result_second_player}"

    def __repr__(self):
        return str(self)

    def serialize(self, match_id):
        """Return a serialized version of the match."""
        serialized_match = {
            match_id: {
                DB_MATCH_FIRST_PLAYER_ID: self.result_first_player.player.get_id(),
                DB_MATCH_FIRST_PLAYER_SCORE: self.result_first_player.score,
                DB_MATCH_SECOND_PLAYER_ID: self.result_second_player.player.get_id(),
                DB_MATCH_SECOND_PLAYER_SCORE: self.result_second_player.score,
            }
        }
        return serialized_match
