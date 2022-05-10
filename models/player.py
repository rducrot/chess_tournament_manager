"""Define the players."""
from itertools import count


class Player:
    """Player class."""
    id_iter = count()

    def __init__(self, last_name, first_name,
                 date_of_birth, gender, rank):
        self.id = next(self.id_iter)
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rank = rank
        self.score = 0

    def __str__(self):
#        return f"{self.first_name} {self.last_name} ({self.rank} points)"
        return f"{self.first_name} {self.last_name} ({self.score})"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __eq__(self, other):
        return self.rank == other.rank
