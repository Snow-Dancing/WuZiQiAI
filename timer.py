import time
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLCDNumber, QFrame
from PyQt5.QtCore import QTimer



class GameClock(QWidget):
    def __init__(self, width, height, parent=None):
        super(QWidget, GameTimer).__init__(self, parent)
        self.fixedWidth = width
        self.fixedHeight = height
        self.setFixedSize(self.fixedWidth, self.fixedHeight)
        self.initUI()

    def initUI(self):
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)
        timeNow = time.strftime('%H:%M:%S', time.localtime(time.time()))
        self.lcd.display(timeNow)
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.refresh)
        timer.start()

        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setFixedSize(self.fixedWidth, self.fixedHeight)
        self.lcd.setFrameShape(QFrame.NoFrame)

    def refresh(self):
        timeNow = time.strftime('%H:%M:%S', time.localtime(time.time()))
        self.lcd.display(timeNow)


class GameTimer(QWidget):
    def __init__(self, width, height, parent=None):
        super(QWidget, GameTimer).__init__(self, parent)
        self.fixedWidth = width
        self.fixedHeight = height
        self.setFixedSize(self.fixedWidth, self.fixedHeight)
        self.initUI()

    def initUI(self):
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)
        self.time = 0
        self.lcd.display(self.getTimeStr())

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.refresh)

        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setFixedSize(self.fixedWidth, self.fixedHeight)
        self.lcd.setFrameShape(QFrame.NoFrame)

        # startButton = QPushButton("开始")
        # stopButton = QPushButton("暂停")
        # resetButton = QPushButton("重置")
        #
        # startButton.setFixedSize(128, 50)
        # stopButton.setFixedSize(128,50)
        # resetButton.setFixedSize(128,50)

        # font = QtGui.QFont()
        # font.setFamily('微软雅黑')
        # font.setBold(True)      # 设置加粗类型
        # font.setPointSize(20)   # 设置字体大小
        # font.setWeight(35)      # 设置字体粗细
        #
        # startButton.setFont(font)
        # stopButton.setFont(font)
        # resetButton.setFont(font)
        #
        # startButton.clicked.connect(self.startButtonEvent)
        # stopButton.clicked.connect(self.stopButtonEvent)
        # resetButton.clicked.connect(self.resetButtonEvent)
        #
        # hbl = QHBoxLayout()
        # hbl.addWidget(startButton)
        # hbl.addWidget(stopButton)
        # hbl.addWidget(resetButton)
        #
        #
        # vbl.addWidget(self.lcd)
        # vbl.addLayout(hbl)
        # vbl.setStretchFactor(self.lcd, 1)
        # vbl.setStretchFactor(hbl, 2)
        # self.setLayout(vbl)

        # self.setWindowTitle('计时器')
        # self.show()

    def refresh(self):
        self.time += 1
        self.lcd.display(self.getTimeStr())

    def getTimeStr(self):
        m, s = divmod(self.time, 60)
        h, m = divmod(m, 60)
        return "{:0>2d}:{:0>2d}:{:0>2d}".format(h, m, s)

    def resetTimer(self):
        self.time = 0
        self.timer.stop()
        self.lcd.display(self.getTimeStr())

