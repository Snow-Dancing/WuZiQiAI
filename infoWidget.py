from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont
from timer import GameTimer, GameClock
from PyQt5.QtCore import pyqtSignal

class InfoWidget(QWidget):
    startPauseButtonClicked = pyqtSignal()
    newGameButtonClicked = pyqtSignal()
    exitGameButtonClicked = pyqtSignal()
    callBackButtonClicked = pyqtSignal()

    def __init__(self, width, height, gameLogit, parent=None):
        super(QWidget, InfoWidget).__init__(self, parent)
        self.fixedWidth = width
        self.fixedHeight = height
        self.gameRunning = False
        self.gameLogit = gameLogit
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.fixedWidth, self.fixedHeight)
        """Timer label"""
        gameTimerLabel = QLabel("游戏时间:", self)
        gameTimerLabel.move(15, 10)
        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)      # 设置加粗类型
        font.setPointSize(30)   # 设置字体大小
        font.setWeight(35)      # 设置字体粗细
        gameTimerLabel.setFont(font)

        # palette1 = QPalette()
        # palette1.setColor(QPalette.Background, QColor(0, 0, 255))
        # self.setPalette(palette1)
        # self.setAutoFillBackground(True)

        """Timer"""
        self.gameTimer = GameTimer(200, 100, self)
        self.gameTimer.move(0, 50)

        """Player info"""
        self.playerInfoLable = QLabel("玩家 \t{:}\nAI \t{:}".format("", ""), self)
        self.playerInfoLable.setFixedSize(self.fixedWidth, 100)
        self.playerInfoLable.move(0, 140)
        font.setPointSize(25)
        self.playerInfoLable.setFont(font)

        font.setPointSize(30)
        """Start and pause button"""
        self.startPauseButton = QPushButton("开始游戏", self)
        self.startPauseButton.move(0, 250)
        self.startPauseButton.setFixedSize(200, 80)
        self.startPauseButton.setFont(font)
        # self.startPauseButton.setFlat(True)
        self.startPauseButton.setAutoFillBackground(True)
        self.startPauseButton.setStyleSheet("background-color:rgb(0, 205, 0);")
        self.startPauseButton.clicked.connect(self.startPauseButtonClickedEvent)

        """Call back A chess button"""
        self.callBackButton = QPushButton("悔棋", self)
        self.callBackButton.move(0, 350)
        self.callBackButton.setFixedSize(200, 80)
        self.callBackButton.setFont(font)
        # self.startPauseButton.setFlat(True)
        self.callBackButton.setAutoFillBackground(True)
        self.callBackButton.setStyleSheet("background-color:rgb(100, 149, 237);")
        self.callBackButton.clicked.connect(self.callBackButtonClickedEvent)

        """New game button"""
        self.newGameButton = QPushButton("新游戏", self)
        self.newGameButton.move(0, 450)
        self.newGameButton.setFixedSize(200, 80)
        self.newGameButton.setFont(font)
        self.newGameButton.setAutoFillBackground(True)
        self.newGameButton.setStyleSheet("background-color:rgb(200, 87, 18);")
        self.newGameButton.clicked.connect(self.newGameButtonClickedEvent)

        """Exit game button"""
        self.exitGameButton = QPushButton("退出游戏", self)
        self.exitGameButton.move(0, 550)
        self.exitGameButton.setFixedSize(200, 80)
        self.exitGameButton.setFont(font)
        self.exitGameButton.setAutoFillBackground(True)
        self.exitGameButton.setStyleSheet("background-color:rgb(213, 16, 33);")
        self.exitGameButton.clicked.connect(self.exitGameButtonClickedEvent)

        """Clock label"""
        gameTimerLabel = QLabel("当前时钟:", self)
        gameTimerLabel.move(15, 650)
        gameTimerLabel.setFont(font)

        """Clock"""
        clock = GameClock(200, 100, self)
        clock.move(0, 690)

    def updatePlayerInfo(self, s1, s2):
        self.playerInfoLable.setText("玩家:\t{:}\nAI:\t{:}".format(s1, s2))


    def changeStartButtonInfo(self):
        if not self.gameRunning:
            self.gameRunning = True
            self.startPauseButton.setText("暂停游戏")
        else:
            self.gameRunning = False
            self.startPauseButton.setText("继续游戏")

    def startPauseButtonClickedEvent(self):
        if self.gameLogit.isRunning:
            self.changeStartButtonInfo()
            self.startPauseButtonClicked.emit()
        else:
            self.startPauseButtonClicked.emit()

    def callBackButtonClickedEvent(self):
        self.callBackButtonClicked.emit()

    def newGameButtonClickedEvent(self):
        self.newGameButtonClicked.emit()

    def exitGameButtonClickedEvent(self):
        self.exitGameButtonClicked.emit()

    def startGameTimer(self):
        self.gameTimer.timer.start()

    def stopGameTimer(self):
        self.gameTimer.timer.stop()

    def resetGameTimer(self):
        self.gameTimer.resetTimer()
