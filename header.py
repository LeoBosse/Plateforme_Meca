#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3
from __future__ import division


import os as os
import sys as sys
import pygame as pygame
from pygame.locals import *

import math as m
import time as time
import random as rand

a=pygame.init()[1]
while a!=0:
	a=pygame.init()[1]

font=pygame.font.SysFont(pygame.font.get_default_font(), 25)

Info=pygame.display.Info()

HAUTEUR_FENETRE=Info.current_h-50
LONGUEUR_FENETRE=Info.current_w

fenetre = pygame.display.set_mode((LONGUEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Plateforme")


LONGUEUR_SPRITE= 40
HAUTEUR_SPRITE=40

NB_SPRITE_FEN_X = int(LONGUEUR_FENETRE/LONGUEUR_SPRITE+1)
NB_SPRITE_FEN_Y	= int(HAUTEUR_FENETRE/HAUTEUR_SPRITE+1)

NB_SPRITE_CARTE_X = 1000
NB_SPRITE_CARTE_Y = 1000

NB_PIX_CARTE_X = NB_SPRITE_CARTE_X*LONGUEUR_SPRITE
NB_PIX_CARTE_Y = NB_SPRITE_CARTE_Y*HAUTEUR_SPRITE

NB_PIX_FEN_X   = NB_SPRITE_FEN_X*LONGUEUR_SPRITE
NB_PIX_FEN_Y   = NB_SPRITE_FEN_Y*HAUTEUR_SPRITE



NOIR=0
AIR=1
HERBE=2
TREE=3
ARBRE_H=57
CAVE=4
DIAMOND=5
WATER=6

I_HERBE=pygame.image.load("images/herbe.bmp").convert()
I_AIR=pygame.image.load("images/air.bmp").convert()
I_NOIR=pygame.image.load("images/noir.bmp").convert()
I_ARBRE=pygame.image.load("images/arbre.bmp").convert()
I_ARBRE.set_colorkey((0, 0, 255))
I_CAVE=pygame.image.load("images/terre.bmp").convert()
I_MOB=pygame.image.load("images/mob.bmp").convert()
I_MOB.set_colorkey((0, 0, 255))

#I_ARBRE=pygame.image.load("images/arbre.png")

FLOOR=0
ROOF=1


fps=50
dt=1/fps

continuer = 1
g=1
fu=-3.5
timer_fu=time.time()
up=0
fd=1
timer_fd=time.time()
down=0
fl=-0.8
timer_fl=time.time()
left=0
fr=-fl
timer_fr=time.time()
right=0


def spritex(x):
	return int(x/LONGUEUR_SPRITE)
def spritey(y):
	return NB_SPRITE_CARTE_Y-int(y/HAUTEUR_SPRITE)
