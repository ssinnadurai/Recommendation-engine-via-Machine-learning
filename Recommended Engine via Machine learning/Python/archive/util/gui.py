import csv
import sys

from archive.driver import get_recommendation_content_based, get_recommendation_collaborative_based
from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QApplication, QTableView, QAbstractItemView, QPushButton, QVBoxLayout, QMessageBox, \
    QTabWidget


def table_view_factory(self):
    table_view = QTableView()
    table_view.setSortingEnabled(True)
    table_view.verticalHeader().hide()
    table_view.horizontalHeader().setStretchLastSection(True)  # the last column consumes any empty space
    table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # disable editing
    table_view.setSelectionMode(QAbstractItemView.SingleSelection)  # disable multiple highlighting
    table_view.setSelectionBehavior(QAbstractItemView.SelectRows)  # selects the row instead of just the cell
    return table_view


class ResultsGUI(QWidget):

    def __init__(self, key_value, column_headers, method, parent=None):
        super(ResultsGUI, self).__init__(parent)

        # set window dimension and center it
        screen = QApplication.desktop().screenGeometry()
        width = int(screen.width() * 0.5)
        height = int(screen.height() * 0.5)
        xpos = screen.width() // 2 - width // 2
        ypos = screen.height() // 2 - height // 2
        self.setGeometry(xpos, ypos, width, height)

        # Initialize tabs
        self.tabs = QTabWidget(self)
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        self.tab1.layoutVertical = QVBoxLayout(self.tab1)
        self.tab2.layoutVertical = QVBoxLayout(self.tab2)
        self.tab3.layoutVertical = QVBoxLayout(self.tab3)
        self.tab1.setLayout(self.tab1.layoutVertical)
        self.tab2.setLayout(self.tab2.layoutVertical)
        self.tab3.setLayout(self.tab3.layoutVertical)
        self.tabs.addTab(self.tab1, 'Alg 1')
        self.tabs.addTab(self.tab2, 'Alg 2')
        self.tabs.addTab(self.tab3, 'Alg 3')

        # table view 1
        self.tab1.tableView = table_view_factory(self.tab1)
        self.tab1.model = QStandardItemModel(self.tab1)
        self.tab1.tableView.setModel(self.tab1.model)
        self.tab1.layoutVertical.addWidget(self.tab1.tableView)

        # table view 2
        self.tab2.tableView = table_view_factory(self.tab2)
        self.tab2.model = self.tab1.model
        self.tab2.tableView.setModel(self.tab2.model)
        self.tab2.layoutVertical.addWidget(self.tab2.tableView)

        # table view 3
        self.tab3.tableView = table_view_factory(self.tab3)
        self.tab3.model = self.tab1.model
        self.tab3.tableView.setModel(self.tab3.model)
        self.tab3.layoutVertical.addWidget(self.tab3.tableView)

        self.tab1.model.setHorizontalHeaderLabels(column_headers)

        if method == "cb":
            data = get_recommendation_content_based(key_value)
        else:
            data = get_recommendation_collaborative_based(key_value)

        for rank, row in enumerate(data, start=1):
            items = [
                QStandardItem(str(field)) for field in row
            ]
            items.insert(0, QStandardItem(str(rank)))
            self.tab1.model.appendRow(items)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class DatasetGUI(QWidget):

    def __init__(self, key_col, movies_file_path, user_profiles_file_path, parent=None):
        super(DatasetGUI, self).__init__(parent)
        self.key_col = key_col
        self.movies_file_path = movies_file_path
        self.user_profiles_file_path = user_profiles_file_path
        self.column_headers = next(csv.reader(open(movies_file_path, 'r')))
        self.method = ""

        # set window dimension and center it
        screen = QApplication.desktop().screenGeometry()
        self.width = int(screen.width() * 0.5)
        self.height = int(screen.height() * 0.5)
        self.xpos = screen.width() // 2 - self.width // 2
        self.ypos = screen.height() // 2 - self.height // 2
        self.setGeometry(self.xpos, self.ypos, self.width, self.height)

        # setup the view of the GUI
        self.tableView = table_view_factory(self)
        self.model = QStandardItemModel(self)   # data is stored and accessed using this field
        self.tableView.setModel(self.model)
        self.tableView.doubleClicked.connect(self.parse_row)  # double-clicking a row triggers an event

        # button triggers the importing of data from a csv file
        self.pushButtonLoadMovies = QPushButton(self)
        self.pushButtonLoadMovies.setText("Load Movies CSV File")
        self.pushButtonLoadMovies.clicked.connect(lambda: self.load_csv(self.movies_file_path, "cb"))

        # button triggers the importing of data from a csv file
        self.pushButtonLoadUserProfiles = QPushButton(self)
        self.pushButtonLoadUserProfiles.setText("Load User Profile CSV File")
        self.pushButtonLoadUserProfiles.clicked.connect(lambda: self.load_csv(self.user_profiles_file_path, "cf"))

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.pushButtonLoadMovies)
        self.layoutVertical.addWidget(self.pushButtonLoadUserProfiles)

    @QtCore.pyqtSlot()
    def load_csv(self, file_path, method):
        self.model.clear()
        self.method = method
        reader = csv.reader(open(file_path, 'r'))
        self.model.setHorizontalHeaderLabels(next(reader))
        for row in reader:
            items = [
                QStandardItem(field) for field in row
            ]
            self.model.appendRow(items)

    @QtCore.pyqtSlot()
    def parse_row(self):
        row = self.tableView.selectionModel().currentIndex().row()
        key_value = self.model.item(row, self.key_col).text()
        msg_box = QMessageBox()
        msg_box.setModal(True)
        msg_box.setIcon(QMessageBox.Question)
        if self.method == "cb":
            msg_box.setText("Recommend movies similar to " + key_value + "?")
        else:
            msg_box.setText("Recommend movies to the user with id " + key_value + "?")
        msg_box.setWindowTitle("Selection Confirmation")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        return_value = msg_box.exec()
        if return_value == QMessageBox.Yes:
            if self.method == "cb":
                self.results_window = ResultsGUI(key_value, self.column_headers, "cb")
            else:
                self.results_window = ResultsGUI(int(key_value), self.column_headers, "cf")
            self.results_window.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName('Movie Recommendation App')

    main = DatasetGUI(1, '../data/sample_movie_dataset.csv', "../data/user_profile_logs.csv")
    main.show()

    sys.exit(app.exec_())
