"""Define the main controller."""

from random import choice, randrange
from models import tournament, player, round, match


class Controller:
    """Main controller."""
    def __init__(self, current_tournament: tournament.Tournament):
        self.tournament = current_tournament

    def get_players(self):
        """Add players to the tournament."""
        while len(self.tournament.players) < tournament.NUMBER_OF_PLAYERS:
            self.tournament.players.append(player.Player(choice(player.PLAYERS_LAST_NAMES),
                                                         choice(player.PLAYERS_FIRST_NAMES),
                                                         choice(player.PLAYERS_BIRTH_DATES),
                                                         choice(player.GENDERS),
                                                         randrange(980, 1400)))

    def get_rounds(self):
        """Add rounds to the tournament."""
        round_number = 1
        while len(self.tournament.rounds) < tournament.DEFAULT_NUMBER_OF_ROUNDS:
            self.tournament.rounds.append(round.Round(f"Round {round_number}"))
            round_number += 1

    def run(self):
        self.get_players()
        self.get_rounds()

        self.tournament.rounds[0].matches.append(match.Match(([self.tournament.players[0], 1], [self.tournament.players[1], 0])))

        print(self.tournament)
        print(self.tournament.players)
        print(self.tournament.rounds)
        print(self.tournament.rounds[0].matches)
