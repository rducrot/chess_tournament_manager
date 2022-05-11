"""App entry point."""
from constants import TIME_CONTROL_BLITZ
from controllers.base import Controller
from controllers.swisssystem import SwissSystemController
from models.tournament import Tournament
from views.base import View
from views.tournament import TournamentView


def main():
    view = View()
    tournament_view = TournamentView()
    tournament_controller = SwissSystemController()
    tournament = Tournament("Régional 2022", "Strasbourg", "01/05/2022",
                            TIME_CONTROL_BLITZ, "Premier tournois de la saison")

    app = Controller(view, tournament_view, tournament_controller, tournament)
    app.run()


if __name__ == "__main__":
    main()
