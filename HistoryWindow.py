from PyQt5.QtWidgets import QTableView, QPushButton, QHeaderView, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class HistoryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("History")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.db = None
        self.table_model = None

        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.horizontalHeader().setStretchLastSection(1)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.load_data()

        self.btn_clear_history = QPushButton("Clear")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_view)
        self.layout.addWidget(self.btn_clear_history)
        self.setLayout(self.layout)

        self.setGeometry(400, 200, 400, 600)

        self.btn_clear_history.clicked.connect(self.clear_history)

    def load_data(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('history.db')
        self.db.open()

        self.table_model = QSqlTableModel()
        self.table_model.setTable("history")
        self.table_model.select()

        self.table_view.setModel(self.table_model)

    def clear_history(self):
        query = QSqlQuery()
        query.exec_("DELETE FROM history")
        if query.isActive():
            print("Records deleted successfully")
        else:
            print("Error deleting records: ", query.lastError().text())

        self.load_data()