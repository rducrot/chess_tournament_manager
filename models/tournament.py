class Tournament:

    def __int__(self, name, place, date, rounds, time_control,
                description, number_of_rounds=4):
        self.name = name
        self.place = place
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.rounds = rounds
        self.players = []
        self.time_control = time_control
        self.description = description
