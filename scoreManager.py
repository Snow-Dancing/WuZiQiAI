
class ScoreManager:
    def __init__(self):
        self.scorePoint = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
            [0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0],
            [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def scoreSleepTwo(self, gameLogit, chessType, nextPlayer):
        if chessType == gameLogit.aiPlayer:
            return 2 if nextPlayer == gameLogit.aiPlayer else 1
        else:
            return -1 if nextPlayer == gameLogit.aiPlayer else -2

    def scoreLiveTwo(self, gameLogit, chessType, nextPlayer):
        if chessType == gameLogit.aiPlayer:
            return 20 if nextPlayer == gameLogit.aiPlayer else 10
        else:
            return -10 if nextPlayer == gameLogit.aiPlayer else -20


    def scoreSleepThree(self, gameLogit, chessType, nextPlayer):
        if chessType == gameLogit.aiPlayer:
            return 200 if nextPlayer == gameLogit.aiPlayer else 100
        else:
            return -100 if nextPlayer == gameLogit.aiPlayer else -200

    def scoreLiveThree(self, gameLogit, chessType, nextPlayer):
        if chessType == gameLogit.aiPlayer:
            return 2000 if nextPlayer == gameLogit.aiPlayer else 1000
        else:
            return -1000 if nextPlayer == gameLogit.aiPlayer else -2000

    def scoreSleepFour(self, gameLogit, chessType, nextPlayer):
        if chessType == gameLogit.aiPlayer:
            return 2000000 if nextPlayer == gameLogit.aiPlayer else 10000
        else:
            return -10000 if nextPlayer == gameLogit.aiPlayer else -2000000

    def scoreLiveFour(self, gameLogit, chessType, nextPlayer):
        if chessType == gameLogit.aiPlayer:
            return 2000000 if nextPlayer == gameLogit.aiPlayer else 100000
        else:
            return -100000 if nextPlayer == gameLogit.aiPlayer else -2000000

    def scoreFiveInLine(self, gameLogit, chessType, nextPlayer):
        if chessType == gameLogit.aiPlayer:
            return 2000000
        else:
            return -2000000






