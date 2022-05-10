"""Define the Swiss System Tournament controller."""
from typing import List
from models.player import Player
from models.match import Match


class SwissSystem:

    def sort_players_by_rank(self, players: list):
        """Sort a list of players by player rank."""
        players.sort(reverse=True)

    def sort_players_by_score(self, players: list):
        """Sort a list of players by player score."""
        players.sort(key=lambda x: (x.rank, x.score), reverse=True)

    def make_matches_list_first_round(self, players: List[Player]) -> List[tuple]:
        """Define a list of matches for the first round."""
        matches = []
        half = len(players) // 2
        first_half_players = players[:half]
        second_half_players = players[half:]
        for first_player, second_player in zip(first_half_players, second_half_players):
            first_player.previous_opponent = second_player.id
            second_player.previous_opponent = first_player.id
            matches.append((first_player, second_player))
        return matches

    def make_matches_list(self, players: List[Player]) -> List[tuple]:
        """Define a list of matches."""
        matches = []
        iter_players = iter(players)
        for player in iter_players:
            first_player = player
            second_player = next(iter_players)
            first_player.previous_opponent = second_player.id
            second_player.previous_opponent = first_player.id
            matches.append((first_player, second_player))
        return matches

    def update_player_score(self, player, matches: List[Match]):
        """Update the total score of a player with the result of the match."""
        for match in matches:
            for result in match:
                if player.id == result.player.id:
                    player.score += result.score
