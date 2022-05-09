"""Base view."""
from models.player import Player
from models.tournament import Tournament
from models.match import Match
from constants import DEFAULT_NUMBER_OF_ROUNDS, WIN_PROMPT, WIN_SCORE, LOSE_PROMPT, LOSE_SCORE, DRAW_PROMPT, DRAW_SCORE, SCORE_PROMPT, UPDATE_TOURNAMENT_PROMPT, UPDATE_PLAYERS_LIST_PROMPT


class View:

    def prompt_ask_new_tournament(self):
        """Ask for a new tournament"""
        update_tournament = input("Souhaitez-vous initialiser un nouveau tournoi ? (O/N)")
        if update_tournament != UPDATE_TOURNAMENT_PROMPT:
            return False
        return True

    def prompt_update_current_tournament(self) -> Tournament:
        """Prompt to add a tournament."""
        name = input("Nom du tournois : ")
        place = input("Lieu : ")
        date = input("Date : ")
        time_control = input("Mode de gestion du temps : ")
        description = input(" Description : ")
        number_of_rounds = input("Nombre de tours (Par défaut : 4) : ")
        if not number_of_rounds:
            number_of_rounds = DEFAULT_NUMBER_OF_ROUNDS

        tournament = Tournament(name, place, date, time_control, description, number_of_rounds)
        return tournament

    def prompt_ask_update_players_list(self):
        update_players_list = input("Souhaitez-vous mettre à jour la liste des joueurs ?")
        if update_players_list != UPDATE_PLAYERS_LIST_PROMPT:
            return False
        return True

    def prompt_add_a_player(self) -> Player:
        """Prompt to add a player."""
        last_name = input("Nom du joueur : ")
        first_name = input("Prénom du joueur : ")
        date_of_birth = input("Date de naissance : ")
        gender = input("Genre : ")
        rank = input("Rang : ")

        new_player = Player(last_name, first_name, date_of_birth, gender, rank)
        return new_player

    def show_matches_players_list(self, matches):
        """Print the matches of the turn."""
        print(f"Liste des matchs du tour :")
        for match in matches:
            print(str(match))

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
        first_player.score += first_player_score
        second_player.score += second_player_score
        match = Match(((first_player, first_player_score), (second_player, second_player_score)))
        return match
