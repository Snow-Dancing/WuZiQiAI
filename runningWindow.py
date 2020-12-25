from PyQt5.QtWidgets import QLabel, QDialog, QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont, QBrush
from PyQt5.QtCore import Qt
from betaGameLogit import GameOver
import sys

class AiSearchingWindow(QDialog):

    def __init__(self, width, height, parent):
        super(QDialog, AiSearchingWindow).__init__(self, parent)
        self.setFixedSize(width, height)
        """ label"""
        searchingLabel = QLabel("AI落子中...", self)
        searchingLabel.setFixedSize(width, height)
        searchingLabel.move(80, 0)

        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)      # 设置加粗类型
        font.setPointSize(40)   # 设置字体大小
        font.setWeight(80)      # 设置字体粗细
        searchingLabel.setFont(font)
        searchingLabel.setStyleSheet("color: red")

        self.setStyleSheet("background-color:rgb(249, 214, 91)")
        self.setWindowTitle("AI落子中")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        btn = QPushButton("dialog", self)
        self.resize(700,300)
        btn.move(100,100)
        btn.clicked.connect(self.winCreate)
        self.show()

    def winCreate(self):
        wind = AiSearchingWindow(400, 200, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Demo()
    sys.exit(app.exec_())
