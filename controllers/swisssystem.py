"""Define the Swiss System Tournament controller."""
from typing import List


class SwissSystem:

    def sort_players_by_rank(self, players: list):
        """Sort a list of players by player rank."""
        players.sort(reverse=True)

    def sort_players_by_score(self, players: list):
        """Sort a list of players by player score."""
        players.sort(key=lambda x: (x.score, x.rank), reverse=True)

    def make_matches_players_list(self, players: list) -> List[tuple]:
        """Define a list of matches."""
        matches = []
        half = len(players) // 2
        first_half_players = players[:half]
        second_half_players = players[half:]
        for first_player, second_player in zip(first_half_players, second_half_players):
            matches.append((first_player, second_player))
        return matches

"""    def update_player_score(self, player, matches):
        Update the total score of a player with the result of the match.
        for match in matches:
            for result in match:
                if player.name in result:
                    player.score += result[1]"""
