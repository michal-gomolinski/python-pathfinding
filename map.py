import node

class Map:

    def __init__(self, width, height):
        self.nodeArray = []
        self.width = width
        self.height = height

        for j in range(height):
            tempList = []
            for i in range(width):
                tempList.append(node.Node(j, i))
            self.nodeArray.append(tempList)

    def setBeginning(self,x,y):
        self.nodeArray[x][y].isBeginning = True
        self.nodeArray[x][y].gValue = 0

    def setDestination(self,x,y):
        self.nodeArray[x][y].isDestination = True

        for j in range(len(self.nodeArray)):
            for i in self.nodeArray[j]:
                i.hEuc(x,y)

    def setTraversable(self,x,y):
        self.nodeArray[x][y].isTraversable = False

    def sortList(self,e):
        return e.gValue

    def aStar(self):
        openNodesList = []

        for j in range(len(self.nodeArray)):
            for i in self.nodeArray[j]:
                if i.isTraversable:
                    openNodesList.append(i)

        openNodesList.sort(key=self.sortList)

        while(True):
            openNodesList.sort(key=self.sortList)
            activeNode = openNodesList.pop(0)

            if activeNode.isDestination:
                self.path(activeNode)
                return

            self.checkNeighbor(activeNode)

    def path(self,node):
        if node.isBeginning:
            return
        x = node.parentX
        y = node.parentY

        self.nodeArray[x][y].isPath = True
        #print(x, end='')
        #print(y)

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


    def checkNeighbor(self, node):

        x = node.cordX
        y = node.cordY
        g = node.gValue + 1

        if x != 0:
            self.nodeArray[x - 1][y].checkNode(x,y,g)
        if y != 0:
            self.nodeArray[x][y - 1].checkNode(x,y,g)
        if x != self.width - 1:
            self.nodeArray[x + 1][y].checkNode(x,y,g)
        if y != self.height - 1:
            self.nodeArray[x][y + 1].checkNode(x,y,g)

        node.isOpen = False