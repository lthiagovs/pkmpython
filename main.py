import pygame
import map
import gameObject
import core
import threading
import interface
import moves

#INIT and Globals
pygame.init()
pygame.display.init()
gameScreen = pygame.display.set_mode((core.screenSizeX,core.screenSizeY))
pygame.mixer.init()
tileSize = 32
tick = 0

MouseX = 0
MouseY = 0

#load and add map
gameMap = map.readMap("map.map")
objectData = gameObject.readObjects("obj//teste.obj")
core.gameObjects = map.renderMap(gameMap, objectData)

#add players
core.gamePlayer = gameObject.Player(core.playerStartPosX*core.tileSize, core.playerStartPosY*core.tileSize, ["sprites//player.png"], "Player", "", 3, "PlayerName")
core.gamePokemon = ""
core.currentPlayer = core.gamePlayer
core.gamePlayer.collide = True
gameClock = pygame.time.Clock()
#add players

#UI
interface.buildPokemonUI()
#UI

#INIT
#pygame.mixer.music.load("music//viridiancity.mp3")
landscapeIMG = pygame.image.load("sprites//Tiles//landscape.png")
pygame.mixer.Channel(0).play(pygame.mixer.Sound("music//viridiancity.mp3"))
pygame.mixer.Channel(

    0).set_volume(0.1)

core.currentPlayer.addPokemonsTeste()

#LOOP
if __name__ == '__main__':
    while True:
        pygame.display.set_caption(str(gameClock.get_fps()))
        #Render
        threading.Thread(target=gameObject.smartRenderObjects(gameScreen)).start()
        threading.Thread(target=gameObject.smartRenderPokemons(gameScreen)).start()
        threading.Thread(target=interface.renderUI(gameScreen)).start()

        core.gamePlayer.render(gameScreen)
        if core.pokemonThrow:
            core.gamePokemon.render(gameScreen)

        #Player Logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #THROW POKEMON SYSTEM

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    if core.pokemonThrow:
                        #gameObjects.remove(gamePokemon)
                        core.currentPlayer = core.gamePlayer
                        core.currentPlayer.state="back"
                        core.cameraX -= core.pCameraX
                        core.cameraY -= core.pCameraY
                        core.pCameraX = 0
                        core.pCameraY = 0
                        core.pokemonThrow = False
                    elif core.gamePlayer.state=="idle":

                        core.gamePokemon = gameObject.Player(core.gamePlayer.screenX,core.gamePlayer.screenY-64,[pygame.image.load("sprites//player.png")],"Pokemon","",4,"Primeape")
                        core.cameraY-=64
                        core.pCameraY-=64
                        core.gamePokemon.path = "sprites//Pokemon//Primeape//"
                        core.gamePokemon.state="idle"
                        core.gamePokemon.currentSPR="front"
                        core.currentPlayer.state="throw"
                        core.gamePokemon.Name = "Primeape"
                        core.gamePokemon.speed = 6
                        core.gamePokemon.Moves = [moves.Move(60),moves.Move(120)]
                        core.currentPlayer = core.gamePokemon
                        core.pokemonThrow = True
                elif event.key == pygame.K_p and not core.pokemonThrow:
                    dX = 0
                    dY = 0
                    if core.gamePlayer.direction == 0:
                        dX = -1
                    elif core.gamePlayer.direction == 1:
                        dX = 1
                    elif core.gamePlayer.direction == 2:
                        dY = 1
                    elif core.gamePlayer.direction == 3:
                        dY = -1
                    nPokeball = gameObject.GameObject(core.gamePlayer.screenX-core.cameraX,core.gamePlayer.screenY-core.cameraY,[pygame.image.load("sprites//Effects//3.png")],"Effect")
                    nPokeball.collide = False
                    nPokeball.speed = 10
                    nPokeball.dX = dX
                    nPokeball.dY = dY
                    nPokeball.autoDestroy = 60
                    nPokeball.catchPokemon = True
                    core.gameObjects.append(nPokeball)

                elif event.key == pygame.K_u:
                    nPokemon = gameObject.GameObject(core.gamePlayer.screenX-core.cameraX,core.gamePlayer.screenY-core.cameraY,[pygame.image.load("sprites//entity.png")],"Pokemon")
                    nPokemon.isPokemon = True
                    nPokemon.hasWalk = True
                    nPokemon.Name = "Primeape"
                    nPokemon.walkSpeed = 1
                    nPokemon.changeDirectionTime = 60
                    core.pokemonObjects.append(nPokemon)
                elif event.key == pygame.K_y:
                    core.gamePlayer.addPokemon()
                elif event.key == pygame.K_1 and core.pokemonThrow:
                    core.currentPlayer.state = "move1"
                elif event.key == pygame.K_2 and core.pokemonThrow:
                    core.currentPlayer.state = "move2"

            #THROW POKEMON SYSTEM

        #TO FIX JUST RE ADD THE ELIF
        keys = pygame.key.get_pressed()  # Checking pressed keys

        #PLAYER MOVEMENT KEYS
        if core.currentPlayer.state != "throw" and core.currentPlayer.state != "back" and not("move" in core.currentPlayer.state):

            if keys[pygame.K_LEFT] and not gameObject.collidePlayer(core.currentPlayer,core.gameObjects,0):
                #gameObject.moveAllMapObjects(gameObjects, currentPlayer.speed, 0)
                core.cameraX += core.currentPlayer.speed
                core.currentPlayer.state = "walk"
                core.currentPlayer.direction = 0
                core.currentPlayer.WalkX = 1

                if core.pokemonThrow:
                    core.pCameraX += core.gamePokemon.speed

            elif keys[pygame.K_RIGHT] and not gameObject.collidePlayer(core.currentPlayer,core.gameObjects,1):
                #gameObject.moveAllMapObjects(gameObjects, currentPlayer.speed * -1, 0)
                core.cameraX -= core.currentPlayer.speed
                core.currentPlayer.state = "walk"
                core.currentPlayer.direction = 1
                core.currentPlayer.WalkX = -1

                if core.pokemonThrow:
                    core.pCameraX -= core.gamePokemon.speed
            else:
                core.currentPlayer.WalkX = 0

            if keys[pygame.K_UP] and not gameObject.collidePlayer(core.currentPlayer,core.gameObjects,3):
                #gameObject.moveAllMapObjects(gameObjects, 0, currentPlayer.speed)
                core.cameraY+=core.currentPlayer.speed
                core.currentPlayer.state = "walk"
                core.currentPlayer.direction = 3
                core.currentPlayer.WalkY = 1

                if core.pokemonThrow:
                    core.pCameraY += core.gamePokemon.speed

            elif keys[pygame.K_DOWN] and not gameObject.collidePlayer(core.currentPlayer,core.gameObjects,2):
                #gameObject.moveAllMapObjects(gameObjects, 0, currentPlayer.speed*-1)
                core.cameraY -= core.currentPlayer.speed
                core.currentPlayer.state = "walk"
                core.currentPlayer.direction = 2
                core.currentPlayer.WalkY = -1

                if core.pokemonThrow:
                    core.pCameraY -= core.gamePokemon.speed
            else:
                core.currentPlayer.WalkY = 0

            if core.currentPlayer.WalkX == 0 and core.currentPlayer.WalkY == 0:
                core.currentPlayer.state = "idle"

        #Update
        pygame.display.update()
        #gameScreen.fill((0, 0, 0))
        gameScreen.blit(landscapeIMG, (0, 0))
        gameClock.tick(60)

    #LOOP