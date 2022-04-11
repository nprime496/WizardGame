import pygame
from constants import *
import os
from projectile import *
import sys

#list of all the spells
#spells=[Spell(name="coldfire//",incantation="Expelliamus!")]
class Character(object):
    def __init__(self,image_path,dim,keystrokes=None,speed=1,life=100):

        self.life=life
        self.speed=speed
        self.keystrokes=keystrokes
        #walking  
        self.dim=dim
        self.mana=100
        self.walking=[]#this list contains the images of the frameset when the character is moving
        
        animations=["walk","donothing","perform","hit","die"]
        self.animations=[]
        for anim in animations:
            tmp=[]
            for i in range(1,ANIM+1):
                try:
                    persoSource=pygame.image.load(os.path.join("character",image_path,anim,"w"+str(i)+".png")).convert_alpha()#the walking's images are named w1.png,w2.png...etc in walk directory
                    
                    persoSource=pygame.transform.scale(persoSource,(dim,dim)).convert_alpha()
                    tmp.append(persoSource)
                except Exception as e:
                    print(e,file=sys.stderr)
            self.animations.append(tmp)                
        self.direction=True#right
        self.action=DONOTHTING#the character is lazy so he does nothing by default
        self.index=0
        #all the movements are stored there
        #self.animations=[self.walking,self.donothing,self.perform,self.hit,self.die]#,self.die]#,self.perform,self.walking,self.die]
        self.comment_animations=["  ","...","attack","fabulous!","arrrgh!!"]
        self.image=self.animations[self.action][self.index]
        self.pos=(30,LENGTH-dim-70)
        self.time=0#useful to do the special move after a certain time
        self.rect=self.image.get_rect()
        self.myAttack=True#it's not really an attack,it's just there to be different from "None" 
        #print(self.image.get_rect())
        #self.menu=[(self.keystrokes[2],self.walk(True)),(self.keystrokes[3],self.walk(False)),(self.keystrokes[4],self.at)]
    def dying(self,window):
        #print("I'm dying")
        self.index+=1
        #print(len(self.die))
        if self.index<(TAMPON*3)*ANIM-1:
            try:
                self.sayDialogue(self.comment_animations[DIE],window)
                self.image=pygame.transform.flip(self.animations[DIE][self.index//(TAMPON*3)],not self.direction,False)#the character changes orientation if necessary
            except Exception as e:
                print(e,file=sys.stderr)
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

        tmp=(self.pos[0]+self.speed*P,self.pos[1])#he character moves
        if not (tmp[0]>=WIDTH-50 or tmp[0]<-30):
            self.pos=tmp
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
    def manage_attacks(self,keystrokes,window):
        if keystrokes[self.keystrokes[4]]:
            if self.action!=PERFORM:
                self.index=0
                self.action=PERFORM
                self.myAttack=True#Spell(self,name="coldfire//",incantation="Expelliamus!")
    def update(self,keystrokes,window):
        sp=None#possible spell
        if self.action!=DIE:
            #self.mana+=1
            if keystrokes[self.keystrokes[2]]:
                self.walk(True,window)#moves right
            elif keystrokes[self.keystrokes[3]]:
                #self.sayDialogue(self.comment_animations[WALK],window)
                self.walk(False,window)#moves left
            else:
                self.manage_attacks(keystrokes,window)
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

    def setKeystrokes(self,keystrokes):
        self.keystrokes=keystrokes
        return self

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
    def __init__(self,image_path,dim=100,keystrokes=None,speed=1.5,life=200):
        Character.__init__(self,image_path,dim,keystrokes,speed,life)
        self.comment_animations=["  ","...","ARGH!!","AAARGHH","AGRRRRH!!"]
class Orc(Character):
    """
        mysterious as f*ck
    """
    def __init__(self,image_path,dim=80,keystrokes=None):
        Character.__init__(self,image_path,dim,keystrokes)
        print("ORC: ",image_path)
        self.comment_animations=["  ","*sssss*","!hiss!","*sssss*","..."]


class Knight(Character):
    """
        Just give him a castle to protect
    """
    def __init__(self,image_path,dim=80,keystrokes=None):
        Character.__init__(self,image_path,dim,keystrokes)
        self.comment_animations=["  ","...","En garde!","Pour le roi!","Oh! Je me meurs!!"]
class Hunter(Character):
    """
        a forest, and he will be happy
    """
    def __init__(self,image_path,dim=80,keystrokes=None):
        Character.__init__(self,image_path,dim,keystrokes)
        self.comment_animations=["  ","...","In your eye!!","What a shoot!","Arrrgh!!"]
    def nothing(self,t=200):
        Character.nothing(self,t)
class Wizard(Character):
    """
        avada kedavra
    """
    def __init__(self,image_path,dim=75,keystrokes=None,life=80):
        Character.__init__(self,image_path,dim,keystrokes)
        self.myAttack=None
        self.comment_animations=["  ","...","Expelliarmus!!","Magic is might","Arrrgh!!"]
    def nothing(self,t=400):
        Character.nothing(self,t)
    def manage_attacks(self,keystrokes,window):
        if keystrokes[self.keystrokes[4]]:
            if self.action!=PERFORM:
                self.index=0
                self.action=PERFORM
                self.myAttack=Spell(self,name="coldfire//",incantation="Expelliamus!")
