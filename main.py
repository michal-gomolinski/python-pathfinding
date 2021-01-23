import window, map, sys
from PyQt5.QtWidgets import QApplication


#example maps:

firstMap = map.Map(10, 10)
firstMap.setBeginning(0, 0)
firstMap.setDestination(5, 9)

firstMap.setTraversable(0, 4)
firstMap.setTraversable(1, 4)
firstMap.setTraversable(2, 4)

firstMap.aStar()

firstMap.printMap()

app = QApplication(sys.argv)
window = window.Window(firstMap)
sys.exit(app.exec_())