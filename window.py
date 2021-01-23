from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QPushButton
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush,QPen
from PyQt5.QtCore import QRectF, Qt, pyqtSlot
import map, math

from PyQt5 import QtGui


class Window(QMainWindow):
    begIsSet = False
    endIsSet = False

    def __init__(self, mapa: map.Map):
        super().__init__()

        self.mapa = map.Map(10,10)
        self.show()
        self.createUI()




    def createUI(self):
        self.setWindowTitle('A* Pathfinding')
        self.setFixedSize(800,600)
        self.paintButtons()


        self.show()


    @pyqtSlot()
    def handleAStarButton(self):
        self.mapa.aStar()
        self.repaint()

    def handleReset(self):
        self.mapa = map.Map(10,10)
        self.begIsSet = False
        self.endIsSet = False
        self.repaint()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:

            rectangleWidth = 400 / self.mapa.width
            rectangleHeight = 400 / self.mapa.height

            x = math.floor(event.pos().x() / rectangleWidth)
            y = math.floor((event.pos().y() - 200) / rectangleHeight)

            print(x)
            print(y)

            if (y < 0)| (x < 0)| (y > self.mapa.height - 1) | (x > self.mapa.width - 1):
                print('error')
            elif self.begIsSet == False:
                self.mapa.setBeginning(x,y)
                self.begIsSet = True
            elif self.endIsSet == False:
                self.mapa.setDestination(x, y)
                self.endIsSet = True
            else:
                self.mapa.setTraversable(x,y)
            self.repaint()

    def paintEvent(self, e):
        self.paintMap()


    def paintButtons(self):
        buttonAStar = QPushButton('Find Path', self)
        buttonAStar.show()
        buttonAStar.setToolTip('aStar Pathfind Button')
        buttonAStar.move(100, 70)
        buttonAStar.clicked.connect(self.handleAStarButton)

        buttonReset = QPushButton('Reset', self)
        buttonReset.show()
        buttonReset.setToolTip('Reset Button')
        buttonReset.move(100, 140)
        buttonReset.clicked.connect(self.handleReset)



    def paintMap(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        rectangleWidth = 400 / self.mapa.width
        rectangleHeight = 400 / self.mapa.height

        for i in range(self.mapa.width):
            for j in range(self.mapa.height):
                node = self.mapa.nodeArray[i][j]

                if node.isBeginning | node.isDestination:
                    painter.setBrush(Qt.green)
                elif node.isPath:
                    painter.setBrush(Qt.yellow)
                elif node.isTraversable == False:
                    painter.setBrush(Qt.red)
                else:
                    painter.setBrush(Qt.white)

                painter.drawRect(i * rectangleWidth, j * rectangleHeight + 200, rectangleWidth, rectangleHeight)
