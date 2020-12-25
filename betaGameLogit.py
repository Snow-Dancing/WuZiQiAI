import sys
import math
from enum import Enum
from scoreManager import ScoreManager


class AlphaBetaLayer(Enum):
    ALPHA = 1
    BETA = 2


class GameOver(Enum):
    PLAYER_WIN = 1
    AI_WIN = 2
    EQUAL = 3


class GameLogit(object):

    """The logit of wuziqi game"""

    def __init__(self, alphaBetaLayer=3):
        self.row = 15
        self.column = 15
        self.chessArray = [[0 for i in range(self.row)] for j in range(self.column)]
        self.usedChessList = []
        self.adjacentChessList = []
        self.preAdjacentChessList = []
        self.currentFiveTupleScore = {fiveTuple: 0 for fiveTuple in self.fiveTupleGenerator()}
        self.callBackCount = {(i, j): 0 for i in range(self.row) for j in range(self.column)}
        self.bestFutureChessScore = None
        self.tempFutureChessScore = None
        self.scoreDict = None
        self.lastChess = None
        self.lastPlayer = -1
        self.directs = [(1, 0), (0, 1), (1, 1), (1, -1)]
        self.aiPlayer = -1
        self.playerDict = {self.aiPlayer: GameOver.AI_WIN, -self.aiPlayer: GameOver.PLAYER_WIN}
        self.isRunning = False
        self.aiSearching = False
        self.scoreManager = ScoreManager()
        self.winner = None
        self.aiChessStack = []
        self.adjacentDepth = 1
        self.alphaBetaLayer = alphaBetaLayer
        self.searchedChess = []
        # self.debugMark1 = False
        # self.debugMark2 = False
        # self.debugMark3 = False

    def setAiOrder(self, order):
        self.aiPlayer = order
        self.playerDict = {self.aiPlayer: GameOver.AI_WIN, -self.aiPlayer: GameOver.PLAYER_WIN}

    def quickFind(self):
        for chess in self.adjacentChessList:
            if self.chessArray[chess[0]][chess[1]] == 0:
                self.putAChess(self.aiPlayer, chess[0], chess[1], aiSimulated=True)
                self.aiChessStack.append(chess)
                winner = self.gameOver(aiChess=chess)
                self.aiChessStack.pop()
                self.callbackAChess(aiChess=chess)
                if winner == GameOver.AI_WIN:
                    return chess
        return None

    def getBestPoint(self):
        bestChess = self.quickFind()
        if bestChess:
            return bestChess

        centerChess = self.lastChess
        # if self.searchedChess:
        #     centerChess = self.searchedChess.pop()
        #     if self.searchedChess:
        #         centerChess = self.searchedChess.pop()
        if self.bestFutureChessScore:
            # print(self.lastChess)
            centerChess = self.bestFutureChessScore[self.lastChess]
            if not centerChess:
                centerChess = self.lastChess

        cmp = lambda chess: math.fabs(chess[0] - centerChess[0]) + math.fabs(chess[1] - centerChess[1])
        # cmp = lambda chess: self.searchScoreCache[chess]
        self.adjacentChessList = sorted(self.preAdjacentChessList, key=cmp)
        if self.aiChessStack:
            raise Exception("aiChessStackError!")
        maxScore = 100000000
        print("Total number of searching chesses: %d" % len(self.adjacentChessList))

        score, self.searchedChess = self.alphaBetaCut(layer=self.alphaBetaLayer,
                                     alphaBetaType=AlphaBetaLayer.ALPHA,
                                     nextPlayer=-self.lastPlayer,
                                     alphaBetaScore=maxScore)
        if not self.searchedChess:
            raise Exception("Not find best point!")
        return self.searchedChess[-1]

    def alphaBetaCut(self, layer, alphaBetaType, nextPlayer, alphaBetaScore):
        # print((layer, alphaBetaType, alphaBetaScore))
        if layer < 0:
            raise Exception("Error when recursion!")
        if layer == 0:
            return self.updateChessBoardScore(self.aiChessStack, nextPlayer, aiChess=True), []

        bestScore = 100000000 if alphaBetaType == AlphaBetaLayer.BETA else -100000000
        bestChessList = None

        for chessIndex in range(len(self.adjacentChessList)):
            chessX, chessY = self.adjacentChessList[chessIndex]
            if layer == self.alphaBetaLayer:
                self.tempFutureChessScore = {(i, j): None for i in range(self.row) for j in range(self.column)}
                print("(%d, %d): %d" % (chessX, chessY, bestScore))
            # if chessX == 7 and chessY == 6 and layer == 3:
            #     self.debugMark1 = True
            #     i = 1
            # if self.debugMark1 and chessX == 7 and chessY == 12 and layer == 2:
            #     self.debugMark2 = True
            #     i = 1
            # if self.debugMark1 and self.debugMark2 and chessX == 7 and chessY == 8 and layer == 1:
            #     self.debugMark3 = True

            if self.chessArray[chessX][chessY]:
                continue
            if alphaBetaType == AlphaBetaLayer.ALPHA:
                if bestScore >= alphaBetaScore:
                    return bestScore, bestChessList
            elif alphaBetaType == AlphaBetaLayer.BETA:
                if bestScore <= alphaBetaScore:
                    return bestScore, bestChessList

            self.putAChess(nextPlayer, chessX, chessY, aiSimulated=True)
            self.aiChessStack.append((chessX, chessY))

            simuWinner = self.gameOver((chessX, chessY))
            if simuWinner == GameOver.AI_WIN or simuWinner == GameOver.PLAYER_WIN:
                chessList = []
                if alphaBetaType == AlphaBetaLayer.ALPHA:
                    chessList.append((chessX, chessY))
                score = 2000000 if simuWinner == GameOver.AI_WIN else -2000000
                self.aiChessStack.pop()
                self.callbackAChess(aiChess=(chessX, chessY))
                return score, chessList
            else:
                nextLayer = AlphaBetaLayer.ALPHA if alphaBetaType == AlphaBetaLayer.BETA else AlphaBetaLayer.BETA
                score, chessList= self.alphaBetaCut(layer-1, nextLayer, -nextPlayer, bestScore)
                # print("(%d, %d): %d alphaBetaScore: %d" % (chessX, chessY, score, bestScore))
                if alphaBetaType == AlphaBetaLayer.ALPHA:
                    chessList.append((chessX, chessY))

            if layer == self.alphaBetaLayer - 1:
                self.tempFutureChessScore[(chessX, chessY)] = chessList[-1]
            if alphaBetaType == AlphaBetaLayer.ALPHA and score > bestScore:
                bestScore = score
                bestChessList = chessList
                if layer == self.alphaBetaLayer:
                    # tempChess = self.tempFutureChessScore[(8, 8)]
                    self.bestFutureChessScore = self.tempFutureChessScore.copy()
            elif alphaBetaType == AlphaBetaLayer.BETA and score < bestScore:
                bestScore = score
                bestChessList = chessList

            self.aiChessStack.pop()
            self.callbackAChess(aiChess=(chessX, chessY))

        return bestScore, bestChessList

    def putAChess(self, player, x, y, aiSimulated=False):
        if not self.chessArray[x][y]:
            self.chessArray[x][y] = player
            if not aiSimulated:
                self.lastChess = x, y
                self.lastPlayer = player
                self.usedChessList.append((x, y))
                self.updateChessBoardScore([(x, y)], -player)
                # if self.chessArray[x][y] == -self.aiPlayer and self.bestFutureChessScore:
                #     print("###############################")
                #     print((x, y))
                #     print(self.bestFutureChessScore[(x, y)])
                #     print("###############################")


            count = 0
            for i in range(x - self.adjacentDepth, x + self.adjacentDepth + 1):
                for j in range(y - self.adjacentDepth, y + self.adjacentDepth + 1):
                    if self.isVaildChessPoint(i, j) and not self.chessArray[i][j]:
                        if (i, j) not in self.adjacentChessList:
                            self.adjacentChessList.append((i, j))
                            self.preAdjacentChessList.append((i, j))
                            count += 1
            self.callBackCount[(x, y)] = count
            return True
        else:
            raise Exception("There is already a chess at (%d, %d)" % (x, y))


    def callbackAChess(self, aiChess=None):
        if aiChess:
            x, y = aiChess
        else:
            x, y = self.usedChessList.pop()
        chessType = self.chessArray[x][y]
        if chessType:
            self.chessArray[x][y] = 0
            for i in range(self.callBackCount[(x, y)]):
                self.adjacentChessList.pop()
                self.preAdjacentChessList.pop()
            if not aiChess:
                if self.usedChessList:
                    self.lastChess = self.usedChessList[-1]
                else:
                    self.lastChess = None
                self.lastPlayer = -self.lastPlayer
        else:
            raise Exception("There is no chess to call back at (%d, %d)" % (x, y))

    def isVaildChessPoint(self, x, y):
        if x < 0 or x > 14 or y < 0 or y > 14:
            return False
        return True

    def gameOver(self, aiChess=None):
        if aiChess:
            lastChessX, lastChessY = aiChess
        else:
            lastChessX, lastChessY = self.lastChess
        chessType = self.chessArray[lastChessX][lastChessY]
        for direct in range(4):
            for chessStringNum in range(5):
                startX = lastChessX - chessStringNum * self.directs[direct][0]
                startY = lastChessY - chessStringNum * self.directs[direct][1]
                count = 0
                for chessNum in range(5):
                    chessX = startX + chessNum * self.directs[direct][0]
                    chessY = startY + chessNum * self.directs[direct][1]
                    if chessX < 0 or chessX >= self.row or chessY < 0 or chessY >= self.column:
                        break
                    else:
                        if self.chessArray[chessX][chessY] == chessType:
                            count += 1
                            if count == 5:
                                if not aiChess:
                                    self.isRunning = False
                                self.winner = self.playerDict[chessType]
                                return self.winner
        if len(self.chessArray) == self.row * self.column:
            if not aiChess:
                self.isRunning = False
            self.winner = GameOver.EQUAL
            return self.winner
        return 0

    def fiveTupleGenerator(self):
        for i in range(self.row):
            for j in range(2, self.column - 2):
                fiveChessList = []
                for chess in range(5):
                    fiveChessList.append((i, j - 2 + chess))
                yield tuple(fiveChessList)

        for i in range(2, self.row - 2):
            for j in range(self.column):
                fiveChessList = []
                for chess in range(5):
                    fiveChessList.append((i - 2 + chess, j))
                yield tuple(fiveChessList)

        for i in range(2, self.row - 2):
            for j in range(2, self.column - 2):
                fiveChessList = []
                for chess in range(5):
                    fiveChessList.append((i - 2 + chess, j - 2 + chess))
                yield tuple(fiveChessList)
                fiveChessList = []
                for chess in range(5):
                    fiveChessList.append((i - 2 + chess, j + 2 - chess))
                yield tuple(fiveChessList)

    def evalFiveChessTuple(self, fiveChessTuple, nextPlayer):
        sevenChesses = self.getSevenChess(fiveChessTuple)
        chessType, sameChessCount = self.getSameChessCount(sevenChesses)

        if sameChessCount == 2:
            # TODO liveTwo, sleepTwo
            if not sevenChesses[1] and not sevenChesses[6]:
                return self.scoreManager.scoreLiveTwo(self, chessType, nextPlayer)
            elif sevenChesses[0] or sevenChesses[5] and sevenChesses[0] != chessType:
                return self.scoreManager.scoreSleepTwo(self, chessType, nextPlayer)

        elif sameChessCount == 3:
            # TODO liveThree, sleepThree
            if not sevenChesses[1] and not sevenChesses[6]:
                return self.scoreManager.scoreLiveThree(self, chessType, nextPlayer)
            elif sevenChesses[0] or sevenChesses[5] and sevenChesses[0] != chessType:
                return self.scoreManager.scoreSleepThree(self, chessType, nextPlayer)

        elif sameChessCount == 4:
            # TODO liveFour, sleepFour
            # 此处指定活四必须满足左侧第一个棋子是空,否则会造成重复判断
            if not sevenChesses[1] and not sevenChesses[6]:
                return self.scoreManager.scoreLiveFour(self, chessType, nextPlayer)
            elif sevenChesses[0] or sevenChesses[5] and sevenChesses[0] != chessType:
                return self.scoreManager.scoreSleepFour(self, chessType, nextPlayer)

        elif sameChessCount == 5:
            # TODO five
            return self.scoreManager.scoreFiveInLine(self, chessType, nextPlayer)
        return 0

    def getSevenChess(self, fiveChessTuple):
        first, second, third, forth, fifth = fiveChessTuple
        zero = 2 * first[0] - second[0], 2 * first[1] - second[1]
        sixth = 2 * fifth[0] - forth[0], 2 * fifth[1] - forth[1]

        zero = self.chessArray[zero[0]][zero[1]] if self.isVaildChessPoint(*zero) else 4
        sixth = self.chessArray[sixth[0]][sixth[1]] if self.isVaildChessPoint(*sixth) else 4

        first = self.chessArray[first[0]][first[1]]
        second = self.chessArray[second[0]][second[1]]
        third = self.chessArray[third[0]][third[1]]
        forth = self.chessArray[forth[0]][forth[1]]
        fifth = self.chessArray[fifth[0]][fifth[1]]
        return zero, first, second, third, forth, fifth, sixth

    def getSameChessCount(self, sevenChesses):
        zeroChessCount = 0
        notZeroChessCount = 0
        for i in range(1, 6):
            if sevenChesses[i] != 0:
                notZeroChessCount += sevenChesses[i]
            else:
                zeroChessCount += 1
        chessType = 1
        if notZeroChessCount < 0:
            chessType = -1
            notZeroChessCount = -notZeroChessCount
        if zeroChessCount + notZeroChessCount == 5:
            return chessType, notZeroChessCount
        else:
            return chessType, 0

    def updateChessBoardScore(self, chessList, nextPlayer, aiChess=False):
        score = 0
        for fiveChessTuple in self.getRelatedFiveTupleSet(chessList):
            if not self.isRunning:
                sys.exit(0)
            # if self.lastChessX == 10 and self.lastChessY == 2:
            #     i = 1
            fiveTupleScore = self.evalFiveChessTuple(fiveChessTuple, nextPlayer)
            if aiChess:
                score += fiveTupleScore - self.currentFiveTupleScore[fiveChessTuple]
                # if self.debugMark1 and self.debugMark2 and self.debugMark3 and score == -2000282:
                #     print(self.currentFiveTupleScore[fiveChessTuple])
                #     i = 1
            else:
                # if fiveChessTuple == ((6, 6), (7, 5), (8, 4), (9, 3), (10, 2)) and fiveTupleScore == 2000000:
                #     i = 1
                self.currentFiveTupleScore[fiveChessTuple] = fiveTupleScore

        return score

    def getRelatedFiveTupleSet(self, chessList):
        relatedFiveTupleSet = set()
        for (centerChessX, centerChessY) in chessList:
            for direct in range(4):
                for chessStringNum in range(-1, 6):
                    startX = centerChessX - chessStringNum * self.directs[direct][0]
                    startY = centerChessY - chessStringNum * self.directs[direct][1]
                    fiveTuple = []
                    for chessNum in range(5):
                        chessX = startX + chessNum * self.directs[direct][0]
                        chessY = startY + chessNum * self.directs[direct][1]
                        if not self.isVaildChessPoint(chessX, chessY):
                            break
                        else:
                            fiveTuple.append((chessX, chessY))
                    if len(fiveTuple) == 5:
                        relatedFiveTupleSet.add(tuple(fiveTuple))
        return relatedFiveTupleSet


if __name__ == '__main__':
    pass
    # gl = GameLogit()
    # gl.setAiOrder(1)
    # gl.isRunning = True
    # gl.putAChess(1, 7, 7)
    # gl.putAChess(-1, 8, 8)
    # gl.putAChess(1, 6, 8)
    # gl.putAChess(-1, 8, 6)
    # gl.putAChess(1, 5, 9)
    # gl.putAChess(-1, 8, 7)
    # gl.putAChess(1, 8, 9)
    # gl.putAChess(-1, 7, 9)
    # gl.putAChess(1, 6, 10)
    # gl.putAChess(-1, 6, 9)
    # gl.putAChess(1, 4, 8)
    # gl.putAChess(-1, 7, 11)
    # gl.putAChess(1, 3, 7)
    # gl.putAChess(-1, 2, 6)
    # gl.putAChess(1, 4, 10)
    # gl.putAChess(-1, 3, 11)
    # gl.putAChess(1, 5, 10)
    # gl.putAChess(-1, 7, 10)
    # gl.searchedChess = [(5, 10)]
    # print(gl.getBestPoint())

