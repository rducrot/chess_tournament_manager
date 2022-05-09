from models.tournament import Tournament

from controllers.base import Controller
from controllers.swisssystem import SwissSystem

from views.base import View

from constants import TIME_CONTROL_BLITZ


def main():
    view = View()
    tournament_system = SwissSystem()
    tournament = Tournament("Régional 2022", "Strasbourg", "01/05/2022",
                            TIME_CONTROL_BLITZ, "Premier tournois de la saison")

    controller = Controller(view, tournament_system, tournament)
    controller.run()


if __name__ == "__main__":
    main()
