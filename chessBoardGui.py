from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget, QPushButton
from PyQt5.QtGui import QPen, QIcon, QPainter, QBrush, QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import math
from gameLogit import GameLogit


class ChessBoardGui(QWidget):
    gameOver = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, ChessBoardGui).__init__(self, parent)
        self.lineWidth = 3
        self.lineInterval = 50
        self.chessBoardTopLeftPos = (30, 30)
        self.focousRate = 0.2
        self.chessRadius = 25
        self.focusPoint = None
        self.chessList = []
        # self.currentPlayer = 0
        # self.chessArray = np.zeros([15, 15], dtype=int)
        self.gameLogit = GameLogit()
        self.gamaRunning = False
        self.winner = 0
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
        self.gamaRunning = status

    def mouseReleaseEvent(self, e):
        if not self.gamaRunning:
            return
        orderX = (e.x() - self.chessBoardTopLeftPos[0]) / (self.lineWidth + self.lineInterval)
        orderY = (e.y() - self.chessBoardTopLeftPos[1]) / (self.lineWidth + self.lineInterval)
        integerX, integerY = int(orderX + 0.5), int(orderY + 0.5)
        distX = math.fabs(orderX - integerX)
        distY = math.fabs(orderY - integerY)
        if distX > self.focousRate or distY > self.focousRate:
            return
        if integerX < 0 or integerX > 14 or integerY < 0 or integerY > 14:
            return
        if not self.focusPoint:
            self.focusPoint = (integerX, integerY)
            self.update()
        elif self.focusPoint[0] != integerX or self.focusPoint[1] != integerY:
            self.focusPoint = (integerX, integerY)
            self.update()
        elif self.gameLogit.chessArray[integerX][integerY] == 0:
            self.chessList.append((integerX, integerY))
            self.gameLogit.lastPlayer = -1 if self.gameLogit.lastPlayer == 1 else 1
            self.gameLogit.putAChess(self.gameLogit.lastPlayer, integerX, integerY)
            self.update()
            self.gameOverCheck(self.gameLogit.gameOver())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawChessBoard(qp)
        self.drawFocusPoint(qp)
        self.drawAllChessed(qp)
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

    def drawAllChessed(self, qp):
        if self.chessList:
            for lineX, lineY in self.chessList:
                self.drawOneChess(qp, lineX, lineY, self.gameLogit.chessArray[lineX][lineY])

    def drawOneChess(self, qp, lineX, lineY, player):
        posX = self.chessBoardTopLeftPos[0] + lineX * (self.lineWidth + self.lineInterval)
        posY = self.chessBoardTopLeftPos[1] + lineY * (self.lineWidth + self.lineInterval)
        if player == 1:
            color = Qt.black
        else:
            color = Qt.white
        pen = QPen(color, 1, Qt.SolidLine)
        brush = QBrush(color, Qt.SolidPattern)
        qp.setBrush(brush)
        qp.setPen(pen)
        qp.drawEllipse(posX - self.chessRadius, posY - self.chessRadius, 2 * self.chessRadius, 2 * self.chessRadius)

    def gameOverCheck(self, winner):
        if winner:
            self.gameOver.emit()
            self.winner = winner


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChessBoardGui()
    window.show()
    sys.exit(app.exec_())
