from PyQt5.QtWidgets import QLabel, QDialog, QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
import sys


class ChooseOrderWindow(QDialog):

    firstOrderSignal = pyqtSignal()
    secondOrderSignal = pyqtSignal()

    def __init__(self, width, height, parent, listener):
        super(QDialog, ChooseOrderWindow).__init__(self, parent)
        self.setFixedSize(width, height)

        self.firstOrderSignal.connect(listener.firstOrderEvent)
        self.secondOrderSignal.connect(listener.secondOrderEvent)

        chooseLabel = QLabel("请选择先手或后手", self)
        chooseLabel.setFixedSize(450, 200)
        chooseLabel.move(50, 0)

        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)      # 设置加粗类型
        font.setPointSize(30)   # 设置字体大小
        font.setWeight(80)      # 设置字体粗细
        chooseLabel.setFont(font)
        chooseLabel.setStyleSheet("color: green")

        font.setPointSize(20)

        firstButton = QPushButton("先手", self)
        firstButton.setFixedSize(100, 50)
        firstButton.move(80, 200)
        firstButton.setFont(font)
        firstButton.setStyleSheet("background-color:black;color:white;")
        firstButton.clicked.connect(self.firstButtonEvent)

        secondButton = QPushButton("后手", self)
        secondButton.setFixedSize(100, 50)
        secondButton.move(230, 200)
        secondButton.setFont(font)
        secondButton.setStyleSheet("background-color:white;color:black;")
        secondButton.clicked.connect(self.secondButtonEvent)

        self.setStyleSheet("background-color:rgb(249, 214, 91)")
        # self.setStyleSheet("background-color:gray")
        self.setWindowTitle("先后手选择")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def firstButtonEvent(self):
        self.firstOrderSignal.emit()
        self.close()

    def secondButtonEvent(self):
        self.secondOrderSignal.emit()
        self.close()


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        btn = QPushButton("dialog", self)
        self.resize(700,300)
        btn.move(100,100)
        btn.clicked.connect(self.winCreate)
        self.show()

    def winCreate(self):
        wind = ChooseOrderWindow(400, 300, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Demo()
    sys.exit(app.exec_())
