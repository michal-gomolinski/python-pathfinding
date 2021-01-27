import window, sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
window = window.Window()
sys.exit(app.exec_())