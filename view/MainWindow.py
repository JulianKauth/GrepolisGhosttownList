from presenter import Presenter
from model.Town import Town

from PyQt6.QtWidgets import QWidget, QPushButton, QFormLayout, QLineEdit, QTableWidget, QTableWidgetItem, QMainWindow, QSplitter
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, presenter: Presenter):
        super().__init__()
        self.presenter = presenter

        self.left_side = LeftSide(self, presenter)
        self.right_side = ListOfTowns(self, presenter)

        horizontal_splitter = QSplitter(Qt.Orientation.Horizontal, self)

        horizontal_splitter.addWidget(self.left_side)
        horizontal_splitter.addWidget(self.right_side)

        self.setCentralWidget(horizontal_splitter)


class LeftSide(QWidget):
    def __init__(self, parent: QWidget, presenter: Presenter):
        super().__init__(parent)
        self.presenter = presenter

        self.widget_server = QLineEdit(self)
        self.widget_distance = QLineEdit(self)
        self.widget_reference = QLineEdit(self)
        self.button_fetch_data = QPushButton("Fetch Data", self)
        self.button_copy_to_clipboard = QPushButton("Copy to Clipboard", self)

        form_layout = QFormLayout()
        form_layout.addRow("Server: ", self.widget_server)
        form_layout.addRow("Max Distance: ", self.widget_distance)
        form_layout.addRow("From x, y: ", self.widget_reference)
        form_layout.addRow(self.button_fetch_data)
        form_layout.addRow(self.button_copy_to_clipboard)
        self.setLayout(form_layout)

        self.button_fetch_data.clicked.connect(lambda x: self.presenter.fetch_data(self.widget_server.text(), self.distance_as_int(), self.reference_as_point()))
        self.widget_server.returnPressed.connect(lambda: self.presenter.fetch_data(self.widget_server.text(), self.distance_as_int(), self.reference_as_point()))
        self.widget_distance.returnPressed.connect(lambda: self.presenter.fetch_data(self.widget_server.text(), self.distance_as_int(), self.reference_as_point()))
        self.widget_reference.returnPressed.connect(lambda: self.presenter.fetch_data(self.widget_server.text(), self.distance_as_int(), self.reference_as_point()))
        self.button_copy_to_clipboard.clicked.connect(lambda x: self.presenter.copy_to_clipboard(self.distance_as_int(), self.reference_as_point()))

    def distance_as_int(self):
        try:
            return int(self.widget_distance.text())
        except ValueError:
            return None

    def reference_as_point(self):
        try:
            a, b = self.widget_reference.text().split(",")
            return int(a.strip()), int(b.strip())
        except ValueError:
            return None


class NumericalTableWidgetItem(QTableWidgetItem):
    def __init__(self, number: int):
        super().__init__(f"{number}")
        self.__value = number

    def __lt__(self, other):
        if isinstance(other, NumericalTableWidgetItem):
            return self.__value < other.__value
        else:
            return True


class ListOfTowns(QTableWidget):
    def __init__(self, parent: QWidget, presenter: Presenter):
        super().__init__(parent)
        self.presenter = presenter

    def set_data(self, towns: list[Town]):
        # print(f"ListOfTowns.set_data({len(towns)} towns)")
        self.setSortingEnabled(False)

        headers = ["Town Name", "BBCode", "Points", "X", "Y", "Sea"]
        self.setRowCount(len(towns))
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        for i, town in enumerate(towns):
            self.setItem(i, 0, QTableWidgetItem(town.name))
            self.setItem(i, 1, QTableWidgetItem(f"[town]{town.id}[/town]"))
            self.setItem(i, 2, NumericalTableWidgetItem(town.points))
            self.setItem(i, 3, NumericalTableWidgetItem(town.x))
            self.setItem(i, 4, NumericalTableWidgetItem(town.y))
            self.setItem(i, 5, QTableWidgetItem(f"{town.sea}"))

        self.setSortingEnabled(True)
