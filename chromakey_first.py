import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import control_edit_preview_window

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1400,800)
        self.setWindowTitle('chroma key')

        self.chroma_title = QLabel('Chroma Key', self)
        self.chroma_title.setGeometry(450, 200, 500, 200)
        self.chroma_title.setAlignment(Qt.AlignCenter)
        self.chroma_title.setStyleSheet("font-size : 48pt; font-family : '휴먼편지체'; ")

        self.chroma_start_btn = QPushButton('시작하기', self)
        self.chroma_start_btn.setGeometry(600,500,200,100)
        self.chroma_start_btn.setStyleSheet("font-size : 20pt; font-family : '휴먼옛체';")
        self.chroma_start_btn.setCursor(QCursor(Qt.PointingHandCursor))  #버튼의 cursor를 변경
        self.chroma_start_btn.clicked.connect(self.goToEdit)

    def goToEdit(self):
        self.control_edit_preview_window = control_edit_preview_window.ControlWindow()
        self.close()
        self.control_edit_preview_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()