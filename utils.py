import pygame
from constants import *

class LifeBar(object):#show the actual state of a character on the scene
    def __init__(self,character=None):
#        global compteur
#        compteur+=1
        global font
        self.character=character
        self.maxlevel=character.life#contains the max level of the lifre of one character, let's assume that the life is filled at the instanciation of the class
        self.length=character.dim#the life bar float upon the character 
        #self.label=font.render("player: "+str(self.level)+"/100",True,(0,255,155))

    def draw(self,window):
        #t=pygame.display.get_surface().get_size()
        pygame.draw.rect(window,(0,0,255),((self.character.rect[0],self.character.rect[1]-10,self.length,5)))#first barr
        pygame.draw.rect(window,(0,255,0),(self.character.rect[0],self.character.rect[1]-10,(self.level*self.length/self.maxlevel),5))#life level
        #window.blit(self.label,(character.rect[0],character.rect[1]))
    def update(self,window):
        global font
        self.level=self.character.life if self.character.life>=0 else 0
        #self.label=font.render("player "+str(self.level)+"/100",True,(0,255,155))
        self.draw(window)

class EnergyBar(object):#show the actual state of a character on the scene
    def __init__(self,character=None):
#        global compteur
#        compteur+=1
        global font
        self.character=character
        self.maxlevel=character.life#contains the max level of the lifre of one character, let's assume that the life is filled at the instanciation of the class
        self.length=character.dim#the life bar float upon the character 
        #self.label=font.render("player: "+str(self.level)+"/100",True,(0,255,155))

    def draw(self,window):
        #t=pygame.display.get_surface().get_size()
        pygame.draw.rect(window,(0,0,255),((self.character.rect[0],self.character.rect[1]-10,self.length,5)))#first barr
        pygame.draw.rect(window,(0,255,0),(self.character.rect[0],self.character.rect[1]-10,(self.level*self.length/self.maxlevel),5))#life level
        #window.blit(self.label,(character.rect[0],character.rect[1]))
    
    def update(self,window):
        global font
        self.level=self.character.life if self.character.life>=0 else 0
        #self.label=font.render("player "+str(self.level)+"/100",True,(0,255,155))
        self.draw(window)