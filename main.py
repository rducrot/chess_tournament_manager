"""App entry point."""
from tinydb import TinyDB

from constants import *
from controllers.base import Controller
from controllers.dataload import DataLoadController
from controllers.swisssystem import SwissSystemController
from views.base import View
from views.report import ReportView
from views.tournament import TournamentView


def main():
    view = View()
    tournament_view = TournamentView()
    report_view = ReportView()

    data_load_controller = DataLoadController()
    tournament_controller = SwissSystemController()

    db = TinyDB(DB_NAME)
    report_db = TinyDB(REPORT_DB_NAME)

    app = Controller(view,
                     tournament_view,
                     report_view,
                     data_load_controller,
                     tournament_controller,
                     db,
                     report_db)
    app.run()


if __name__ == "__main__":
    main()
