from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class PreviewWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1400,800)

        self.preview = QLabel(self)
        self.preview.setGeometry(100, 50, 1200, 550)
        self.preview.setStyleSheet("background-color : red")

        self.control_bar = QLabel(self)
        self.control_bar.setGeometry(100, 610, 1200, 50)
        self.control_bar.setStyleSheet("background-color : green")

        self.back_edit = QPushButton('돌아가기',self)
        self.back_edit.setGeometry(100, 725, 100, 50)
        self.back_edit.setCursor(QCursor(Qt.PointingHandCursor))
        # self.back_edit.clicked.connect(self.backEdit)

        self.store = QPushButton('저장',self)
        self.store.setGeometry(1200,725,100,50)
        self.store.setCursor(QCursor(Qt.PointingHandCursor))

    # def backEdit(self):
    #     self.hide()
    #     self.edit = chromakey_edit.EditWindow()
    #     self.edit.show()