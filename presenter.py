import sys
from typing import Optional

from PyQt6 import QtWidgets


class Presenter:
    def __init__(self):
        # print("Presenter.__init__()", flush=True)
        from model.Database import Database
        from view.MainWindow import MainWindow
        self.model = Database()
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = MainWindow(self)

    def start(self):
        # print("Presenter.start()", flush=True)
        self.view.show()
        self.app.exec()

    def fetch_data(self, server: str, distance: Optional[int], reference: Optional[tuple[int, int]]):
        # print(f"Presenter.fetch_data({server})", flush=True)
        self.model.fill_database(server)
        self.display_data(distance, reference)

    def display_data(self, distance: Optional[int], reference: Optional[tuple[int, int]]):
        # print("Presenter.display_data()", flush=True)
        self.view.right_side.set_data(self.model.get_ghosts(distance, reference))

    def copy_to_clipboard(self, distance: Optional[int], reference: Optional[tuple[int, int]]):
        # print(f"Presenter.copy_to_clipboard({distance_str})", flush=True)
        gt = self.model.get_ghosts(distance)
        copy_string = "\n".join([f"[town]{t.id}[/town] {t.points} {t.x}/{t.y}" for t in gt])
        QtWidgets.QApplication.clipboard().setText(copy_string)
        # print(f"Copied {len(copy_string)} characters to the clip board", flush=True)


if __name__ == '__main__':
    presenter = Presenter()
    presenter.start()
