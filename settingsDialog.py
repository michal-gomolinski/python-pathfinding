from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QCheckBox, )

class Dialog(QDialog):

    def __init__(self,mainWindow):
        super(Dialog, self).__init__()

        self.algorithSettings = QGroupBox("Algorith Settings")
        self.dimensionSettings = QGroupBox("Map Dimension Settings")

        topLayout = QFormLayout()

        topLayout.addRow("Algorith Type:", QComboBox())
        topLayout.addRow("Heuristic Type:", QComboBox())

        optionsLayout = QHBoxLayout()

        optionsLayout.addWidget(QSpinBox())
        optionsLayout.addWidget(QSpinBox())

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)




        self.algorithSettings.setLayout(topLayout)
        self.dimensionSettings.setLayout(optionsLayout)

        actualLayout = QVBoxLayout()
        actualLayout.addWidget(self.algorithSettings)
        actualLayout.addWidget(self.dimensionSettings)
        actualLayout.addWidget(buttonBox)

        self.setLayout(actualLayout)

        self.setWindowTitle("Settings")




