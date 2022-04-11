# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 08:56:30 2019

@author: _Nprime496_
"""
import os
import pygame
from pygame.locals import *
from constants import *
from projectile import *
from character import *
from utils import *
import random

#datas used in the program below
compteur=0

    
def manage_characters_projectiles(characters,projectiles):
    for p in projectiles:#and type(c) is not Wizard:
        for c in characters:
            
            if p.creator!=c and p.rect.colliderect(c.rect) and c.action!=DIE:

                p.setDamage(c)
                try:
                    projectiles.remove(p)
                except ValueError:#this happens when two characters are at the same place when the projectile hit 
                    pass


def manage_characters_collision(characters,c):#when a character c has thrown an attack
    for c2 in characters:
        if c2!=c and c.rect.colliderect(c2.rect):#if one anather character is nearby, it get the damages
            if ((c.direction is False and c2.pos[0]<c.pos[0] ) or (c.direction is True and c2.pos[0]>c.pos[0])) and c2.action!=DIE :#if they are face to face
                c2.receiveInjuries()#get damages
                break#the attack is over          




        
def afficher(window,character):
    character.draw(window)    #write the name of the character and his life and mana



#main program
def main():
    player2_keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_d,pygame.K_a,pygame.K_s]
    player1_keys=[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT,pygame.K_SPACE]
    
    #screen    
    window=pygame.display.set_mode((WIDTH,LENGTH))
    pygame.display.set_caption("Wizard Fight 496")#title of the game... don't blame me, I was kinda in hurry
    backgound=pygame.image.load(os.path.join("backgrounds",f"{random.randint(1,6)}.jpg")).convert()#the backgrounds are named like 1.png,2.png,...6.png in backgrounds directory
    backgound=pygame.transform.scale(backgound,(WIDTH,LENGTH))#the background is scaled to the size of the screen
    
    all_characters=[Goblin(),Wizard(),Hunter(),Orc(),Knight()]#this list contains all the characters on the screen
    
    player1=random.choice(all_characters).setKeystrokes(player1_keys)
    all_characters.remove(player1)
    list_characters=[player1,random.choice(all_characters).setKeystrokes(player2_keys)]
    #list_life_bar=[(LifeBar(,list_characters[1]),(LifeBar(length=200,pos=(-20,30)),list_characters[0])]
    list_life_bar=[LifeBar(elt) for elt in list_characters]#this list contains all the character's life bar and will be used for the update of those
    #list_energy_bar=[LifeBar(elt) for elt in list_characters]#this list contains all the character's life bar and will be used for the update of those

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

print("THANKS FOR GAMING, for any suggestion contact me : https://www.github.com/nprime496")