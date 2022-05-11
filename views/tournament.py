"""Define the Tournament View."""
from constants import SEPARATOR, WIN_PROMPT, WIN_SCORE, LOSE_PROMPT, LOSE_SCORE, DRAW_PROMPT, DRAW_SCORE
from models.match import Match, Result


class TournamentView:

    def show_matches_list(self, matches):
        """Print the matches of the turn."""
        print(SEPARATOR)
        print(f"Liste des matchs du tour :")
        for match in matches:
            print(str(match))
        print(SEPARATOR)

    def prompt_enter_match_score(self, players_in_match: tuple) -> Match:
        """Prompt to add the scores of the players of a match."""
        first_player = players_in_match[0]
        second_player = players_in_match[1]
        while True:
            first_player_prompt = input(f"Score du joueur {first_player} - (V)ictoire, (D)éfaite, (N)ul : ")
            if first_player_prompt == WIN_PROMPT:
                first_player_score = WIN_SCORE
                second_player_score = LOSE_SCORE
                break
            elif first_player_prompt == LOSE_PROMPT:
                first_player_score = LOSE_SCORE
                second_player_score = WIN_SCORE
                break
            elif first_player_prompt == DRAW_PROMPT:
                first_player_score = DRAW_SCORE
                second_player_score = DRAW_SCORE
                break

        match = Match(Result(first_player, first_player_score), Result(second_player, second_player_score))
        return match
