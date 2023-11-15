#Globals

#FORMULA FOR PRECISE POSITION = POSX-CAMERAX

tileSize = 32
screenSizeX = 800
screenSizeY = 600

minBorderX = 12*tileSize
minBorderY = 9*tileSize

playerStartPosX = 11
playerStartPosY = 8

cameraX = minBorderX-(playerStartPosX*tileSize)
cameraY = minBorderY-(playerStartPosY*tileSize)

pokemonObjects = []
gameObjects = []
uiObjects = []

pCameraX = 0
pCameraY = 0

#PLAYER GLOBALS
gamePlayer = ""
gamePokemon = ""
currentPlayer = ""
pokemonTeam = []
pokemonThrow = False
pThrowTeste = False
#PLAYER GLOBALS