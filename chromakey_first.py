import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import chromakey_edit

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1400,700)
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
        self.hide()
        chromakey_edit.EditWindow().show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'You really want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()