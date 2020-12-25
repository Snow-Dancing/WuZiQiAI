from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget, QPushButton
from PyQt5.QtGui import QPen, QIcon, QPainter, QBrush, QColor, QPalette, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import math
import threading
import time


class ChessBoardGui(QWidget):

    putChessCheck = pyqtSignal()

    def __init__(self, parent, gameLogit):
        super(QWidget, ChessBoardGui).__init__(self, parent)
        self.lineWidth = 3
        self.lineInterval = 50
        self.chessBoardTopLeftPos = (30, 30)
        self.focousRate = 0.2
        self.chessRadius = 25
        self.focusPoint = None
        self.preparedChess = None
        # self.currentPlayer = 0
        # self.chessArray = np.zeros([15, 15], dtype=int)
        self.gameLogit = gameLogit
        self.gameRunning = False
        self.initUI()

    def initUI(self):
        self.resize(800, 800)
        self.setAutoFillBackground(True)
        palette1 = QPalette()
        palette1.setColor(QPalette.Background, QColor(249, 214, 91))
        self.setPalette(palette1)

        # self.setStyleSheet("background-color:rgb(249, 214, 91);")

        # palette1.setBrush(self.backgroundRole(),
        # QtGui.QBrush(QtGui.QPixmap('../../../Document/images/17_big.jpg')))   # 设置背景图片

        # self.setGeometry(500, 200, 800, 800)

        # self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)#无边框，置顶
        # self.setAttribute(Qt.WA_TranslucentBackground)#透明背景色
        # self.show()

    def setGameStatus(self, status):
        self.gameRunning = status

    def mouseReleaseEvent(self, e):
        if not self.gameRunning:
            return
        orderX = (e.x() - self.chessBoardTopLeftPos[0]) / (self.lineWidth + self.lineInterval)
        orderY = (e.y() - self.chessBoardTopLeftPos[1]) / (self.lineWidth + self.lineInterval)
        integerX, integerY = int(orderX + 0.5), int(orderY + 0.5)
        distX = math.fabs(orderX - integerX)
        distY = math.fabs(orderY - integerY)
        if distX > self.focousRate or distY > self.focousRate:
            return
        if not self.gameLogit.isVaildChessPoint(integerX, integerY):
            return
        if not self.focusPoint:
            self.focusPoint = (integerX, integerY)
            self.update()
        elif self.focusPoint[0] != integerX or self.focusPoint[1] != integerY:
            self.focusPoint = (integerX, integerY)
            self.update()
        elif self.gameLogit.chessArray[integerX][integerY] == 0:
            if self.gameLogit.lastPlayer == self.gameLogit.aiPlayer:
                self.preparedChess = integerX, integerY
                self.putChessCheck.emit()


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawChessBoard(qp)
        self.drawFocusPoint(qp)
        self.drawAllChesses(qp)
        qp.end()

    def drawChessBoard(self, qp):
        chessBoardWidth = 14 * (self.lineInterval + self.lineWidth)
        pen = QPen(Qt.black, self.lineWidth, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(15):
            startX = self.chessBoardTopLeftPos[0]
            startY = self.chessBoardTopLeftPos[1] + i * (self.lineWidth + self.lineInterval)
            qp.drawLine(startX, startY, startX + chessBoardWidth, startY)

        for i in range(15):
            startX = self.chessBoardTopLeftPos[0] + i * (self.lineWidth + self.lineInterval)
            startY = self.chessBoardTopLeftPos[1]
            qp.drawLine(startX, startY, startX, startY + chessBoardWidth)

    def drawFocusPoint(self, qp):
        if not self.focusPoint:
            return
        pen = QPen(Qt.red, self.lineWidth, Qt.CustomDashLine)
        pen.setDashPattern([3,11,3,10])
        qp.setPen(pen)
        posX = self.chessBoardTopLeftPos[0] + self.focusPoint[0] * (self.lineWidth + self.lineInterval)
        posY = self.chessBoardTopLeftPos[1] + self.focusPoint[1] * (self.lineWidth + self.lineInterval)
        qp.drawLine(posX - self.chessRadius, posY - self.chessRadius, posX + self.chessRadius, posY - self.chessRadius)
        qp.drawLine(posX - self.chessRadius, posY - self.chessRadius, posX - self.chessRadius, posY + self.chessRadius)
        qp.drawLine(posX - self.chessRadius, posY + self.chessRadius, posX + self.chessRadius, posY + self.chessRadius)
        qp.drawLine(posX + self.chessRadius, posY - self.chessRadius, posX + self.chessRadius, posY + self.chessRadius)

    def drawAllChesses(self, qp):
        with threading.RLock():
            if self.gameLogit.usedChessList:
                for order, (lineX, lineY) in enumerate(self.gameLogit.usedChessList):
                    self.drawOneChess(qp, lineX, lineY, self.gameLogit.chessArray[lineX][lineY], order)

    def drawOneChess(self, qp, lineX, lineY, player, order):
        posX = self.chessBoardTopLeftPos[0] + lineX * (self.lineWidth + self.lineInterval)
        posY = self.chessBoardTopLeftPos[1] + lineY * (self.lineWidth + self.lineInterval)
        color = Qt.black if player == 1 else Qt.white
        pen = QPen(color, 1, Qt.SolidLine)
        brush = QBrush(color, Qt.SolidPattern)
        qp.setBrush(brush)
        qp.setPen(pen)
        qp.drawEllipse(posX - self.chessRadius, posY - self.chessRadius, 2 * self.chessRadius, 2 * self.chessRadius)
        color = Qt.white if player == 1 else Qt.black
        qp.setPen(QColor(color))
        qp.setFont(QFont('微软雅黑', 20))
        qp.drawText(posX - self.chessRadius, posY - self.chessRadius,
                    2 * self.chessRadius, 2 * self.chessRadius,
                    Qt.AlignCenter, str(order + 1))

    def putChessEvent(self, aiChess=None):
        if aiChess:
            x, y = aiChess
            self.focusPoint = aiChess
        else:
            x, y = self.preparedChess
        self.gameLogit.lastPlayer = 1 if self.gameLogit.lastPlayer == -1 else -1
        self.gameLogit.putAChess(self.gameLogit.lastPlayer, x, y)
        self.update()
        return self.gameLogit.gameOver()

    def callBackEvent(self):
        limit = 1 if self.gameLogit.aiPlayer == 1 else 0
        if len(self.gameLogit.usedChessList) > limit:
            self.gameLogit.callbackAChess()
            self.focusPoint = self.gameLogit.lastChess
            self.update()
            time.sleep(0.3)
            if self.gameLogit.usedChessList:
                self.gameLogit.callbackAChess()
                self.focusPoint = self.gameLogit.lastChess
                self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChessBoardGui()
    window.show()
    sys.exit(app.exec_())
