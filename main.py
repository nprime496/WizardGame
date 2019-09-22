# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 08:56:30 2019

@author: _Nprime496_
"""
import os
import pygame
from pygame.locals import *
#from math import abs
pygame.init()

#datas used in the program below
compteur=0
font=pygame.font.Font('freesansbold.ttf',20)
fontCharacter=pygame.font.Font('freesansbold.ttf',15)
WALK=0
DONOTHTING=1
PERFORM=2
HIT=3
DIE=4

TAMPON=1
PAS=6
RIGHT=0   
LEFT=1
SPRITE_DIM=100
SPRITESHEET_DIM=320
ANIM=10
WIDTH=700
LENGTH=350

#pygame.mixer.music.load(os.path.join("backgrounds/","theme.mp3"))
#pygame.mixer.music.play(-1)
pygame.mixer.stop()
#classes


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
#list of all the spells
#spells=[Spell(name="coldfire//",incantation="Expelliamus!")]
class Character(object):
    def __init__(self,source,dim=SPRITE_DIM,keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_SPACE],speed=1,life=100):
        self.life=life
        self.speed=speed
        self.keys=keys
        #walking  
        self.dim=dim
        self.mana=100
        self.walking=[]#this list contains the images of the frameset when the character is moving
        for i in range(1,ANIM+1):
            persoSource=pygame.image.load(os.path.join("character\\"+source+"\walk","w"+str(i)+".png")).convert_alpha()#the walking's images are named w1.png,w2.png...etc in walk directory
            persoSource=pygame.transform.scale(persoSource,(dim,dim)).convert_alpha()
            self.walking.append(persoSource)                
        #do nothing
        self.donothing=[]#same as walking
        for i in range(1,ANIM+1):
            persoSource=pygame.image.load(os.path.join("character\\"+source+"\donothing","w"+str(i)+".png")).convert_alpha()
            persoSource=pygame.transform.scale(persoSource,(dim,dim)).convert_alpha()
            self.donothing.append(persoSource)        
#        #perform spell
        self.perform=[]
        for i in range(1,ANIM+1):
            persoSource=pygame.image.load(os.path.join("character\\"+source+"\perform","w"+str(i)+".png")).convert_alpha()
            persoSource=pygame.transform.scale(persoSource,(dim,dim)).convert_alpha()
            self.perform.append(persoSource)        
        #dying
        self.die=[]
        for i in range(1,ANIM+1):
            persoSource=pygame.image.load(os.path.join("character\\"+source+"\die","w"+str(i)+".png")).convert_alpha()
            persoSource=pygame.transform.scale(persoSource,(dim,dim)).convert_alpha()
            self.die.append(persoSource)        
##        #stand here like a retard       
        self.hit=[]
        for i in range(1,ANIM+1):
            persoSource=pygame.image.load(os.path.join("character\\"+source+"\hit","w"+str(i)+".png")).convert_alpha()
            persoSource=pygame.transform.scale(persoSource,(dim,dim)).convert_alpha()
            self.hit.append(persoSource)
        self.direction=True#right
        self.action=DONOTHTING#the character is lazy so he does nothing by default
        self.index=0
        #all the movements are stored there
        self.animations=[self.walking,self.donothing,self.perform,self.hit,self.die]#,self.die]#,self.perform,self.walking,self.die]
        self.comment_animations=["  ","...","attack","fabulous!","arrrgh!!"]
        self.image=self.animations[self.action][self.index]
        self.pos=(30,LENGTH-dim-70)
        self.time=0#useful to do the special move after a certain time
        self.rect=self.image.get_rect()
        self.myAttack=True#it's not really an attack,it's just there to be different from "None" 
        #print(self.image.get_rect())
        #self.menu=[(self.keys[2],self.walk(True)),(self.keys[3],self.walk(False)),(self.keys[4],self.at)]
    def dying(self,window):
        #print("I'm dying")
        self.index+=1
        #print(len(self.die))
        if self.index<(TAMPON*3)*ANIM-1:
            self.sayDialogue(self.comment_animations[DIE],window)
            self.image=pygame.transform.flip(self.animations[DIE][self.index//(TAMPON*3)],not self.direction,False)#the character changes orientation if necessary
            #self.action=DIE        
    def attack(self,attack):
        self.time=0
        self.index+=1
        if self.index<(TAMPON*2)*ANIM:
            self.image=pygame.transform.flip(self.animations[PERFORM][self.index//(TAMPON*2)],not self.direction,False)#the character changes orientation if necessary
            #persoSource=pygame.transform.scale(persoSource,(self.dim,self.dim)).convert_alpha()
            self.action=PERFORM
            if -self.index+(TAMPON*2)*ANIM==10:
                return attack
        else:
            self.action=DONOTHTING
    def nothing(self,t=200):
        self.time+=1
        if self.time>t:
            #self.time=0
            self.action=HIT
            self.index=0
        if self.action==DONOTHTING:#if the character is doing nothing, then it does nothing
            self.index+=1
            if self.index>(TAMPON*4)*ANIM-1:
                self.index=0
            self.image=pygame.transform.flip(self.animations[DONOTHTING][self.index//(TAMPON*4)],not self.direction,False)
        elif self.action!=PERFORM and self.action!=HIT:
            self.action=DONOTHTING#else,he does nothing
    def walk(self,direction,window):
        P=PAS
        self.time=0
        if direction is not True:#if the direction changed
            P=-PAS#the sign of deplacement change
        self.direction=direction#the direction of the character changes
        self.index+=1
        self.pos=(self.pos[0]+self.speed*P,self.pos[1])#he character moves
        if self.index>TAMPON*ANIM-1:
            self.index=0
        self.sayDialogue(self.comment_animations[WALK],window)
        self.image=pygame.transform.flip(self.animations[WALK][self.index//TAMPON],not self.direction,False)#the character changes orientation if necessary
        self.action=WALK#it walks
        
    def movement(self):
        self.index+=1
        if self.index<(TAMPON*5)*ANIM-1:
            self.image=pygame.transform.flip(self.animations[HIT][self.index//(TAMPON*5)],not self.direction,False)#the character changes orientation if necessary
            self.action=HIT
        else:
            self.time=0
            self.action=DONOTHTING
    def draw(self,screen):
        self.rect=pygame.Rect((self.pos,(self.dim,self.dim)))
        #self.image.move(self.image,self.pos)
        screen.blit(self.image,self.pos)
    def manage_attacks(self,keys,window):
        if keys[self.keys[4]]:
            if self.action!=PERFORM:
                self.index=0
                self.action=PERFORM
                self.myAttack=True#Spell(self,name="coldfire//",incantation="Expelliamus!")
    def update(self,keys,window):
        sp=None#possible spell
        if self.action!=DIE:
            #self.mana+=1
            if keys[self.keys[2]]:
                self.walk(True,window)#moves right
            elif keys[self.keys[3]]:
                #self.sayDialogue(self.comment_animations[WALK],window)
                self.walk(False,window)#moves left
            else:
                self.manage_attacks(keys,window)
            if self.action!=PERFORM:
                if self.action!=HIT:
                    self.sayDialogue(self.comment_animations[DONOTHTING],window)
                    self.nothing()#does nothing if not doing anything else
                else:
                    
                    self.sayDialogue(self.comment_animations[HIT],window)
                    self.movement()
            else:
                self.sayDialogue(self.comment_animations[PERFORM],window)
                #self.sayDialogue(a.incantation,window)
                sp=self.attack(self.myAttack)
                
            if self.life<=0:
                self.action=DIE
                self.index=0
        else:
            #print(self.action)
            self.dying(window)
        self.draw(window)
        return sp
    def receiveInjuries(self):
        self.life-=20
        
    def sayDialogue(self,texte,window):
        global fontCharacter
        text=fontCharacter.render(texte,True,(200,0,180))
        #print(self.rect)
        window.blit(text,(self.rect[0],self.rect[1]-25))
        pass        
#definition of herited classes    
class Goblin(Character):
    """
        Incredibly dumb but powerful
    """
    def __init__(self,source,dim=100,keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_SPACE],speed=1.5,life=200):
        Character.__init__(self,source,dim,keys,speed,life)
        self.comment_animations=["  ","...","ARGH!!","AAARGHH","AGRRRRH!!"]
class Orc(Character):
    """
        mysterious as f*ck
    """
    def __init__(self,source,dim=100,keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_SPACE]):
        Character.__init__(self,source,dim,keys)
class Knight(Character):
    """
        Just give him a castle to protect
    """
    def __init__(self,source,dim=100,keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_SPACE]):
        Character.__init__(self,source,dim,keys)
        self.comment_animations=["  ","...","Expelliarmus","Magic is might","Arrrgh!!"]
class Hunter(Character):
    """
        a forest, and he will be happy
    """
    def __init__(self,source,dim=100,keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_SPACE]):
        Character.__init__(self,source,dim,keys)
        self.comment_animations=["  ","...","In your eye!!","What a shoot!","Arrrgh!!"]
    def nothing(self,t=200):
        Character.nothing(self,t)
class Wizard(Character):
    """
        avada kedavra
    """
    def __init__(self,source,dim=75,keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_SPACE],life=100):
        Character.__init__(self,source,dim,keys)
        self.myAttack=None
        self.comment_animations=["  ","...","Expelliarmus!!","Magic is might","Arrrgh!!"]
    def nothing(self,t=400):
        Character.nothing(self,t)
    def manage_attacks(self,keys,window):
        if keys[self.keys[4]]:
            if self.action!=PERFORM:
                self.index=0
                self.action=PERFORM
                self.myAttack=Spell(self,name="coldfire//",incantation="Expelliamus!")
    
def manage_characters_projectiles(characters,projectiles):
    #return
    
    for p in projectiles:#and type(c) is not Wizard:
        #print(len(projectiles))
        for c in characters:
            
            if p.creator!=c and p.rect.colliderect(c.rect) and c.action!=DIE:
                #print("touche"
                #pass
                #print("touche")
                #pass#print("touche")
                p.setDamage(c)
                try:
                    projectiles.remove(p)
                except ValueError:#this happens when two characters are at the same place when the projectile hit 
                    pass
            #p.pos=c.pos
            #projectiles.remove(p)
            #if p intersects the character, then apply the damages on the projectile on it
            #then, delete the projectile in the list of projectiles
            #pass
def manage_characters_collision(characters,c):#when a character c has thrown an attack
    for c2 in characters:
        if c2!=c and c.rect.colliderect(c2.rect):#if one anather character is nearby, it get the damages
            if ((c.direction is False and c2.pos[0]<c.pos[0] ) or (c.direction is True and c2.pos[0]>c.pos[0])) and c2.action!=DIE :#if they are face to face
                c2.receiveInjuries()#get damages
                break#the attack is over
            
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
        
def afficher(window,character):
    character.draw(window)    #write the name of the character and his life and mana
#main program
def main():
    player2_keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_d,pygame.K_a,pygame.K_s]
    #player1_keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_l,pygame.K_j,pygame.K_k]
    #screen    
    window=pygame.display.set_mode((WIDTH,LENGTH))
    pygame.display.set_caption("Wizard Fight 496")#title of the game... don't blame me, I was kinda in hurry
    backgound=pygame.image.load(os.path.join("backgrounds","5.jpg")).convert()#the backgrounds are named like 1.png,2.png,...6.png in backgrounds directory
    backgound=pygame.transform.scale(backgound,(WIDTH,LENGTH))#the background is scaled to the size of the screen
    #cld=Spell()
    #Character("wizard")
    #Wizard("wizard")
    #Goblin("goblin")
    list_characters=[Goblin("goblin",100),Wizard("wizard",80,player2_keys)]#,Hunter("hunter",80,player1_keys)]#this list contains all the characters on the screen
    #list_life_bar=[(LifeBar(,list_characters[1]),(LifeBar(length=200,pos=(-20,30)),list_characters[0])]
    list_life_bar=[LifeBar(elt) for elt in list_characters]#this list contains all the character's life bar and will be used for the update of those
    list_spells=[]#contains all the spells aimed during the current frame of the game    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
                os.sys.exit()
        keys=pygame.key.get_pressed()
        window.blit(backgound,(0,0))
        #for every character on the window
        for chrtr in list_characters:
            sp=chrtr.update(keys,window)#get character comportment
            if type(sp) is Spell:
                list_spells.append(sp)
            elif sp is not None:
                #print(sp,"a")
                manage_characters_collision(list_characters,chrtr)#manage if a character aimed an physical attack
        #manage all the spells aimed
        for elt in list_spells:
            if not elt.update(window):
                list_spells.remove(elt)
            #pygame.draw.rect(window,(0,155,10),elt.rect,3)
        for elt in list_life_bar:
            if elt.character.life>0:
                elt.update(window)
            else:
                list_life_bar.remove(elt)
        manage_characters_projectiles(list_characters,list_spells)
        #pygame.draw.rect(window,(45,255,200),list_characters[0].rect,3)
        #pygame.draw.rect(window,(0,155,200),list_characters[1].rect,3)
        pygame.display.update()
        pygame.time.Clock().tick(30)
    #pygame.mixer.music.stop()
#execution
main()

print("THANKS FOR GAMING, for any suggestion contact me : feedback496@gmail.com ")