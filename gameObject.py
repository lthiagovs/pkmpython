import pygame
import random
import core
import moves

globalAnimationDelay = 30
pygame.font.init()
gameFont = pygame.font.Font("system//gamefont.ttf",8)
tileSize = 32
pygame.mixer.init()
pygame.mixer.Channel(1).set_volume(0.1)
pygame.mixer.Channel(2).set_volume(0.1)
pygame.mixer.Channel(3).set_volume(0.5)

class GameObject():
    def __init__(self, x, y, image, type):
        #------------Core------------
        self.x = x
        self.y = y
        self.rX = x
        self.rY = y
        self.rect = pygame.Rect(x, y, tileSize, tileSize)
        self.image = image
        self.type = type
        self.collide = False
        #------------Movement------------ BALLISTIC
        self.speed = 1
        self.dX = 0
        self.dY = 0
        # ------------Animation------------ SPRITES
        self.animationDelay = globalAnimationDelay/self.speed
        self.animationCount = 0
        self.currentImage = 0
        #------------Self Destroy------------
        self.autoDestroy = 0
        self.autoCount = 0
        #------------Colision------------
        self.hit = 0
        # ------------Pokemon------------
        self.isPokemon = False
        self.Name = ""
        self.Moves = []
        self.Cry = ""
        # STATS
        self.HP = 100
        self.PP = 100
        #------------Walk------------ ENTITY
        #if walk
        self.hasWalk = False
        self.changeDirectionTime = 0
        self.walkInterval = 0
        self.walkIntervalCount = 0
        self.walkCount = 0
        self.walkSpeed = 0
        self.Step = 0
        self.StepCount = 0
        self.State = "walk"
        self.lastPos = ""
        self.WalkX = random.randint(-1,1)
        self.WalkY = random.randint(-1, 1)
        # ------------Special------------ ENTITY
        self.catchPokemon = False
        self.doDamage = False
        self.Damage = 0

    def getDirection(self):
        if self.dX>0:
            return 1
        elif self.dX>0:
            return 0
        elif self.dY<0:
            return 3
        elif self.dY>0:
            return 2
    def setDirection(self):
        self.rX += self.speed * self.dX
        self.rY += self.speed * self.dY
    def selfDestroy(self):
        if self.autoDestroy > 0:
            self.autoCount += 1
            if self.autoCount >= self.autoDestroy:
                self.type = "None"
    #changes image frame
    def animate(self):
        if len(self.image):
            self.animationCount += 1
            if self.animationCount >= self.animationDelay:
                self.animationCount = 0
                self.currentImage += 1
                if self.currentImage == len(self.image):
                    self.currentImage = 0
    def setWalkDirection(self):
        self.rX += self.WalkX * self.walkSpeed
        self.rY += self.WalkY * self.walkSpeed
    def changeStep(self):
        self.animationCount += 1
        if self.animationCount >= self.animationDelay / self.speed:
            self.animationCount = 0
            if self.StepCount == 0:
                self.StepCount = 1
                self.Step = 1
            else:
                self.Step = 2
                self.StepCount = 0
    def setWalkFrame(self):
        self.image = "sprites//Pokemon//" + self.Name + "//"
        if self.State == "walk":
            self.lastPos = ""
            if self.WalkX > 0:
                self.image += "right"
                self.lastPos += "right"
            elif self.WalkX < 0:
                self.image += "left"
                self.lastPos += "left"

            if self.WalkY > 0:
                self.image += "front"
                self.lastPos += "front"
            elif self.WalkY < 0:
                self.image += "back"
                self.lastPos += "back"
            self.image += str(self.Step) + ".png"
        elif self.State == "idle":
            self.image += self.lastPos + "0.png"
        self.image = pygame.image.load(self.image)
    def render(self,surface):

        if self.catchPokemon:
            catchPokemon(self)

        #Core + Movement
        if not self.hasWalk:
            self.setDirection()

        #Self Destroy (autoDestroy > 0)
        self.selfDestroy()

        #Animation
        if not self.isPokemon:
            self.animate()

        #Damage
        if self.doDamage:
            doRangedDamage(self)

        #Walk
        if self.hasWalk:
            self.setWalkDirection()

            #CHANGE STEP CODE
            if self.isPokemon:
                self.changeStep()

            self.walkCount += 1
            if self.walkCount >= self.changeDirectionTime:
                self.walkCount = 0
                if self.walkInterval == 0:
                    self.WalkX = random.randint(-1, 1)
                    self.WalkY = random.randint(-1, 1)
                    self.walkInterval = 1
                    self.State = "walk"
                else:
                    self.State = "idle"
                    self.StepCount = 0
                    self.WalkX = 0
                    self.WalkY = 0
                    self.walkInterval = 0
                    #self.State = "idle"

            self.setWalkFrame()

        #Render
        #if the object is a pokemon
        if self.isPokemon:
            surface.blit(self.image, (self.x, self.y))
            self.drawHealthBar(surface, self.x, self.y+50)
            self.drawPPBar(surface, self.x, self.y+55)
        #if is a common object
        else:
            surface.blit(self.image [self.currentImage], (self.x, self.y))
    def drawHealthBar(self, surface,x,y):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(x, y, 40, 3))
        pygame.draw.rect(surface, (255,50,50), pygame.Rect(x,y,0.4*self.HP,3))
    def drawPPBar(self, surface,x,y):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(x, y,40, 3))
        pygame.draw.rect(surface, (100,100,255), pygame.Rect(x,y,0.4*self.PP,3))

class Player(GameObject) :
    def __init__(self,x,y,image,type,sprPlayer,speed,name):
        super().__init__(x,y,image,type)
        self.sprPlayer = sprPlayer
        self.speed = speed
        self.screenX = 384
        self.screenY = 288
        self.x = self.screenX
        self.y = self.screenY
        self.Name = "Player"
        self.pFont = gameFont.render(name, True, (0, 255, 0))
        self.state = "idle"
        self.direction = 2
        self.step = 1
        self.stepCount = 0
        self.animationSpeed = globalAnimationDelay/speed
        self.animationCount = 0
        self.path = "sprites//Pokemon//Player//"
        self.currentSPR = ""

    def addPokemonsTeste(self):
        nPokemon1 = Player(core.gamePlayer.screenX, core.gamePlayer.screenY - 64,
                          [pygame.image.load("sprites//player.png")], "Pokemon", "", 4,
                          "Primeape")
        nPokemon1.path = "sprites//Pokemon//Primeape//"
        nPokemon1.state = "idle"
        nPokemon1.currentSPR = "front"
        nPokemon1.Name = "Primeape"
        nPokemon1.speed = 6
        nPokemon1.Cry = "music//cries//Primeape.mp3"
        nPokemon1.Moves = [moves.Move(60), moves.Move(120)]
        #########################################################
        nPokemon2 = Player(core.gamePlayer.screenX, core.gamePlayer.screenY - 64,
                           [pygame.image.load("sprites//player.png")], "Pokemon", "", 4,
                           "Gengar")
        nPokemon2.path = "sprites//Pokemon//Gengar//"
        nPokemon2.state = "idle"
        nPokemon2.currentSPR = "front"
        nPokemon2.Name = "Gengar"
        nPokemon2.speed = 6
        nPokemon2.Cry = "music//cries//Gengar.mp3"
        nPokemon2.Moves = [moves.Move(60), moves.Move(120)]
        core.pokemonTeam.append(nPokemon1)
        core.pokemonTeam.append(nPokemon2)
    def addPokemon(self):
        if len(core.pokemonTeam) == 6:
            print("PT FULL")
        else:
            nPokemon = Player(core.gamePlayer.screenX, core.gamePlayer.screenY - 64,
                                                 [pygame.image.load("sprites//player.png")], "Pokemon", "", 4,
                                                 "Primeape")
            nPokemon.path = "sprites//Pokemon//Primeape//"
            nPokemon.state = "idle"
            nPokemon.currentSPR = "front"
            nPokemon.Name = "Primeape"
            nPokemon.speed = 6
            nPokemon.Moves = [moves.Move(60), moves.Move(120)]
    def summonPokemon(self,pokemon):
        #core.pokemonObjects.append(core.pokemonTeam[pokemon])
        if core.gamePlayer.state == "idle":
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("music//effects//pokeballEnter.mp3"))
            core.cameraY -= 64
            core.pCameraY -= 64
            core.currentPlayer.state = "throw"
            core.gamePokemon = core.pokemonTeam[pokemon]
            core.currentPlayer = core.gamePokemon
            core.pokemonThrow = True
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(core.gamePokemon.Cry))
    def backPokemon(self,pokemon):
        #core.pokemonObjects.remove(core.pokemonTeam[pokemon])
        if core.pokemonThrow:
            core.currentPlayer = core.gamePlayer
            core.currentPlayer.state = "back"
            core.cameraX -= core.pCameraX
            core.cameraY -= core.pCameraY
            core.pCameraX = 0
            core.pCameraY = 0
            core.pokemonThrow = False
    def getCurrentSPR(self):
        currentSPR = ""
        if self.WalkX > 0:
            currentSPR += "left"
        elif self.WalkX < 0:
            currentSPR += "right"
        if self.WalkY > 0:
            currentSPR += "back"
        elif self.WalkY < 0:
            currentSPR += "front"
        return currentSPR
    def newPlayerAnimations(self):
        img = self.path
        if self.state == "idle":
            self.step = 1
            self.stepCount = 0
            img = self.path + self.currentSPR+"0.png"
            #if self.direction == 0:
            #    img = self.path + "left0.png"
            #elif self.direction == 1:
            #    img = self.path + "right0.png"
            #elif self.direction == 2:
            #    img = self.path + "front0.png"
            #elif self.direction == 3:
            #    img = self.path + "back0.png"
        elif self.state == "walk":
            if self.WalkX > 0:
                img += "left"
            elif self.WalkX < 0:
                img += "right"
            if self.WalkY > 0:
                img += "back"
            elif self.WalkY < 0:
                img += "front"
            img += str(self.step) + ".png"
            self.currentSPR = self.getCurrentSPR()
        elif self.state == "throw":
            img = self.path + self.state + str(self.stepCount) + ".png"
            self.animationCount += 1
            if self.animationCount >= self.animationSpeed:
                self.animationCount = 0
                self.stepCount += 1
                if self.stepCount > 4:
                    self.stepCount = 4
                    self.animationCount = 0

        elif self.state == "back":
            img = self.path + "throw" + str(self.stepCount) + ".png"
            self.animationCount += 1
            if self.animationCount >= self.animationSpeed:
                self.animationCount = 0
                self.stepCount -= 1
                if self.stepCount < 0:
                    self.stepCount = 0
                    self.state = "idle"

        self.image = pygame.image.load(img)
    def changeStep(self):
        self.animationCount+=1
        if (self.state == "walk" or "move" in self.state) and self.animationCount >= self.animationSpeed:
            self.animationCount = 0
            if self.stepCount == 0:
                self.step = 1
                self.stepCount = 1
            elif self.stepCount == 1:
                self.step = 0
                self.stepCount = 2
            elif self.stepCount == 2:
                self.step = 2
                self.stepCount = 3
            elif self.stepCount == 3:
                self.step = 0
                self.stepCount = 0
    def getDirectionX(self):
        if "left" in self.currentSPR:
            return -1
        elif "right" in self.currentSPR:
            return 1
        else:
            return 0
    def getDirectionY(self):
        if "back" in self.currentSPR:
            return -1
        elif "front" in self.currentSPR:
            return 1
        else:
            return 0

    def pokemonAnimations(self):
        if "move1" == self.state:
            #Move animation
            img = "sprites//Pokemon//"+self.Name+"//move1//"+self.currentSPR+str(self.step)+".png"
            self.image = pygame.image.load(img)

            if self.Moves[0].runMove():
                createRangedDamage(30, self.x - core.cameraX, self.y - core.cameraY, self.getDirectionX(),self.getDirectionY())
                self.state = "idle"
        if "move2" == self.state:
            #Move animation
            img = "sprites//Pokemon//"+self.Name+"//move2//"+self.currentSPR+str(self.step)+".png"
            self.image = pygame.image.load(img)
            if self.Moves[1].runMove():
                self.state = "idle"
            doMeeleeDamage(0.5)
    def render(self,surface):

        #self.playerAnimations()
        if not "move" in self.state:
            self.newPlayerAnimations()

        #Player screen position
        drawX = self.screenX
        drawY = self.screenY
        if self.state=="throw":
            drawX += core.pCameraX
            drawY += core.pCameraY
        # Player screen position

        #Change Step on walking
        self.changeStep()
        self.pokemonAnimations()
        surface.blit(self.pFont,(drawX-4,drawY-10))
        surface.blit(self.image,(drawX,drawY))
        self.rect.x = drawX
        self.rect.y = drawY
        self.drawHealthBar(surface,drawX,drawY+50)
        self.drawPPBar(surface, drawX, drawY + 55)

#Renders only the objects inside the screen
def smartRenderObjects(surface):
    for objects in core.gameObjects:

        #UPDATE POSITIONS
        objects.x = objects.rX + core.cameraX
        objects.y = objects.rY + core.cameraY
        objects.rect.x = objects.x
        objects.rect.y = objects.y
        # UPDATE POSITIONS

        #if not (objects.x>800 or objects.x<-32 or objects.y>600 or objects.y<-32):
        if objects.type == "None":
            core.gameObjects.remove(objects)
        else:
            objects.render(surface)

#Renders only the pokemons inside the screen
def smartRenderPokemons(surface):
    for objects in core.pokemonObjects:

        #UPDATE POSITIONS
        objects.x = objects.rX + core.cameraX
        objects.y = objects.rY + core.cameraY
        objects.rect.x = objects.x
        objects.rect.y = objects.y
        # UPDATE POSITIONS

        #if not (objects.x>800 or objects.x<-32 or objects.y>600 or objects.y<-32):
        if objects.HP <= 0:
            core.pokemonObjects.remove(objects)
        else:
            objects.render(surface)

#Moves all the objects in the given object list
def moveAllObjects(objectList, xMove, yMove):
    for objects in objectList:
        objects.x+=xMove
        objects.y+=yMove
        objects.rect.x = objects.x
        objects.rect.y = objects.y

def moveAllMapObjects(objectList, xMove, yMove):
    for objects in objectList:
        if objects.type == "Tile":
            #print(objects.type)
            objects.x+=xMove
            objects.y+=yMove
            objects.rect.x=objects.x
            objects.rect.y=objects.y

def collide(object1, objectList):
    for object2 in objectList:
        if(object2.type!="Tile"and object2!=object1):
            if pygame.Rect.colliderect(object1.rect,object2.rect):
                objectList.remove(object2)

def collidePlayer(gamePlayer,objectList,direction):
    collideRect = ""
    if direction == 0:#esquerda
        collideRect = pygame.Rect(gamePlayer.screenX,gamePlayer.screenY+10,1,tileSize-10)
    elif direction == 1:#direita
        collideRect = pygame.Rect(gamePlayer.screenX+tileSize+6, gamePlayer.screenY+16, 1, tileSize-16)
    elif direction == 2:#baixo
        collideRect = pygame.Rect(gamePlayer.screenX+10, gamePlayer.screenY+8+tileSize, tileSize-10, 1)
    elif direction == 3:#cima
        collideRect = pygame.Rect(gamePlayer.screenX+10, gamePlayer.screenY - 6, tileSize-10, 1)
    for object in objectList:
        if object.collide and pygame.Rect.colliderect(collideRect,object.rect):
            return True
    return False

def catchPokemon(pokeball):
    for pokemon in core.pokemonObjects:
        if pygame.Rect.colliderect(pokemon.rect,pokeball.rect):
            core.pokemonObjects.remove(pokemon)
            core.gameObjects.remove(pokeball)
            nPokeballEffect = GameObject(pokeball.x-core.cameraX,pokeball.y-core.cameraY,[pygame.image.load("sprites//Effects//Catch//0.png"),
                                                                pygame.image.load("sprites//Effects//Catch//1.png")],"Effect")
            nPokeballEffect.autoDestroy = 200
            core.gameObjects.append(nPokeballEffect)
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("music//effects//pokeballShaking.mp3"))

def doMeeleeDamage(damage):
    for pokemon in core.pokemonObjects:
        if pygame.Rect.colliderect(core.currentPlayer.rect,pokemon.rect):
            pokemon.HP -= damage

def doRangedDamage(missile):
    for pokemon in core.pokemonObjects:
        if pygame.Rect.colliderect(missile.rect,pokemon.rect):
            pokemon.HP -= missile.Damage
            core.gameObjects.remove(missile)

def createRangedDamage(damage,x,y,dX,dY):
    missile = GameObject(x,y,[pygame.image.load("sprites//Effects//rocks.png")],"Effects")
    missile.dX = dX
    missile.dY = dY
    missile.autoDestroy = 120
    missile.speed = 8
    missile.doDamage = True
    missile.Damage = damage
    core.gameObjects.append(missile)

def createDamageObject(damage,x,y):
    print()

#Reads a object list
def readObjects(objData):
    objectList = []
    readingOBJ = False
    currentOBJ = ""
    sprites = []
    colision = 0

    readingSprite = False
    readingCollision = False
    objFile = open("obj//teste.obj",'r')
    for lines in objFile:
        lines = lines.replace('\n','')
        if readingOBJ:

            if "&spr&" in lines:
                readingSprite = True
            elif "&collide&" in lines:
                readingCollision = True
            elif "#" in lines:
                readingSprite=False
                readingCollision=False
            elif readingSprite:
                sprites.append(pygame.image.load(lines))
            elif readingCollision:
                colision=int(lines)

        if "$" in lines:
            readingOBJ = True
            currentOBJ = GameObject(0, 0, ["sprites//empty.png"], "Tile")
        elif "@" in lines:
            currentOBJ.image = sprites
            currentOBJ.collide = colision
            sprites = []
            objectList.append(currentOBJ)
            readingOBJ = False
        elif "!" in lines:
            break
    objFile.close()
    return objectList