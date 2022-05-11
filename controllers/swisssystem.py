"""Define the Swiss System Tournament controller."""
from typing import List

from models.match import Match
from models.player import Player


class SwissSystem:

    def sort_players_by_rank(self, players: List[Player]):
        """Sort a list of players by player rank."""
        players.sort(key=lambda x: x.rank, reverse=True)

    def sort_players_by_score(self, players: List[Player]):
        """Sort a list of players by player score."""
        players.sort(key=lambda x: (x.score, x.rank), reverse=True)

    def make_matches_list_first_round(self, players: List[Player]) -> List[tuple]:
        """Define a list of matches for the first round."""
        matches = []
        half = len(players) // 2
        first_half_players = players[:half]
        second_half_players = players[half:]

        for first_player, second_player in zip(first_half_players, second_half_players):
            first_player.previous_opponent = second_player.get_id()
            second_player.previous_opponent = first_player.get_id()
            matches.append((first_player, second_player))

        return matches

    def make_matches_list(self, players: List[Player]) -> List[tuple]:
        """Define a list of matches.
        Switch to the next player if a player was the opponent on the previous round."""
        matches = []
        player_without_match_ids = []

        for player in players:
            player_without_match_ids.append(player.get_id())

        while len(player_without_match_ids) > 0:
            players_without_match = [player for player in players if player.get_id() in player_without_match_ids]
            iter_players = iter(players_without_match)
            for player in iter_players:
                first_player = player
                try:
                    second_player = next(iter_players)
                except StopIteration:
                    break
                if len(player_without_match_ids) > 1:
                    if first_player.previous_opponent == second_player.get_id():
                        second_player = next(iter_players)
                player_without_match_ids.remove(first_player.get_id())
                player_without_match_ids.remove(second_player.get_id())
                first_player.previous_opponent = second_player.get_id()
                second_player.previous_opponent = first_player.get_id()
                matches.append((first_player, second_player))
                break

        return matches

    def update_player_score(self, player, matches: List[Match]):
        """Update the total score of a player with the result of the match."""
        for match in matches:
            for result in match:
                if player == result.player:
                    player.score += result.score
