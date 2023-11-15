import pygame
import core
import gameObject

class Interface():
    def __init__(self,x,y,image, type):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.type = type

        #SPECIAL - Pokemon Portrait
        self.portraitNumber = -1
        self.pokeballSprite = pygame.image.load("sprites//portraitSelect.png")
        self.rect = pygame.Rect(x,y,self.image.get_width(),self.image.get_height())

    def mouse_event(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True
        return False
    def render(self,surface):
        surface.blit(self.image,(self.x,self.y))

        if self.type == "Portrait" and self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.pokeballSprite, (self.x, self.y))
            if self.mouse_event():
                #lembrar o pokemon que foi jogado para depois apaga-lo
                if self.portraitNumber < len(core.pokemonTeam):
                    if core.pokemonThrow:
                        core.gamePlayer.backPokemon(self.portraitNumber)
                    else:
                        core.gamePlayer.summonPokemon(self.portraitNumber)

def renderUI(surface):
    for ui in core.uiObjects:
        if ui.type == "Portrait":
            if ui.portraitNumber < len(core.pokemonTeam):
                ui.image = pygame.image.load("sprites//Pokemon//"+core.pokemonTeam[ui.portraitNumber].Name+"//portrait.png")
        ui.render(surface)

def buildPokemonUI():
    portrait1 = Interface(0,core.screenSizeY-40,"sprites//portrait.png","Portrait")
    portrait1.portraitNumber = 0
    portrait2 = Interface(portrait1.x+45, core.screenSizeY-40, "sprites//portrait.png","Portrait")
    portrait2.portraitNumber = 1
    portrait3 = Interface(portrait2.x+45, core.screenSizeY-40, "sprites//portrait.png","Portrait")
    portrait3.portraitNumber = 2
    portrait4 = Interface(portrait3.x+45, core.screenSizeY-40, "sprites//portrait.png","Portrait")
    portrait4.portraitNumber = 3
    portrait5 = Interface(portrait4.x+45, core.screenSizeY-40, "sprites//portrait.png","Portrait")
    portrait5.portraitNumber = 4
    portrait6 = Interface(portrait5.x+45, core.screenSizeY-40, "sprites//portrait.png","Portrait")
    portrait6.portraitNumber = 5
    core.uiObjects.append(portrait1)
    core.uiObjects.append(portrait2)
    core.uiObjects.append(portrait3)
    core.uiObjects.append(portrait4)
    core.uiObjects.append(portrait5)
    core.uiObjects.append(portrait6)

