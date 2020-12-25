import sys
import threading
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from infoWidget import InfoWidget
from chessBoardGui import ChessBoardGui
from gameOverWindow import GameOverWindow
from betaGameLogit import GameLogit
from chooseOrderWindow import ChooseOrderWindow
from runningWindow import AiSearchingWindow

class MainWindow(QMainWindow):

    gameOverSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.windowWeight = 1000
        self.windowHeight = 800

        """MainWindow property"""
        self.setFixedSize(self.windowWeight, self.windowHeight)
        self.setWindowIcon(QIcon('figures/gameIcon.png'))
        self.setWindowTitle("五子棋AI")

        self.initUI()
        self.center()
        self.show()

        self.gameOverSignal.connect(self.gameOverEvent)
        self.gameOverClickedMark = False

    def initUI(self):
        self.gameLogit = GameLogit(3)
        self.gameStarted = False
        self.gameRunning = False

        """MainWindow layout and overall widgets"""
        self.mainWidget = QWidget()
        leftWidget = QWidget(self.mainWidget)
        leftWidget.setFixedSize(800,800)
        leftWidget.move(0,0)
        rightWidget = QWidget(self.mainWidget)
        rightWidget.move(800, 0)
        rightWidget.setFixedSize(200, 800)
        self.setCentralWidget(self.mainWidget)
        # self.setObjectName("cw")
        # self.setStyleSheet("#cw{background-color: rgb(255,0,255);}")

        """Chessboard GUI"""
        self.chessBoardGui = ChessBoardGui(leftWidget, self.gameLogit)
        self.chessBoardGui.move(0, 0)
        self.chessBoardGui.putChessCheck.connect(self.putChessEvent)

        """Infomation GUI"""
        self.infoGUI = InfoWidget(200, 800, self.gameLogit, rightWidget)
        self.infoGUI.move(0, 0)
        self.infoGUI.startPauseButtonClicked.connect(self.startPauseEvent)
        self.infoGUI.newGameButtonClicked.connect(self.newGameEvent)
        self.infoGUI.exitGameButtonClicked.connect(self.exitGameEvent)
        self.infoGUI.callBackButtonClicked.connect(self.callBackEvent)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def firstOrderEvent(self):
        self.gameStarted = True
        self.gameLogit.isRunning = True
        self.infoGUI.changeStartButtonInfo()
        self.infoGUI.updatePlayerInfo("先手", "后手")
        self.gameLogit.setAiOrder(-1)
        self.startPauseEvent()

    def secondOrderEvent(self):
        self.gameStarted = True
        self.gameLogit.isRunning = True
        self.infoGUI.changeStartButtonInfo()
        self.infoGUI.updatePlayerInfo("后手", "先手")
        self.gameLogit.setAiOrder(1)
        self.startPauseEvent()
        threading.Thread(target=self.chessBoardGui.putChessEvent, args=((7, 7), )).start()

    def startPauseEvent(self):
        if not self.gameStarted:
            ChooseOrderWindow(400, 300, self.mainWidget, self)
        else:
            if self.gameRunning:
                self.chessBoardGui.setGameStatus(False)
                self.infoGUI.stopGameTimer()
            else:
                self.chessBoardGui.setGameStatus(True)
                self.infoGUI.startGameTimer()
            self.gameRunning = not self.gameRunning

    def callBackEvent(self):
        if self.gameLogit.aiSearching:
            AiSearchingWindow(400, 200, self.mainWidget)
        else:
            threading.Thread(target=self.chessBoardGui.callBackEvent).start()

    def newGameEvent(self):
        self.gameLogit.isRunning = False
        self.initUI()

    def exitGameEvent(self):
        self.gameLogit.isRunning = False
        QtCore.QCoreApplication.instance().quit()

    def gameOverEvent(self):
        self.infoGUI.stopGameTimer()
        self.gameOverClickMark = False
        GameOverWindow(400, 300, self.mainWidget, self.gameLogit.winner, self)
        if not self.gameOverClickMark:
            self.newGameEvent()

    def putChessEvent(self):

        # t1 = threading.Thread(target=self.chessBoardGui.putChessEvent, args=(None, ))
        # t1.start()
        winner = self.chessBoardGui.putChessEvent(aiChess=None)
        # print(self.gameLogit.getChessBoardScore(self.gameLogit.chessArray, -self.gameLogit.lastPlayer))
        if winner:
            self.gameOverSignal.emit()
        else:
            t = threading.Thread(target=self.aiStep)
            t.start()

    def aiStep(self):
        print("AI step")
        self.gameLogit.aiSearching = True
        aiChess = self.gameLogit.getBestPoint()
        winner = self.chessBoardGui.putChessEvent(aiChess)
        self.gameLogit.aiSearching = False
        if winner:
            self.gameOverSignal.emit()


    def closeEvent(self, e):
        self.exitGameEvent()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
