class SaveGame ():

    def __init__(self,name, wins, losses):
        self.__name = name
        self.__wins = wins
        self.__losses = losses

    def changeName(newName):
        self.__name= newName

    def changeWins(self):
        self.__wins = self.__wins + 1

    def changeLosses(self):
        self.__losses = self.__losses + 1

    def currentScore(self):

        score = "you have won " + str(self.__wins) + " games, and lost " + str(self.__losses)

        return score

    def __str__ (self):

        csvStr = self.__name + ',' + str(self.__wins) + ',' + str(self.__losses)

        return csvStr
