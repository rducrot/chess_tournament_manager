"""App entry point."""
from tinydb import TinyDB

from constants import *
from controllers.base import Controller
from controllers.swisssystem import SwissSystemController
from views.base import View
from views.tournament import TournamentView


def main():
    view = View()
    tournament_view = TournamentView()
    tournament_controller = SwissSystemController()
    db = TinyDB(DB_NAME)
    report_db = TinyDB(REPORT_DB_NAME)

    app = Controller(view, tournament_view, tournament_controller, db, report_db)
    app.run()


if __name__ == "__main__":
    main()
