from controller import Controller
from models import tournament

tournois = tournament.Tournament("Régional 2022", "Strasbourg", "01/05/2022",
                                 tournament.TIME_CONTROL_BLITZ, "Premier tournoi de la saison")


def main():
    controller = Controller(tournois)
    controller.run()


if __name__ == "__main__":
    main()
