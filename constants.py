import pygame
import os
pygame.init()


font=pygame.font.Font('freesansbold.ttf',20)
fontCharacter=pygame.font.Font('freesansbold.ttf',15)
pygame.mixer.music.load(os.path.join("theme","theme.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.stop()


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
