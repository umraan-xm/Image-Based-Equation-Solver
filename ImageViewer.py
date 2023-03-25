from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtGui import QPixmap


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            image_path = url.toLocalFile()
            pixmap = QPixmap(image_path)
            self.setPixmap(pixmap)

    def browse(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open image", "C:/",
            "Image Files (*.png *.jpg *.jpeg)",)
        if file_name:
            pixmap = QPixmap(file_name)
            self.setPixmap(pixmap)

