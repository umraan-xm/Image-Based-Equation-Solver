import logging
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import keras
import numpy as np
from ImageViewer import ImageLabel
from HistoryWindow import HistoryWindow
import solver


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image-Based Equation Solver")
        self.showMaximized()
        # self.setMinimumSize(1280, 720)

        # define instance variables
        self.lbl_image = None
        self.txt_answer_field = None
        self.main_layout = None
        self.splitter = None
        self.wgt_left_sidebar = None
        self.lyt_left_sidebar = None
        self.wgt_right_sidebar = None
        self.lyt_right_sidebar = None
        self.btn_open_image = None
        self.btn_clear_image = None
        self.btn_solve = None
        self.btn_history = None
        self.cb_select_equation_type = None
        self.lbl_info = None
        self.db = None
        self.history_window = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.configure_database()

    def create_widgets(self):
        self.wgt_left_sidebar = QWidget()
        self.wgt_right_sidebar = QWidget()

        self.lbl_image = ImageLabel()
        self.lbl_image.setText("Drag an image here")
        self.lbl_image.setAlignment(Qt.AlignCenter)

        self.btn_open_image = QPushButton("Open")
        self.btn_clear_image = QPushButton("Clear")
        self.btn_solve = QPushButton("Solve")
        self.btn_history = QPushButton("History")

        self.cb_select_equation_type = QComboBox()
        self.cb_select_equation_type.insertItem(0, "Expression")
        self.cb_select_equation_type.insertItem(1, "Quadratic Equation")
        self.cb_select_equation_type.insertItem(2, "Cubic Equation")
        self.cb_select_equation_type.insertItem(3, "Linear System")
        self.cb_select_equation_type.insertItem(4, "Differentiate")
        self.cb_select_equation_type.insertItem(5, "Indefinite Integral")
        self.cb_select_equation_type.insertItem(6, "Definite Integral")

        self.lbl_info = QLabel("\nSolve expressions such as 5 + 2, 27 x 2 etc."
                               "\n\nDivision is not supported.")

        self.txt_answer_field = QTextEdit()
        self.txt_answer_field.setReadOnly(True)
        self.txt_answer_field.setFixedHeight(150)
        self.txt_answer_field.setStyleSheet("font: 36px")

        self.history_window = HistoryWindow()

    def create_layouts(self):
        # initialize layouts
        self.main_layout = QVBoxLayout()
        self.lyt_left_sidebar = QVBoxLayout()
        self.lyt_right_sidebar = QVBoxLayout()

        # create splitter and set splitter properties
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.wgt_left_sidebar)
        self.splitter.addWidget(self.lbl_image)
        self.splitter.addWidget(self.wgt_right_sidebar)
        self.splitter.setSizes([80, 300, 80])
        self.splitter.setCollapsible(0, False)

        # set layouts
        self.wgt_left_sidebar.setLayout(self.lyt_left_sidebar)
        self.lyt_left_sidebar.addWidget(self.btn_open_image)
        self.lyt_left_sidebar.addWidget(self.btn_clear_image)
        self.lyt_left_sidebar.addWidget(self.btn_solve)
        self.lyt_left_sidebar.addStretch(1)
        self.lyt_left_sidebar.addWidget(self.btn_history)
        self.wgt_right_sidebar.setLayout(self.lyt_right_sidebar)
        self.lyt_right_sidebar.addWidget(self.cb_select_equation_type)
        self.lyt_right_sidebar.addWidget(self.lbl_info)
        self.lyt_right_sidebar.addStretch(1)

        self.main_layout.addWidget(self.splitter)
        self.main_layout.addWidget(self.txt_answer_field)

        self.setLayout(self.main_layout)

    def create_connections(self):
        self.btn_open_image.clicked.connect(self.lbl_image.browse)
        self.btn_clear_image.clicked.connect(self.clear)
        self.btn_solve.clicked.connect(self.solve_equation)
        self.btn_history.clicked.connect(self.show_history)
        self.cb_select_equation_type.currentTextChanged.connect(self.display_info)

    def configure_database(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('history.db')
        self.db.open()
        query = QSqlQuery(self.db)
        query.exec_("""
            CREATE TABLE IF NOT EXISTS history(
                equation TEXT,
                solution TEXT
            )
        """)
        if query.isActive():
            print("Table created successfully")
        else:
            print("Error creating table: ", query.lastError().text())

    def add_record(self, equation, solution):
        query = QSqlQuery()
        query.prepare("INSERT INTO history (equation, solution) VALUES (:equation, :solution)")
        query.bindValue(":equation", equation)
        query.bindValue(":solution", solution)
        query.exec_()
        if query.isActive():
            print("Record added successfully")
        else:
            print("Error adding record: ", query.lastError().text())

        self.history_window.load_data()

    def close_connection(self):
        self.db.close()

    def solve_equation(self):
        pixmap = self.lbl_image.pixmap()
        if pixmap:
            image = self.pixmap_to_numpy(pixmap)
            mode = self.cb_select_equation_type.currentText()
            if mode == 'Expression':
                self.process_expression(image)
            if mode == 'Quadratic Equation':
                self.process_quadratic_eq(image)
            if mode == 'Cubic Equation':
                self.process_quadratic_eq(image)
            if mode == 'Linear System':
                self.process_linear_system(image)
            if mode == 'Differentiate':
                self.process_derivative(image)
            if mode == 'Indefinite Integral':
                self.process_indefinite_integral(image)
            if mode == 'Definite Integral':
                self.process_definite_integral(image)
        else:
            QMessageBox.critical(self, 'Error', 'Please input an image.')

    def process_expression(self, image):
        try:
            expression = solver.extract(image)
            solution = solver.solve_expression(expression)

            self.txt_answer_field.setText(solution)

            self.add_record(expression, solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Invalid Expression. Please open another image.')
        except Exception as e:
            logging.exception(e)

    def process_quadratic_eq(self, image):
        try:
            equation = solver.extract(image)
            equation, solution = solver.solve_linear_equation(equation)

            self.add_record(equation, solution)

            solution = self.pretty(solution)
            self.txt_answer_field.setHtml(solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Invalid Equation. Please open another image.')
        except Exception as e:
            logging.exception(e)

    def process_linear_system(self, image):
        try:
            equations = solver.extract_linear_equations(image)
            solution = solver.solve_linear_system(equations)

            self.txt_answer_field.setText(solution)

            self.add_record(equations, solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Invalid system of linear equations. Please open another image.')
        except Exception as e:
            logging.exception(e)

    def process_derivative(self, image):
        try:
            equation = solver.extract(image)
            solution = solver.differentiate(equation)

            equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
            equation = re.sub(r"(x)(\d)", r"\1**\2", equation)
            self.add_record(equation, "Derivative: " + solution)

            solution = self.pretty(solution)
            solution = solution.replace("*", "")

            self.txt_answer_field.setHtml(solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Could not differentiate the equation. Please open another image.')
        except Exception as e:
            logging.exception(e)

    def process_indefinite_integral(self, image):
        try:
            equation = solver.extract(image)
            solution = solver.indefinite_integral(equation)

            equation = equation[1:-2]
            equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
            equation = re.sub(r"(x)(\d)", r"\1**\2", equation)
            self.add_record(equation, "Integral: " + solution)

            solution = self.pretty(solution)
            solution = solution.replace("*", "")

            self.txt_answer_field.setHtml(solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Could not integrate the equation. Please open another image.')
        except Exception as e:
            logging.exception(e)

    def process_definite_integral(self, image):
        try:
            equation = solver.extract(image)
            solution = solver.definite_integral(equation)

            equation = equation[3:-2]
            equation = re.sub(r"(\d)(x)", r"\1*\2", equation)
            equation = re.sub(r"(x)(\d)", r"\1**\2", equation)
            self.add_record(equation, "Definite Integral: " + solution)

            self.txt_answer_field.setHtml(solution)
        except (ValueError, SyntaxError):
            QMessageBox.critical(self, 'Error', 'Could not integrate the equation. Please open another image.')
        except Exception as e:
            logging.exception(e)

    def show_history(self):
        self.history_window.exec_()

    def clear(self):
        self.lbl_image.setPixmap(QPixmap())

    def display_info(self):
        mode = self.cb_select_equation_type.currentText()
        if mode == 'Expression':
            self.lbl_info.setText("<br>Solve expressions such as 5 + 2, 27 x 2 etc."
                                  "<br><br>Division is not supported.")
        if mode == 'Quadratic Equation':
            self.lbl_info.setText("<br>Solve quadratic equations such as 5x<sup>2</sup> + 1 = 0."
                                  "<br><br>Please enter an equation with the variable x only."
                                  "<br><br>Solutions may be complex numbers.")
        if mode == 'Cubic Equation':
            self.lbl_info.setText("<br>Solve cubic equations such as 3x<sup>3</sup> + 2x<sup>2</sup> + 8x = 7."
                                  "<br><br>Please enter an equation with the variable x only."
                                  "<br><br>Solutions may be complex numbers.")
        if mode == 'Linear System':
            self.lbl_info.setText("<br>Solve a linear system of  equations such as:"
                                  "<br>x + 2y = 5"
                                  "<br>2x + 3y = 7"
                                  "<br><br>Please enter 2 equations with the variables x and y only.")
        if mode == 'Differentiate':
            self.lbl_info.setText("<br>Find the derivative of an expression such as 3x<sup>2</sup>"
                                  "<br><br>Do not prepend the expression with d/dx"
                                  "<br><br>Derivatives are calculated with respect to the variable x only")
        if mode == 'Indefinite Integral':
            self.lbl_info.setText("<br>Find the Integral of an expression such as &int;4x<sup>3</sup> + 2x dx"
                                  "<br><br>Integrals are calculated with respect to the variable x only")
        if mode == 'Definite Integral':
            self.lbl_info.setText("<br>Find the Definite Integral of an expression such as "
                                  "<sub>0</sub>&int;<sup>2</sup>4x<sup>3</sup> + 2x dx"
                                  "<br><br>Integrals are calculated with respect to the variable x only")

    @staticmethod
    def pixmap_to_numpy(pixmap):
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format_RGBA8888)
        width, height = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        image = np.array(ptr).reshape((height, width, 4))

        return image

    @staticmethod
    def pretty(text):
        text = text.replace("\n", "<br>")
        text = re.sub(r"sqrt\(([^)]+)\)", r"&radic;\1", text)

        text = re.sub(r"\*\*(\d)", r"<sup>\1</sup>", text)

        return text


def main():
    app = QApplication([])
    app.setStyle("Fusion")
    with open("style.css", 'r') as style:
        app.setStyleSheet(style.read())

    window = MainWindow()
    app.aboutToQuit.connect(window.close_connection)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
