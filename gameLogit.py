import numpy as np


class GameLogit():
    def __init__(self):
        self.row = 15
        self.column = 15
        self.totalChess = 0
        self.chessArray = np.zeros([self.row, self.column])
        self.lastChessX = -1
        self.lastChessY = -1
        self.lastPlayer = 0
        self.directs = [(1, 0), (0, 1), (1, 1), (1, -1)]
        self.playerDict = {1: 1, -1: 2}

    def putAChess(self, player, x, y):
        if not self.chessArray[x][y]:
            self.chessArray[x][y] = player
            self.lastChessX = x
            self.lastChessY = y
            self.lastPlayer = player
            self.totalChess += 1
            return True
        return False

    def gameOver(self):
        for direct in range(4):
            for chessStringNum in range(5):
                startX = self.lastChessX - chessStringNum * self.directs[direct][0]
                startY = self.lastChessY - chessStringNum * self.directs[direct][1]
                count = 0
                for chessNum in range(5):
                    chessX = startX + chessNum * self.directs[direct][0]
                    chessY = startY + chessNum * self.directs[direct][1]
                    if chessX < 0 or chessX >= self.row or chessY < 0 or chessY >= self.column:
                        break
                    else:
                        if self.chessArray[chessX][chessY] == self.lastPlayer:
                            count += 1
                            if count == 5:
                                return self.playerDict[self.lastPlayer]
        if self.totalChess == self.row * self.column:
            return -1
        return 0
