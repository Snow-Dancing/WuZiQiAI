import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon

from infoWidget import InfoWidget
from chessBoardGui import ChessBoardGui
from gameOverWindow import GameOverWindow


class MainWindow(QMainWindow):

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


    def initUI(self):
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
        self.chessBoardGui = ChessBoardGui(leftWidget)
        self.chessBoardGui.move(0, 0)
        self.chessBoardGui.gameOver.connect(self.gameOverEvent)

        """Infomation GUI"""
        self.infoGUI = InfoWidget(200, 800, rightWidget)
        self.infoGUI.move(0, 0)
        self.infoGUI.startPauseButtonClicked.connect(self.startPauseEvent)
        self.infoGUI.newGameButtonClicked.connect(self.newGameEvent)
        self.infoGUI.exitGameButtonClicked.connect(self.exitGameEvent)



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startPauseEvent(self):
        if self.gameRunning:
            self.chessBoardGui.setGameStatus(False)
            self.infoGUI.stopGameTimer()
        else:
            self.chessBoardGui.setGameStatus(True)
            self.infoGUI.startGameTimer()
        self.gameRunning = not self.gameRunning

    def newGameEvent(self):
        del self.mainWidget
        self.initUI()

    def exitGameEvent(self):
        self.close()

    def gameOverEvent(self):
        print(111)
        self.infoGUI.stopGameTimer()
        gameOverDialog = GameOverWindow(400, 200, self.mainWidget)
        self.newGameEvent()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
