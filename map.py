import node
import time
class Map:
    def __init__(self, width, height):
        self.nodeArray = []
        self.width = width
        self.height = height
        self.beginningNode = None
        self.openNodesList = []
        self.isPathFound = False
        self.itersToComplete = 0

        for j in range(height):
            tempList = []
            for i in range(width):
                tempList.append(node.Node(j, i))
            self.nodeArray.append(tempList)

    def setBeginning(self,x,y):
        self.beginningNode = self.nodeArray[x][y]
        self.openNodesList.append(self.beginningNode)
        self.nodeArray[x][y].isBeginning = True
        self.nodeArray[x][y].gValue = 0

    def resMap(self):
        self.openNodesList = []
        self.isPathFound = False
        self.itersToComplete = 0

        for j in range(self.height):
            for i in range(self.width):
                self.nodeArray[i][j].resNode()
                if self.nodeArray[i][j].isBeginning:
                    self.setBeginning(i,j)
                if self.nodeArray[i][j].isDestination:
                    self.setDestination(i, j)



    def setDestination(self,x,y):
        if self.nodeArray[x][y].isBeginning:
            return False
        self.nodeArray[x][y].isDestination = True

        for j in range(len(self.nodeArray)):
            for i in self.nodeArray[j]:
                i.hEuc(x,y)
        return True

    def setTraversable(self,x,y):
        self.nodeArray[x][y].isTraversable = not self.nodeArray[x][y].isTraversable

    def sortList(self,e):
        return e.fValue

    def aStar(self):
        flag = True
        while(flag):
            time.sleep(0.1)
            flag = self.aStarIter()


    def aStarIter(self):
        self.itersToComplete += 1
        openNodesList = self.openNodesList
        openNodesList.sort(key=self.sortList)

        #activeNode = None
        if len(openNodesList) != 0:
            activeNode = openNodesList.pop(0)
        else:
            print("No path found")
            return False

        if activeNode.isDestination:
            self.isPathFound = True
            self.path(activeNode)
            print('Found after ' + str(self.itersToComplete) + ' iterations')
            return False

        openNodesList = self.checkNeighbor(activeNode, openNodesList)
        self.openNodesList = openNodesList

        return True

    def path(self,node):
        if node.isBeginning:
            return
        x = node.parentX
        y = node.parentY

        if x | y < 0:
            print('No path found')
            return

        self.nodeArray[x][y].isPath = True
        self.path(self.nodeArray[x][y])

    def printMap(self):
        for j in range(self.height):
            for i in range(self.width):
                if self.nodeArray[i][j].isBeginning:
                    print('A',end=' ')
                elif self.nodeArray[i][j].isDestination:
                    print('B',end=' ')
                elif self.nodeArray[i][j].isPath:
                    print('*',end=' ')
                elif self.nodeArray[i][j].isTraversable == False:
                    print('x',end=' ')
                else:
                    print('0',end=' ')
            print()


    def checkNeighbor(self, node , list):

        x = node.cordX
        y = node.cordY
        g = node.gValue + 1

        print(x,end=' ')
        print(y)

        if x != 0:
            currentNode = self.nodeArray[x - 1][y]
            if currentNode.isTraversable & (currentNode.isClosed == False):
                if not (currentNode in list):
                    list.append(currentNode)
                currentNode.checkNode(x,y,g)
        if y != 0:
            currentNode = self.nodeArray[x][y - 1]
            if currentNode.isTraversable & (currentNode.isClosed == False):
                if not (currentNode in list):
                    list.append(currentNode)
                currentNode.checkNode(x,y,g)
        if x != self.width - 1:
            currentNode = self.nodeArray[x + 1][y]
            if currentNode.isTraversable & (currentNode.isClosed == False):
                if not (currentNode in list):
                    list.append(currentNode)
                currentNode.checkNode(x,y,g)
        if y != self.height - 1:
            currentNode = self.nodeArray[x][y + 1]
            if currentNode.isTraversable & (currentNode.isClosed == False):
                if not(currentNode in list):
                    list.append(currentNode)
                currentNode.checkNode(x,y,g)
        node.isOpen = False
        node.isClosed = True
        return list