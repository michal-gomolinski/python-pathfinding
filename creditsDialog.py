from PyQt5.QtWidgets import (QDialog , QDialogButtonBox , QGroupBox , QLabel , QVBoxLayout)

class CreditsDialog(QDialog):
    def __init__(self):
        super(CreditsDialog, self).__init__()
        self.setWindowTitle('Credits')
        dialogLayout = QVBoxLayout()

        boxLayout = QVBoxLayout()
        creditsTextArea = QLabel('Wykonawca: Michał Gomoliński\n Grupa: WCY18IJ7S1')

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.close)
        boxLayout.addWidget(creditsTextArea)

        boxLayout.addWidget(buttonBox)

        creditsBox = QGroupBox("Credits")

        creditsBox.setLayout(boxLayout)
        dialogLayout.addWidget(creditsBox)

        self.setLayout(dialogLayout)