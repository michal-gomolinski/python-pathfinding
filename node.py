import math

class Node:
    isOpen = False
    isClosed = False
    isBeginning = False
    isDestination = False
    isTraversable = True
    isPath = False

    weight = 1

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

    def hMan(self,xDestination , yDestination):
        distance = abs(xDestination - self.cordX) + abs(yDestination - self.cordY)
        self.hValue = distance
        self.resetF()

    def resNode(self):
        self.isOpen = False
        self.isClosed = False
        self.isPath = False

        self.gValue = 100000
        self.hValue = 0

        self.parentX = -1
        self.parentY = -1


    def resetF(self):
        self.fValue = self.gValue + self.hValue

    def printCoords(self):
        print(self.cordX, end=' ')
        print(self.cordY)

    def checkNode(self, node):
        x = node.cordX
        y = node.cordY
        g = node.gValue + self.weight

        if self.isClosed | (self.isTraversable == False) :
            return

        if self.gValue > g:
            self.gValue = g
            self.parentX = x
            self.parentY = y
            self.resetF()
            self.isOpen = True