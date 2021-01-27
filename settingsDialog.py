from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QCheckBox, QMessageBox)
import window
class Dialog(QDialog):

    def __init__(self,mainWindow):
        super(Dialog, self).__init__()

        self.mainWindow = mainWindow

        self.algorithmSettings = QGroupBox("Algorithm Settings")
        self.dimensionSettings = QGroupBox("Map Dimension Settings")
        self.resolutionSettings = QGroupBox("Resolution Settings")

        topLayout = QFormLayout()

        self.algorithmType = QComboBox()
        self.algorithmType.addItem('A*')
        self.algorithmType.addItem('Dijkstra')
        self.algorithmType.setCurrentIndex(self.mainWindow.algorithmType)

        self.heuristicType = QComboBox()
        self.heuristicType.addItem('Euclidean')
        self.heuristicType.addItem('Manhattan')
        self.heuristicType.setCurrentIndex(self.mainWindow.mapa.heuristicType)

        topLayout.addRow("Algorith Type:", self.algorithmType)
        topLayout.addRow("Heuristic Type:", self.heuristicType)

        optionsLayout = QHBoxLayout()

        self.widthSpin = QSpinBox()
        self.widthSpin.setRange(10,100)
        self.widthSpin.setValue(self.mainWindow.mapWidth)

        # self.heightSpin = QSpinBox()
        # self.heightSpin.setRange(10,100)
        # self.heightSpin.setValue(self.mainWindow.mapHeight)

        optionsLayout.addWidget(self.widthSpin)


        #optionsLayout.addWidget(self.heightSpin)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


        self.algorithmSettings.setLayout(topLayout)
        self.dimensionSettings.setLayout(optionsLayout)


        actualLayout = QVBoxLayout()
        actualLayout.addWidget(self.algorithmSettings)
        actualLayout.addWidget(self.dimensionSettings)

        actualLayout.addWidget(buttonBox)

        self.setLayout(actualLayout)

        self.setWindowTitle("Settings")


    def accept(self) -> None:
        self.mainWindow.algorithmType = self.algorithmType.currentIndex()
        self.mainWindow.mapa.heuristicType = self.heuristicType.currentIndex()
        self.mainWindow.mapa.resetH()

        if (self.widthSpin.value() != self.mainWindow.mapWidth):
            self.mainWindow.mapWidth = self.widthSpin.value()
            self.mainWindow.mapHeight = self.widthSpin.value()
            self.mainWindow.handleReset()

        self.close()


