"""Define the players."""

PLAYERS_LAST_NAMES = ["DUPONT", "MARTIN", "PEREZ", "ROBERT"]
PLAYERS_FIRST_NAMES = ["Camille", "Charlie", "Dominique", "Sam"]
PLAYERS_BIRTH_DATES = ["03/08/1995", "25/02/2000", "09/12/1987", "10/10/1996"]
GENDER_M = 0
GENDER_F = 1
GENDERS = [GENDER_M, GENDER_F]


class Player:
    """Player class."""

    def __init__(self, last_name, first_name,
                 date_of_birth, gender, rank):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rank} points)"

    def __repr__(self):
        return str(self)

