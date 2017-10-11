class SaveGame ():

    def __init__(self,name, wins, losses):
        self.__name = name
        self.__wins = wins
        self.__losses = losses

    def changeWins(newWins):
        self.__wins = self.__wins + newWins

    def changeLosses(newLosses):
        self.__losses = self.__losses + newLosses

    def __str__ (self):

        csvStr = self.__name + ',' + str(self.__wins) + ',' + str(self.__losses)

        return csvStr
