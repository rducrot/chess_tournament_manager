"""Define the Data Load Controller."""
from typing import List

from tinydb import TinyDB

from constants import *
from models.tournament import Tournament
from models.player import Player
from models.round import Round
from models.match import Match, Result


class DataLoadController:

    def load_tournament(self, db: TinyDB):
        """Load the tournament from the database."""
        tournament_table = db.table(DB_TABLE_TOURNAMENT)
        try:
            serialized_tournament = tournament_table.all()[0]
        except IndexError:
            return None
        except AttributeError:
            return None

        tournament = Tournament(
            name=serialized_tournament[DB_TOURNAMENT_NAME],
            place=serialized_tournament[DB_TOURNAMENT_PLACE],
            date=serialized_tournament[DB_TOURNAMENT_DATE],
            time_control=serialized_tournament[DB_TOURNAMENT_TIME_CONTROL],
            description=serialized_tournament[DB_TOURNAMENT_DESCRIPTION],
            number_of_rounds=serialized_tournament[DB_TOURNAMENT_NUMBER_OF_ROUNDS],
            played_rounds=serialized_tournament[DB_TOURNAMENT_PLAYED_ROUNDS])

        if tournament.played_rounds == BEGINNING_PLAYED_ROUNDS_NUMBER:
            tournament.init_rounds()

        return tournament

    def load_players(self, db: TinyDB) -> List:
        """Load the players from the database."""
        players_table = db.table(DB_TABLE_PLAYERS)
        serialized_players = players_table.all()
        players = []

        for serialized_player in serialized_players:
            player = Player(
                last_name=serialized_player[DB_PLAYER_LAST_NAME],
                first_name=serialized_player[DB_PLAYER_FIRST_NAME],
                date_of_birth=serialized_player[DB_PLAYER_DATE_OF_BIRTH],
                gender=serialized_player[DB_PLAYER_GENDER],
                rank=serialized_player[DB_PLAYER_RANK])
            player.set_id(serialized_player[DB_PLAYER_ID])

            players.append(player)

        return players

    def _load_rounds(self, tournament: Tournament, db: TinyDB) -> List[Round]:
        """Load the played rounds from the database."""
        rounds_table = db.table(DB_TABLE_ROUNDS)
        serialized_rounds = rounds_table.all()
        tournament_rounds = []

        for serialized_round in serialized_rounds:
            tournament_round = Round(serialized_round[DB_ROUND_ID])
            tournament_round.set_beginning_time(serialized_round[DB_ROUND_BEGINNING_TIME])
            tournament_round.set_ending_time(serialized_round[DB_ROUND_ENDING_TIME])

            for serialized_match in serialized_round[DB_ROUND_MATCHES_LIST].values():
                first_player = tournament.get_player(serialized_match[DB_MATCH_FIRST_PLAYER_ID])
                second_player = tournament.get_player(serialized_match[DB_MATCH_SECOND_PLAYER_ID])
                match = Match(Result(first_player, serialized_match[DB_MATCH_FIRST_PLAYER_SCORE]),
                              Result(second_player, serialized_match[DB_MATCH_SECOND_PLAYER_SCORE]))
                tournament_round.matches.append(match)

            tournament_rounds.append(tournament_round)

        return tournament_rounds

    def _calculate_players_scores(self, tournament):
        """Calculate the players' scores from the played matches."""
        for player in tournament.players:
            player.reset_score()
            for tournament_round in tournament.rounds:
                player.update_score(tournament_round.matches)

    def load_played_tournament(self, db: TinyDB) -> Tournament:
        """Load a tournament with its players, rounds and played matches from a database."""
        tournament = self.load_tournament(db)
        tournament.players = self.load_players(db)
        tournament.rounds = self._load_rounds(tournament, db)
        self._calculate_players_scores(tournament)
        tournament.sort_players_by_score()

        return tournament
