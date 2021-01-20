import math

class Node:
    isOpen = True
    isBeginning = False
    isDestination = False
    isTraversable = True
    isPath = False

    gValue = 100000
    hValue = 0

    parentX = -1
    parentY = -1

    def __init__(self, xCord, yCord):
        self.cordX = xCord
        self.cordY = yCord
        self.fValue = self.gValue + self.hValue

#Funkcja obliczająca odległość euklidesową do punktu końcowego
    def hEuc(self,xDestination , yDestination):
        distance = math.sqrt(pow(xDestination - self.cordX, 2) + pow(yDestination - self.cordY, 2))
        distance = round(distance,3)
        self.hValue = distance
        self.resetF()


    def resetF(self):
        self.fValue = self.gValue + self.hValue

    def printCoords(self):
        print(self.cordX, end=' ')
        print(self.cordY)

    def checkNode(self, x, y, g):
        if self.isOpen == False | self.isTraversable == False:
            return

        if self.fValue > g + self.hValue:
            self.gValue = g
            self.parentX = x
            self.parentY = y
            self.resetF()

