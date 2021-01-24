from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QSlider
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush,QPen
from PyQt5.QtCore import QRectF, Qt
import map, math, time
import threading

from PyQt5 import QtGui


class Window(QMainWindow):
    begIsSet = False
    endIsSet = False

    windowWidth = 800
    windowHeight = 600

    buttonRunPause = QPushButton

    isRunning = False

    def __init__(self):
        super().__init__()

        self.mapa = map.Map(10,10)
        self.show()
        self.createUI()


    def createUI(self):
        self.setWindowTitle('A* Pathfinding')
        self.setFixedSize(self.windowWidth,self.windowHeight)
        self.paintButtons()
        self.show()


    def handleAStarButton(self):
        if self.isRunning:
            self.isRunning = False
        else:
            self.isRunning = True
            self.thread = threading.Thread(target=self.aStarFull,args=())
            self.thread.start()
            self.update()



    def handleReset(self):
        self.isRunning = False
        time.sleep(0.1)
        self.mapa = map.Map(10,10)
        self.begIsSet = False
        self.endIsSet = False
        self.repaint()

    def handlePause(self):
        self.isRunning = False

    def handleStop(self):
        self.isRunning = False
        time.sleep(0.1)
        self.mapa.resMap()
        self.repaint()

    def changeValue(self, value):
        value = math.ceil(2.57 *value)
        print(value)

    def aStarFull(self):
        flaga = True
        while(self.isRunning & flaga):
            flaga = self.mapa.aStarIter()
            time.sleep(0.05)
            self.update()
            time.sleep(0.05)

        print('done')
        self.isRunning = False
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:

            dimention = self.windowHeight / 3

            rectangleWidth = dimention * 2 / self.mapa.width
            rectangleHeight = dimention * 2 / self.mapa.height

            x = math.floor(event.pos().x() / rectangleWidth)
            y = math.floor((event.pos().y() - dimention) / rectangleHeight)

            if (y < 0)| (x < 0)| (y > self.mapa.height - 1) | (x > self.mapa.width - 1):
                print('error')
            elif self.begIsSet == False:
                self.mapa.setBeginning(x,y)
                self.begIsSet = True
            elif self.endIsSet == False:
                if self.mapa.setDestination(x, y):
                    self.endIsSet = True
                else:
                    print('To jest poczatek')
            else:
                self.mapa.setTraversable(x,y)
            self.update()

    def paintEvent(self, e):

        if self.isRunning:
            self.buttonRunPause.setText('Pause')
        else:
            self.buttonRunPause.setText('Run')

        self.paintMap()


    def paintButtons(self):
        dimension = self.windowHeight / 9 * 2

        self.buttonRunPause = QPushButton('Find Path', self)
        self.buttonRunPause.show()
        self.buttonRunPause.clicked.connect(self.handleAStarButton)
        self.buttonRunPause.setToolTip('aStar Pathfind Button')
        self.buttonRunPause.move(self.windowHeight / 3 * 2, self.windowHeight / 3 - 2)
        self.buttonRunPause.setFixedSize(dimension + 2,42)


        buttonReset = QPushButton('Reset', self)
        buttonReset.show()
        buttonReset.setToolTip('Reset Button')
        buttonReset.move(0, 70)
        buttonReset.clicked.connect(self.handleReset)
        buttonReset.move(self.windowHeight / 3 * 2 + dimension, self.windowHeight / 3 - 2)
        buttonReset.setFixedSize(dimension + 2, 42)

        buttonStop = QPushButton('Stop', self)
        buttonStop.show()
        buttonStop.setToolTip('Stop Button')
        buttonStop.move(100, 0)
        buttonStop.clicked.connect(self.handleStop)
        buttonStop.move(self.windowHeight / 3 * 2 + dimension * 2, self.windowHeight / 3 - 2)
        buttonStop.setFixedSize(dimension + 2, 42)

        mySlider = QSlider(Qt.Horizontal, self)
        mySlider.setGeometry(self.windowHeight / 3 * 2 + 1, self.windowHeight / 3 + 40,
                             self.windowHeight / 3 * 2 - 1, 40)
        mySlider.valueChanged[int].connect(self.changeValue)
        mySlider.show()

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