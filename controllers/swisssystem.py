"""Define the Swiss System Tournament controller."""
from typing import List
from models.player import Player


class SwissSystem:

    def sort_players_by_rank(self, players: list):
        """Sort a list of players by player rank."""
        players.sort(reverse=True)

    def sort_players_by_score(self, players: list):
        """Sort a list of players by player score."""
        players.sort(key=lambda x: (x.rank, x.score), reverse=True)

    def make_matches_list_first_round(self, players: List[Player]) -> List[tuple]:
        """Define a list of matches."""
        matches = []
        half = len(players) // 2
        first_half_players = players[:half]
        second_half_players = players[half:]
        for first_player, second_player in zip(first_half_players, second_half_players):
            matches.append((first_player, second_player))
        return matches

    def make_matches_list(self, players: List[Player]) -> List[tuple]:
        """Define a list of matches."""
        matches = []
        iter_players = iter(players)
        for player in iter_players:
            first_player = player
            second_player = next(iter_players)
            matches.append((first_player, second_player))
        return matches


    def update_player_score(self, player, matches):
        """Update the total score of a player with the result of the match."""
        for match in matches:
            #print("match : " + str(match) + str(type(match)))
            for result in match:
                #print("result : " + str(result) + str(type(result)))
                if player.id == result[0].id:
                    player.score += result[1]
