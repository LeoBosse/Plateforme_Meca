#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3

from header import *

class Inventory:
	
	def __init__(self):
		self.dictionary={}
		self.size = 50
		self.rect=pygame.Rect(LONGUEUR_FENETRE/4, HAUTEUR_FENETRE/4, LONGUEUR_FENETRE/2, HAUTEUR_FENETRE/2)
		self.colour_bkg=(50, 50, 50)
		
	def Afficher(self, fenetre):
		fenetre.fill(self.colour_bkg, self.rect)	
		


class Object:

	def __init__(self, name):
		
		self.name=name
		self.atk=0
		self.defense=0
		self.cut_wood=0
		self.weight=0
		self.speed_bonus=0
		self.heal=0
		
class Weapons(Object):
	
	def __init__(self, name, atk, defense, weight):
		Object.__init__(name)
		self.atk=atk
		self.defense=defense
		self.weight=weight

class Sword(Weapons):
	
	def __init__(self, name, atk, defense, weight, cut_wood):
		Weapons.__init__(name, atk, defense, weight)
		self.cut_wood=cut_wood
		
class Shield(Weapons):
		
	def __init__(self, name, atk, defense, weight):
		Weapons.__init__(name)

class Axe(Weapons):
	
	def __init__(self, name, atk, defense, weight, cut_wood):
		Weapons.__init__(name)
		self.cut_wood=cut_wood

