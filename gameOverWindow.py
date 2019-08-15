from PyQt5.QtWidgets import QLabel, QDialog, QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont, QBrush
from PyQt5.QtCore import Qt
import sys

class GameOverWindow(QDialog):

    def __init__(self, width, height, parent=None):
        super(QDialog, GameOverWindow).__init__(self, parent)
        self.setFixedSize(width, height)
        """Game over label"""
        gameOverLabel = QLabel("Game Over!", self)
        lwidth = width
        lheight = height
        gameOverLabel.setFixedSize(lwidth, lheight)
        gameOverLabel.move(int((width - lwidth)/2) + 40, int((height - lheight) / 2))
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)      # 设置加粗类型
        font.setPointSize(40)   # 设置字体大小
        font.setWeight(80)      # 设置字体粗细
        gameOverLabel.setFont(font)
        gameOverLabel.setStyleSheet("color: red")

        self.setStyleSheet("background-color:rgb(249, 214, 91)")
        self.setWindowTitle("游戏结束")
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
        wind = GameOverWindow(400, 200, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Demo()
    sys.exit(app.exec_())
