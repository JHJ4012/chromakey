from PyQt5.QtWidgets import *
import chromakey_first,chromakey_edit,chromakey_preview

class ControlWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.initUI()

    def initUI(self):

        self.setFixedSize(1400, 800)
        self.setWindowTitle('chroma key edit')

        edit_window = chromakey_edit.EditWindow()
        preview_window = chromakey_preview.PreviewWindow()

        self.layout = QStackedLayout()
        self.layout.addWidget(edit_window)
        self.layout.addWidget(preview_window)
        self.setLayout(self.layout)

        edit_window.complete_btn.clicked.connect(self.goToPreview)
        edit_window.back_first_window.clicked.connect(self.backToFirst)

        preview_window.back_edit.clicked.connect(self.backToEdit)

    def goToPreview(self):              #preview로 갈 때 창이 꺼지지 않고 layout에서 widget이 바뀌는 형식으로 바꿈.
        self.layout.setCurrentIndex(1)
        self.setWindowTitle('chroma key preview')

    def backToEdit(self):
        self.layout.setCurrentIndex(0)
        self.setWindowTitle('chroma key edit')

    def backToFirst(self):      #처음으로 돌아가면 작업 내용 초기화 해야되므로 self.close를 해줌. 나중에 진짜 나가시겠습니까? 라는 대화창 띄워주는 것 추가하기.
        self.first_window = chromakey_first.MainWindow()
        self.close()
        self.first_window.show()