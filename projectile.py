import pygame
import os
from constants import *

class Projectile(object):
    def __init__(self,perso=None,directory=None,name=None):
        #self.name
        self.dim=32
        self.creator=perso
        self.pos=(perso.pos[0]+40,perso.pos[1]+17)
        #self.pos=(0,200)
        self.mana=40
        self.animation=[]
        self.index=0
        for i in range(1,8):
            spellSource=pygame.image.load(os.path.join(directory,name,"b"+str(i)+".png")).convert_alpha()#the walking's images are named w1.png,w2.png...etc in walk directory
            spellSource=pygame.transform.scale(spellSource,(self.dim,self.dim)).convert_alpha()
            self.animation.append(spellSource)
        self.direction=perso.direction
        if self.direction is not True:
            self.speed=-PAS*3
        else:
            self.speed=PAS*3
        #self.direction=True
        self.image=pygame.transform.flip(self.animation[0],not self.direction,False)
        self.rect=self.image.get_rect()
        
    def update(self,window):
        self.index+=1
        self.pos=(self.pos[0]+self.speed,self.pos[1])
        if self.index>7*3-1:
            self.index=0
        self.image=pygame.transform.flip(self.animation[self.index//(3)],not self.direction,False)
        return self.draw(window)
    
    def draw(self,window):
        self.rect=pygame.Rect((self.pos,(self.dim,self.dim)))
        if 0<=self.pos[0]<=WIDTH and 0<=self.pos[1]<=LENGTH:
            window.blit(self.image,self.pos)
            return True
        else:
            return False
    def gest_collision(self,something=[]):
        for elt in something:         
            #if spell intersects it,then apply damage
            pass
    def setDamage(self,something):
        something.life-=20
        #print("je suis touche")
    def __repr__(self):
        return 
class Arrow(Projectile):
    def __init__(self,perso=None,name=None):
        Projectile.__init__(self,perso,directory="arrows/",name=name)

class Spell(Projectile):
    def __init__(self,perso=None,name=None,incantation=""):
        Projectile.__init__(self,perso,directory="spells/",name=name)
        self.incantation=incantation