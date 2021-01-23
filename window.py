from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QPushButton
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush,QPen
from PyQt5.QtCore import QRectF, Qt, pyqtSlot
import map, math, time
import _thread

from PyQt5 import QtGui


class Window(QMainWindow):
    begIsSet = False
    endIsSet = False

    windowWidth = 800
    windowHeight = 600


    flag = False

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


    #@pyqtSlot()
    def handleAStarButton(self):
        time.sleep(1)
        try:
            self.flag = True
            _thread.start_new_thread(self.aStarFull,())
        except:
            print('error')
        self.repaint()

    def handleReset(self):
        time.sleep(0.2)
        self.flag = False
        time.sleep(0.1)
        self.mapa = map.Map(10,10)
        self.begIsSet = False
        self.endIsSet = False
        self.repaint()

    def handlePause(self):
        time.sleep(0.2)
        self.flag = False

    def handleStop(self):
        time.sleep(0.2)
        self.mapa.resMap()
        self.repaint()

    def aStarFull(self):
        flaga = True
        while(self.flag & flaga):
            flaga = self.mapa.aStarIter()
            time.sleep(0.2)
            self.repaint()
            time.sleep(0.2)

        print('done')

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
            self.repaint()

    def paintEvent(self, e):
        self.paintMap()


    def paintButtons(self):
        buttonAStar = QPushButton('Find Path', self)
        buttonAStar.show()
        buttonAStar.setToolTip('aStar Pathfind Button')
        buttonAStar.move(0, 0)
        buttonAStar.clicked.connect(self.handleAStarButton)

        buttonReset = QPushButton('Reset', self)
        buttonReset.show()
        buttonReset.setToolTip('Reset Button')
        buttonReset.move(0, 70)
        buttonReset.clicked.connect(self.handleReset)

        buttonPause = QPushButton('Pause', self)
        buttonPause.show()
        buttonPause.setToolTip('Pause Button')
        buttonPause.move(0, 140)
        buttonPause.clicked.connect(self.handlePause)

        buttonStop = QPushButton('Stop', self)
        buttonStop.show()
        buttonStop.setToolTip('Stop Button')
        buttonStop.move(100, 0)
        buttonStop.clicked.connect(self.handleStop)


    def paintMap(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        dimention = self.windowHeight / 3

        rectangleWidth = dimention * 2 / self.mapa.width
        rectangleHeight = dimention * 2 / self.mapa.height

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





                painter.drawRect(i * rectangleWidth, j * rectangleHeight + dimention, rectangleWidth, rectangleHeight)

                if node.isBeginning | node.isDestination:
                    painter.setBrush(Qt.black)
                    painter.drawLine(i * rectangleWidth, j * rectangleHeight + dimention, (i + 1) * rectangleWidth,
                                     (j + 1) * rectangleHeight + dimention)
                    painter.drawLine(i * rectangleWidth, (j + 1) * rectangleHeight + dimention, (i + 1) * rectangleWidth,
                                     j * rectangleHeight + dimention)

                if node.isBeginning:
                    font = QFont()
                    font.setPointSizeF(rectangleWidth/2)
                    painter.setFont(font)
                    painter.drawText(i * rectangleWidth, (j + 1) * rectangleHeight + dimention,'A')