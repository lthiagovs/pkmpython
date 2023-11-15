import gameObject
def readTile(tile):
    tileR = []
    tileNUM = ""
    for x in tile:
        if x != ',':
            tileNUM += x
        else:
            tileR.append(int(tileNUM))
            tileNUM = ""
    return tileR
# 12,13@12,13@]
def readLine(line):
    lineR = []
    lineADD = ""
    for x in line:
        if x == ']':
            break
        elif x == '@':
            lineR.append(lineADD)
            lineADD = ""
        else:
            lineADD += x
    return lineR
def readMap(mapFile):
    map = open(mapFile, 'r')
    mapR = []
    for lines in map:
        if '$' in lines:
            break
        else:
            line = []
            mapLines = readLine(lines)
            for tile in mapLines:
                line.append(readTile(tile))
            mapR.append(line)

    map.close()
    return mapR
def renderMap(Map, objectData):
    mapObjectList = []
    currentX = 0
    currentY = 0
    for cols in Map:
        for lines in cols:
            for objects in lines:
                nObject = gameObject.GameObject(currentX,currentY,objectData[objects].image,objectData[objects].type)
                nObject.collide = objectData[objects].collide
                mapObjectList.append(nObject)
            currentX+=32
        currentY+=32
        currentX=0
    return mapObjectList