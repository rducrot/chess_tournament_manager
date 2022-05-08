"""Define the players."""


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

