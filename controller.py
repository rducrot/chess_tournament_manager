"""Define the main controller."""

from random import choice, randrange

from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match

from views.base import View

from constants import NUMBER_OF_PLAYERS, PLAYERS_LAST_NAMES, PLAYERS_FIRST_NAMES, PLAYERS_BIRTH_DATES, GENDERS


class Controller:
    """Main controller."""
    def __init__(self, current_tournament: Tournament):
        self.tournament = current_tournament

    def get_players(self):
        """Add players to the tournament."""
        while len(self.tournament.players) < NUMBER_OF_PLAYERS:
            self.tournament.players.append(Player(choice(PLAYERS_LAST_NAMES),
                                                  choice(PLAYERS_FIRST_NAMES),
                                                  choice(PLAYERS_BIRTH_DATES),
                                                  choice(GENDERS),
                                                  randrange(980, 1400)))

    def get_rounds(self):
        """Add rounds to the tournament."""
        round_number = 1
        while len(self.tournament.rounds) < self.tournament.number_of_rounds:
            self.tournament.rounds.append(Round(f"Round {round_number}"))
            round_number += 1

    def run(self):
        self.get_players()
        self.get_rounds()

        view = View()
        player_1 = view.prompt_add_a_player()
        print(player_1)

        self.tournament.rounds[0].matches.append(Match(([self.tournament.players[0], 1],
                                                        [self.tournament.players[1], 0])))

        print(self.tournament)
        print(self.tournament.players)
        print(self.tournament.rounds)
        print(self.tournament.rounds[0].matches)
