from PyQt5.QtWidgets import QLabel, QDialog, QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from betaGameLogit import GameOver
import sys

class GameOverWindow(QDialog):

    callBackSignal = pyqtSignal()
    newGameSignal = pyqtSignal()

    def __init__(self, width, height, parent, winner, listener):
        super(QDialog, GameOverWindow).__init__(self, parent)
        self.setFixedSize(width, height)
        self.listener = listener

        self.callBackSignal.connect(listener.callBackEvent)
        self.newGameSignal.connect(listener.newGameEvent)

        """Game over label"""
        if winner == GameOver.EQUAL:
            gameOverLabel = QLabel("平局!", self)
            gameOverLabel.setFixedSize(width, 200)
            gameOverLabel.move(150, 0)
        elif winner == GameOver.PLAYER_WIN:
            gameOverLabel = QLabel("玩家获胜!", self)
            gameOverLabel.setFixedSize(width, height)
            gameOverLabel.move(100, 0)
        elif winner == GameOver.AI_WIN:
            gameOverLabel = QLabel("AI获胜!", self)
            gameOverLabel.setFixedSize(width, 200)
            gameOverLabel.move(120, 0)
        else:
            raise Exception("Game over window error!")
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)      # 设置加粗类型
        font.setPointSize(40)   # 设置字体大小
        font.setWeight(80)      # 设置字体粗细
        gameOverLabel.setFont(font)
        gameOverLabel.setStyleSheet("color: red")

        if winner == GameOver.AI_WIN or winner == GameOver.EQUAL:
            font.setPointSize(20)

            callBackButton = QPushButton("悔棋", self)
            callBackButton.setFixedSize(100, 50)
            callBackButton.move(80, 200)
            callBackButton.setFont(font)
            callBackButton.setStyleSheet("background-color:black;color:white;")
            callBackButton.clicked.connect(self.callBackButtonEvent)

            newGameButton = QPushButton("认输", self)
            newGameButton.setFixedSize(100, 50)
            newGameButton.move(230, 200)
            newGameButton.setFont(font)
            newGameButton.setStyleSheet("background-color:white;color:black;")
            newGameButton.clicked.connect(self.newGameButtonEvent)

        self.setStyleSheet("background-color:rgb(249, 214, 91)")
        self.setWindowTitle("游戏结束")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def callBackButtonEvent(self):
        self.listener.gameOverClickMark = True
        self.callBackSignal.emit()
        self.listener.infoGUI.startGameTimer()
        self.listener.gameLogit.isRunning = True
        self.close()

    def newGameButtonEvent(self):
        self.listener.gameOverClickMark = True
        self.newGameSignal.emit()
        self.listener.infoGUI.startGameTimer()
        self.listener.gameLogit.isRunning = True
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
        wind = GameOverWindow(400, 300, self, GameOver.EQUAL, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Demo()
    sys.exit(app.exec_())
