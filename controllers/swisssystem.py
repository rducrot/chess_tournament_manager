"""Define the Swiss System Tournament controller."""
from typing import List

from constants import FIRST_ROUND_ID
from models.match import Match
from models.player import Player
from models.round import Round
from views.tournament import TournamentView


class SwissSystemController:

    def sort_players_by_rank(self, players: List[Player]):
        """Sort a list of players by player rank."""
        players.sort(key=lambda x: x.rank, reverse=True)

    def sort_players_by_score(self, players: List[Player]):
        """Sort a list of players by player score."""
        players.sort(key=lambda x: (x.score, x.rank), reverse=True)

    def _make_matches_list_first_round(self, players: List[Player]) -> List[tuple]:
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

    def _make_matches_list(self, players: List[Player]) -> List[tuple]:
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
                player_without_match_ids.remove(first_player.get_id())
                if first_player.previous_opponent == second_player.get_id():
                    if len(player_without_match_ids) > 1:
                        second_player = next(iter_players)
                player_without_match_ids.remove(second_player.get_id())
                first_player.previous_opponent = second_player.get_id()
                second_player.previous_opponent = first_player.get_id()
                matches.append((first_player, second_player))
                break

        return matches

    def update_player_score(self, player: Player, matches: List[Match]):
        """Update the total score of a player with the result of the match."""
        for match in matches:
            for result in match:
                if player == result.player:
                    player.score += result.score

    def make_a_round(self, tournament_round: Round, tournament_view: TournamentView, players: List[Player]):
        """Implements the progression of a round following the swiss system."""
        if tournament_round == FIRST_ROUND_ID:
            self.sort_players_by_rank(players)
            matches = self._make_matches_list_first_round(players)
        else:
            self.sort_players_by_score(players)
            matches = self._make_matches_list(players)

        tournament_view.show_matches_list(tournament_round, matches)

        for match in matches:
            new_match = tournament_view.prompt_enter_match_score(match)
            tournament_round.matches.append(new_match)
        for player in players:
            self.update_player_score(player, tournament_round.matches)
