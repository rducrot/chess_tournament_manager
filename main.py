from controller import Controller
from models.tournament import Tournament
from constants import TIME_CONTROL_BLITZ

tournois = Tournament("Régional 2022", "Strasbourg", "01/05/2022",
                      TIME_CONTROL_BLITZ, "Premier tournois de la saison")


def main():
    controller = Controller(tournois)
    controller.run()


if __name__ == "__main__":
    main()
