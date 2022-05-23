"""Define the Tournament."""
from typing import List

from tinydb import TinyDB

import constants
from .player import Player
from .round import Round


class Tournament:
    """Tournament class."""

    def __init__(self, name, place, date, time_control,
                 description, number_of_rounds=constants.DEFAULT_NUMBER_OF_ROUNDS,
                 played_rounds=constants.BEGINNING_PLAYED_ROUNDS_NUMBER):
        self.name = name
        self.place = place
        self.date = date
        self.time_control = time_control
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.played_rounds = played_rounds
        self.rounds: List[Round] = []
        self.players: List[Player] = []

    def __str__(self):
        return f"Tournois {self.name} du {self.date} à {self.place}"

    def __repr__(self):
        return str(self)

    def get_player(self, player_id: int) -> Player:
        """Get a player from the players list by its id."""
        for player in self.players:
            if player.get_id() == player_id:
                return player

    def reset_players_list(self):
        """Reset the players list."""
        self.players = []

    def players_list_is_empty(self):
        """Return a boolean to know if the players list is empty."""
        return len(self.players) == 0

    def reset_players_scores(self):
        """Reset the score of every player."""
        for player in self.players:
            player.reset_score()

    def sort_players_by_name(self):
        """Sort the players list by player name."""
        self.players.sort(key=lambda x: (x.last_name, x.first_name))

    def sort_players_by_rank(self):
        """Sort the players list by player rank."""
        self.players.sort(key=lambda x: x.rank, reverse=True)

    def sort_players_by_score(self):
        """Sort the players list by player score."""
        self.players.sort(key=lambda x: (x.score, x.rank), reverse=True)

    def init_rounds(self):
        """Initialize the rounds of the tournament using number_of_rounds."""
        round_number = 1
        while len(self.rounds) < self.number_of_rounds:
            self.rounds.append(Round(round_number))
            round_number += 1

    def all_rounds_played(self):
        """Return a boolean to know if all the rounds are played."""
        return self.played_rounds >= self.number_of_rounds

    def save_basic_information(self, db: TinyDB):
        """Save basic information about the tournament to the database."""
        tournament_table = db.table(constants.DB_TABLE_TOURNAMENT)
        tournament_table.truncate()
        serialized_tournament = {
            constants.DB_TOURNAMENT_NAME: self.name,
            constants.DB_TOURNAMENT_PLACE: self.place,
            constants.DB_TOURNAMENT_DATE: self.date,
            constants.DB_TOURNAMENT_TIME_CONTROL: self.time_control,
            constants.DB_TOURNAMENT_DESCRIPTION: self.description,
            constants.DB_TOURNAMENT_NUMBER_OF_ROUNDS: self.number_of_rounds,
            constants.DB_TOURNAMENT_PLAYED_ROUNDS: self.played_rounds
        }
        tournament_table.insert(serialized_tournament)

    def save_players(self, db: TinyDB):
        """Save the players list to the database."""
        players_table = db.table(constants.DB_TABLE_PLAYERS)
        players_table.truncate()
        for player in self.players:
            player.save(db)

    def save_rounds(self, db: TinyDB):
        """Save each match for each round to the database."""
        rounds_table = db.table(constants.DB_TABLE_ROUNDS)
        rounds_table.truncate()
        for round_ in self.rounds:
            round_.save(db)

    def save(self, db: TinyDB):
        """Save the whole tournament including players and played rounds."""
        self.save_basic_information(db)
        self.save_players(db)
        self.save_rounds(db)
