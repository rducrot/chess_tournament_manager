"""Define the Tournament View."""
from typing import List

from constants import *
from models.match import Match, Result
from models.round import Round


class TournamentView:

    def show_matches_list(self, tournament_round: Round, matches: List[tuple]):
        """Print the matches of the current round."""
        print(SEPARATOR)
        print(f"Liste des matchs du {tournament_round.name} :")
        for match in matches:
            print(str(match))
        print(SEPARATOR)

    def prompt_enter_match_score(self, players_in_match: tuple) -> Match:
        """Prompt to add the scores of the players of the current match."""
        first_player = players_in_match[0]
        second_player = players_in_match[1]
        while True:
            first_player_prompt = input(f"Score du joueur {first_player} - (V)ictoire, (D)éfaite, (N)ul : ")
            if first_player_prompt == WIN_PROMPT:
                first_player_score = WIN_SCORE
                second_player_score = LOSE_SCORE
                print(f"{second_player} : Défaite")
                break
            elif first_player_prompt == LOSE_PROMPT:
                first_player_score = LOSE_SCORE
                second_player_score = WIN_SCORE
                print(f"{second_player} : Victoire")
                break
            elif first_player_prompt == DRAW_PROMPT:
                first_player_score = DRAW_SCORE
                second_player_score = DRAW_SCORE
                print(f"{second_player} : Match Nul")
                break

        match = Match(Result(first_player, first_player_score), Result(second_player, second_player_score))
        return match

    def prompt_continue_next_round(self):
        """Prompt to ask to continue to the next round."""
        print(SEPARATOR)
        while True:
            continue_next_round = input("Souhaitez-vous passer au tour suivant ? "
                                        f"(O/{CONTINUE_NEXT_ROUND_FALSE_PROMPT})")
            if continue_next_round == CONTINUE_NEXT_ROUND_FALSE_PROMPT:
                return False
            return True
