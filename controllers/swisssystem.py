"""Define the Swiss System Controller."""
from typing import List

import constants
from models.match import Match
from models.player import Player
from models.round import Round
from models.tournament import Tournament
from views.tournament import TournamentView


class SwissSystemController:
    """Tournament controller implementing the Swiss System."""

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

    def make_a_round(self, round_: Round, tournament_view: TournamentView, tournament: Tournament):
        """Implements the progression of a round following the swiss system."""
        if round_ == constants.FIRST_ROUND_ID:
            tournament.sort_players_by_rank()
            matches = self._make_matches_list_first_round(tournament.players)
        else:
            tournament.sort_players_by_score()
            matches = self._make_matches_list(tournament.players)

        tournament_view.show_matches_list(round_, matches)

        for match in matches:
            played_match = tournament_view.prompt_enter_match_score(match)
            round_.matches.append(played_match)
        for player in tournament.players:
            player.update_score(round_.matches)
