import map

#example maps:

firstMap = map.Map(10, 10)
firstMap.setBeginning(0, 0)
firstMap.setDestination(0, 9)

firstMap.setTraversable(0, 4)
firstMap.setTraversable(1, 4)
firstMap.setTraversable(2, 4)


firstMap.aStar()

firstMap.printMap()

print()

secondMap = map.Map(10,10)
secondMap.setBeginning(3,2)
secondMap.setDestination(6,6)

for i in range(1,9):
    secondMap.setTraversable(i,3)
for i in range(1,7):
    secondMap.setTraversable(i,5)
secondMap.setTraversable(7,6)
for i in range(0,5):
    secondMap.setTraversable(i, 7)
secondMap.setTraversable(7,7)

secondMap.aStar()

secondMap.printMap()

print()

thirdMap = map.Map(10,10)
thirdMap.setBeginning(3,2)
thirdMap.setDestination(6,6)

for i in range(1,9):
    thirdMap.setTraversable(i,3)
for i in range(0,7):
    thirdMap.setTraversable(i,5)
thirdMap.setTraversable(7,6)
for i in range(0,5):
    thirdMap.setTraversable(i, 7)
thirdMap.setTraversable(7,7)

thirdMap.aStar()

thirdMap.printMap()