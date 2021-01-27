from PyQt5.QtWidgets import (QMainWindow, QPushButton, QSlider, QLabel)
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QFont,QPen
from PyQt5.QtCore import Qt
import map, math, time, settingsDialog
import threading, creditsDialog



class Window(QMainWindow):
    begIsSet = False
    endIsSet = False
    mouseIsPressed = False
    drawType = 1
    drawTypeFirstX = - 1
    drawTypeFirstY = - 1
    parentTraversable = True

    windowWidth = 1200
    windowHeight = 900

    algorithmType = 0
    heuristicType = 0

    mapWidth = 20
    mapHeight = 20

    buttonRunPause = QPushButton
    buttonDrawType = QPushButton

    isRunning = False
    speed = 0.25

    def __init__(self):
        super().__init__()

        self.mapa = map.Map(self.mapWidth,self.mapHeight)
        self.createUI()
        self.show()



    def createUI(self):
        self.setWindowTitle('A* Pathfinding')
        self.setAutoFillBackground(True)
        self.setFixedSize(self.windowWidth,self.windowHeight)
        self.paintButtons()
        self.paintLabel()

        self.label = QLabel(self)
        self.label.setGeometry(0, 10, self.windowWidth, self.windowHeight / 3 - 10)
        self.label.setText("Pathfinding Project")

        font  = QFont()
        font.setPixelSize(self.windowHeight / 8)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.show()

        self.show()


    def handleAStarButton(self):
        if self.isRunning:
            self.isRunning = False
            self.status.setText("Pathfinding algorithm was paused")
        else:
            self.status.setText("Pathfinding algorithm has started")
            self.isRunning = True
            self.thread = threading.Thread(target=self.aStarFull,args=())
            self.thread.start()
            self.update()



    def handleReset(self):
        self.isRunning = False
        self.status.setText('Map reset \nChoose your start node')
        time.sleep(0.1)
        self.mapa = map.Map(self.mapWidth,self.mapHeight)
        self.begIsSet = False
        self.endIsSet = False
        self.repaint()

    def handlePause(self):
        self.isRunning = False

    def handleStop(self):
        self.status.setText('Pathfinding algorithm stopped \nModify your map or start pathfinding algorithm')
        self.isRunning = False
        time.sleep(0.1)
        self.mapa.resMap()
        self.repaint()

    def handleDrawType(self):
        if self.drawType == 1:
            self.drawType = 2
        else:
            self.drawType = 1

    def changeValue(self, value):
        self.speed = (100 - value) / 200

    def aStarFull(self):
        flaga = 0
        while self.isRunning & (flaga == 0):
            flaga = self.mapa.aStarIter(self.algorithmType)
            time.sleep(self.speed)
            self.update()
            time.sleep(self.speed)
        if flaga < 0:
            self.status.setText("No path found")
        elif flaga > 0:
            self.status.setText('Path found after: ' + str(flaga) + " iterations")
        else:
            print('Paused')
        self.isRunning = False
        self.update()

    def mouseMoveEvent(self, event):
        dimension = self.windowHeight / 3

        rectangleWidth = dimension * 2 / self.mapa.width
        rectangleHeight = dimension * 2 / self.mapa.height

        x = math.floor(event.pos().x() / rectangleWidth)
        y = math.floor((event.pos().y() - dimension) / rectangleHeight)

        if ((y < 0) | (x < 0) | (y > self.mapa.height - 1) | (x > self.mapa.width - 1) | (self.begIsSet == False)
                              | (self.endIsSet == False)):
            return
        elif self.drawType == 1:
            self.mapa.setTraversableFill(x, y,self.parentTraversable)
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            dimension = self.windowHeight / 3

            rectangleWidth = dimension * 2 / self.mapa.width
            rectangleHeight = dimension * 2 / self.mapa.height

            x = math.floor(event.pos().x() / rectangleWidth)
            y = math.floor((event.pos().y() - dimension) / rectangleHeight)

            if (y < 0)| (x < 0)| (y > self.mapa.height - 1) | (x > self.mapa.width - 1):
                return
            elif self.begIsSet == False:
                self.mapa.setBeginning(x,y)
                self.begIsSet = True
                self.status.setText('Choose your destination node')
            elif self.endIsSet == False:
                if self.mapa.setDestination(x, y):
                    self.endIsSet = True
                    self.status.setText('Modify your map or start pathfinding algorithm')
                else:
                    print('To jest poczatek')
            else:
                if(self.drawType == 1):
                    self.parentTraversable = not self.mapa.nodeArray[x][y].isTraversable
                    self.mapa.setTraversableFill(x,y,self.parentTraversable)
                elif(self.drawType == 2):
                    if (self.drawTypeFirstX >= 0) & (self.drawTypeFirstY >= 0):
                        howToSet = self.mapa.nodeArray[self.drawTypeFirstX][self.drawTypeFirstY].isTraversable

                        incrementX = 1
                        incrementY = 1

                        if x > self.drawTypeFirstX:
                            incrementX = -1
                        if y > self.drawTypeFirstY:
                            incrementY = -1

                        for i in range (x, self.drawTypeFirstX + incrementX, incrementX):
                            for j in range(y  , self.drawTypeFirstY + incrementY, incrementY):
                                self.mapa.setTraversableFill(i, j, howToSet)
                        self.drawTypeFirstX = -1
                        self.drawTypeFirstY = -1
                    else:
                        self.mapa.setTraversable(x, y)
                        self.drawTypeFirstX = x
                        self.drawTypeFirstY = y

            self.update()

    def paintLabel(self):
        self.status = QLabel(self)
        if self.begIsSet == False:
            self.status.setText('Choose your start node')

        self.status.setGeometry(int(self.windowHeight / 3 * 2 + 10), int(self.windowHeight / 3  + 98),400,100)
        self.status.show()

    def paintEvent(self, e):
        if self.isRunning:
            self.buttonRunPause.setText('Pause')
        else:
            self.buttonRunPause.setText('Run')

        if self.drawType == 1:
            self.buttonDrawType.setText('Single Draw')
        else:
            self.buttonDrawType.setText('Fill Draw')

        self.paintMap()

    def paintButtons(self):
        dimension = self.windowHeight / 9 * 2

        self.buttonRunPause = QPushButton('Find Path', self)
        self.buttonRunPause.show()
        self.buttonRunPause.clicked.connect(self.handleAStarButton)
        self.buttonRunPause.setToolTip('aStar Pathfind Button')
        self.buttonRunPause.move(self.windowHeight / 3 * 2, self.windowHeight / 3 - 2)
        self.buttonRunPause.setFixedSize(dimension + 2,42)

        self.buttonReset = QPushButton('Reset', self)
        self.buttonReset.show()
        self.buttonReset.setToolTip('Reset Button')
        self.buttonReset.clicked.connect(self.handleReset)
        self.buttonReset.move(self.windowHeight / 3 * 2, self.windowHeight / 3 - 2 +40)
        self.buttonReset.setFixedSize(self.windowHeight / 6 * 2 + 2, 42)

        self.buttonStop = QPushButton('Stop', self)
        self.buttonStop.show()
        self.buttonStop.setToolTip('Stop Button')
        self.buttonStop.clicked.connect(self.handleStop)
        self.buttonStop.move(self.windowHeight / 3 * 2 + self.windowHeight / 6 * 2, self.windowHeight / 3 - 2 +40)
        self.buttonStop.setFixedSize(self.windowHeight / 6 * 2 + 2, 42)

        self.mySlider = QSlider(Qt.Horizontal, self)
        self.mySlider.setGeometry(self.windowHeight / 3 * 2 + 1 +dimension, self.windowHeight / 3,
                             dimension * 2, 40)
        self.mySlider.setToolTip("Modify the speed of Pathfinding algorithm")
        self.mySlider.setValue(50)
        self.mySlider.valueChanged[int].connect(self.changeValue)
        self.mySlider.show()

        # buttonTraversableWeight = QPushButton('Traversable', self)
        # #buttonTraversableWeight.show()
        # buttonTraversableWeight.setToolTip('Choose if you want to make a node untraversable or change '
        #                                    'the weight of the node')
        # buttonTraversableWeight.clicked.connect(self.handleStop)
        # buttonTraversableWeight.move(self.windowHeight / 3 * 2, self.windowHeight / 3 + 40 - 2)
        # buttonTraversableWeight.setFixedSize(dimension + 2, 42)

        self.buttonDrawType = QPushButton('Single Draw', self)
        self.buttonDrawType.show()
        self.buttonDrawType.setToolTip('Choose the draw type')
        self.buttonDrawType.clicked.connect(self.handleDrawType)
        self.buttonDrawType.move(self.windowHeight / 3 * 2, self.windowHeight / 3 + 80 - 2)
        self.buttonDrawType.setFixedSize(dimension * 3 + 2, 42)

        self.openSettings = QPushButton('Settings', self)
        self.openSettings.show()
        self.openSettings.setToolTip('Click to open settings window')
        self.openSettings.clicked.connect(self.handleSetting)
        self.openSettings.move(self.windowHeight / 3 * 2 + 40, self.windowHeight - 150 - 2)
        self.openSettings.setFixedSize(dimension * 3 - 78, 42)

        self.buttonCredits = QPushButton('Credits', self)
        self.buttonCredits.show()
        self.buttonCredits.setToolTip('Click to open credits window')
        self.buttonCredits.clicked.connect(self.handleCredits)
        self.buttonCredits.move(self.windowHeight / 3 * 2 + 40, self.windowHeight - 100 - 2)
        self.buttonCredits.setFixedSize(dimension * 3 - 78, 42)

        self.buttonClose = QPushButton('Close', self)
        self.buttonClose.show()
        self.buttonClose.setToolTip('Close application')
        self.buttonClose.clicked.connect(self.close)
        self.buttonClose.move(self.windowHeight / 3 * 2 + 40, self.windowHeight - 50 - 2)
        self.buttonClose.setFixedSize(dimension * 3 - 78, 42)

    def paintMap(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        dimension = self.windowHeight / 3

        rectangleWidth = dimension * 2 / self.mapa.width
        rectangleHeight = dimension * 2 / self.mapa.height

        for i in range(self.mapa.width):
            for j in range(self.mapa.height):
                node = self.mapa.nodeArray[i][j]

                painter.setBrush(Qt.white)

                if node.isBeginning | node.isDestination:
                    painter.setBrush(Qt.darkYellow)
                elif node.isPath:
                    painter.setBrush(Qt.yellow)
                elif (node.cordX == self.drawTypeFirstX) & (node.cordY == self.drawTypeFirstY):
                    painter.setBrush(Qt.gray)
                elif not node.isTraversable:
                    painter.setBrush(Qt.black)
                elif not self.mapa.isPathFound:
                    if node.isOpen:
                        painter.setBrush(Qt.magenta)
                    elif node.isClosed:
                        painter.setBrush(Qt.red)

                painter.drawRect(i * rectangleWidth, j * rectangleHeight + dimension, rectangleWidth, rectangleHeight)

                if node.isBeginning | node.isDestination:
                    painter.setBrush(Qt.black)
                    painter.drawLine(i * rectangleWidth, j * rectangleHeight + dimension, (i + 1) * rectangleWidth,
                                     (j + 1) * rectangleHeight + dimension)
                    painter.drawLine(i * rectangleWidth, (j + 1) * rectangleHeight + dimension, (i + 1) * rectangleWidth,
                                     j * rectangleHeight + dimension)

                if node.isBeginning:
                    font = QFont()
                    font.setPointSizeF(rectangleWidth/2)
                    painter.setFont(font)
                    painter.drawText(i * rectangleWidth, (j + 1) * rectangleHeight + dimension,'A')
                if node.isDestination:
                    font = QFont()
                    font.setPointSizeF(rectangleWidth/2)
                    painter.setFont(font)
                    painter.drawText(i * rectangleWidth, (j + 1) * rectangleHeight + dimension,'B')

    def handleSetting(self):
        dialog = settingsDialog.Dialog(self)
        dialog.exec_()
        dialog.show()

    def handleCredits(self):
        dialog = creditsDialog.CreditsDialog()
        dialog.exec_()
        dialog.show()
