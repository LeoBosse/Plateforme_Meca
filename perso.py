#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3

from header import *
from items import *

class Perso:
	"""Classe du perso : informations, mouvement..."""
	def __init__(self, carte, load=False):
		"""init le perso, son fichier et son inventaire"""
		self.vx=0
		self.vx_max=LONGUEUR_SPRITE#/3
		self.vy=0
		self.vy_max=HAUTEUR_SPRITE#/1.5
		self.fx=0
		self.fy=g
		self.direction=1  #left to right
		self.image=pygame.image.load("images/perso.bmp").convert_alpha()
		self.image.set_colorkey((0,0,255))
		self.width=20
		self.height=40
		self.inventory=Inventory()
		
		self.double_jump=	2
		self.attaque=		False

		if load:
			self.Load(load)	
		else:
			tmp=int(NB_PIX_CARTE_X/2)
			self.rect=pygame.Rect(tmp, (NB_SPRITE_CARTE_Y-carte.ligns[int(NB_SPRITE_CARTE_X/2)].altitude)*HAUTEUR_SPRITE-self.height, self.width, self.height)
			self.hp=			500
			self.max_hp=		500
			self.timer_hit=		0
			self.atk=			20
			self.timer_atk=		0
			self.delai_atk=		0.2
			self.heal=			0.05
			self.exp=			0
			self.max_exp=		1000
			self.cave_view=		10
		self.hitbox=self.rect
	def Save(self, fichier):
		self.data_to_save={	"x":				self.rect.x,
							"y":				self.rect.y,
							"hp":				self.hp,
							"max_hp":			self.max_hp,
							"timer_hit":		self.timer_hit,
							"atk":				self.atk,
							"timer_atk":		self.timer_atk,
							"delai_atk":		self.delai_atk,
							"heal":				self.heal,
							"exp":				self.exp,
							"max_exp":			self.max_exp,
							"cave_view":		self.cave_view
						}
		with open(fichier, "w") as save_file:
			sys.stdout=save_file
			for clef, value in self.data_to_save.items():
				print("{0}:{1}".format(clef, value))
						
			sys.stdout=sys.__stdout__
		
	def Load(self, fichier):
		
		with open(fichier, "r") as load_file:
			raw=load_file.read()
		#print(raw)
		load_ligns=raw.split("\n")
		#print(load_ligns)
		self.data_to_save={}
		i=0
		lign=load_ligns[i]
		while lign!="":
		#for lign in load_ligns:
			datas=lign.split(":")
			#print(datas)
			self.data_to_save[datas[0]]=float(datas[1])
			i+=1
			lign=load_ligns[i]
		self.hp=			self.data_to_save["hp"]
		self.max_hp=		self.data_to_save["max_hp"]
		self.timer_hit=		self.data_to_save["timer_hit"]
		self.atk=			self.data_to_save["atk"]
		self.timer_atk=		self.data_to_save["timer_atk"]
		self.delai_atk=		self.data_to_save["delai_atk"]
		self.heal=			self.data_to_save["heal"]
		self.exp=			self.data_to_save["exp"]
		self.max_exp=		self.data_to_save["max_exp"]
		self.cave_view=		self.data_to_save["cave_view"]
		self.rect=pygame.Rect(int(self.data_to_save["x"]), int(self.data_to_save["y"]), self.width, self.height)

		
	
	def Bouger(self, carte):
		
		self.dx = self.fx*dt + self.vx
		if self.dx * self.direction > self.vx_max: self.dx = self.vx_max * self.direction
		
		self.nx = self.rect.x+self.dx

		self.dy = self.fy*dt + self.vy
		if abs(self.dy)>self.vy_max: self.dy = m.copysign(self.vy_max, self.dy)		
		
		self.ny = self.rect.y+self.dy
		
		coll = self.Collision(carte)
		
		self.rect.x+=self.dx
		if coll[0]==False:
			self.vx+=self.fx

		self.rect.y+=self.dy
		if coll[1]==False:
			self.vy+=self.fy
		
		
	def Collision(self, carte):
		i, j = 0,0
		collision_x=False
		collision_y=False
#Collisions avec les bords	
		if self.nx < LONGUEUR_FENETRE/2: 							
			self.dx=LONGUEUR_FENETRE/2-self.rect.x
			self.vx=0
			collision_x=True
		if self.ny < HAUTEUR_FENETRE/2: 							
			self.dy=HAUTEUR_FENETRE/2-self.rect.y
			self.vy=0
			collision_y=True
		elif self.ny > NB_PIX_CARTE_Y-self.rect.h-LONGUEUR_FENETRE/2:
			self.dy=NB_PIX_CARTE_Y-self.rect.h-LONGUEUR_FENETRE/2-self.rect.y
			self.vy=0
			collision_y=True
#Collisions avec le terrain
		s_x=self.spritex(self.rect.x)
		s_y=self.spritey(self.rect.y)
		obstacles=[]
		for i in range(-5, 5):
			for j in range (-5, 5):
				if carte.ligns[s_x+i].SpriteType(s_y+j)[0].material in [NOIR, HERBE, DIAMOND]:
					obstacles.append(pygame.Rect( (s_x+i)*LONGUEUR_SPRITE, NB_PIX_CARTE_Y-(s_y+j)*HAUTEUR_SPRITE, LONGUEUR_SPRITE, HAUTEUR_SPRITE ))
		
		for i in obstacles:
			if i.left-self.rect.w <= self.nx <= i.right and i.top-self.rect.h < self.rect.y < i.bottom and self.rect.x <= i.left-self.rect.w: 		
				self.dx=i.left-self.rect.w-self.rect.x ; self.vx=0; collision_x=True;
			elif i.left-self.rect.w <= self.nx <= i.right and i.top-self.rect.h < self.rect.y < i.bottom and self.rect.x >= i.right: 				
				self.dx=i.right-self.rect.x ; self.vx=0; collision_x=True;
			
			if i.left-self.rect.w < self.rect.x < i.right and i.top-self.rect.h <= self.ny <= i.bottom and self.rect.y <= i.top-self.rect.h: 			
				self.dy=i.top-self.rect.h-self.rect.y ; self.vy=0; collision_y=True;
			elif i.left-self.rect.w < self.rect.x < i.right and i.top-self.rect.h <= self.ny <= i.bottom and self.rect.y >= i.bottom: 				
				self.dy=i.bottom-self.rect.y ; self.vy=0; collision_y=True;

		return collision_x, collision_y

	def CollisionMob(self, gobelins, plants, fireballs):
		
		if time.time() - self.timer_hit > 1 :

			gobID=self.hitbox.collidelist(gobelins)
			if gobID != -1:
				self.hp -= gobelins[gobID].atk
				self.timer_hit=time.time()

			plID=self.hitbox.collidelist(plants)
			if plID!= -1: 	
				self.hp -= plants[plID].atk
				self.timer_hit=time.time()
			
			fireID=self.hitbox.collidelist(fireballs)
			if fireID!= -1: 	
				self.hp -= fireballs[fireID].atk
				self.timer_hit=time.time()
				del fireballs[fireID]
			
			
			
		if self.attaque==True:
			gobID=self.weapon_rect.collidelist(gobelins)
			plID=self.weapon_rect.collidelist(plants)
			fireID=self.weapon_rect.collidelist(fireballs)
			
			if gobID!= -1:
				gobelins[gobID].hp -= self.atk
				if(gobelins[gobID].hp <= 0):
					del gobelins[gobID]
					self.exp+=10
				
			if plID!= -1: 	
				plants[plID].hp -= self.atk				
				if(plants[plID].hp <= 0):
					del plants[plID]
					self.exp+=10
			
			if fireID!= -1: 	
				fireballs[fireID].hp -= self.atk				
				if(fireballs[fireID].hp <= 0):
					del fireballs[fireID]
		
	def spritex(self, x):
		return int(x/LONGUEUR_SPRITE)
	def spritey(self, y):
		return NB_SPRITE_CARTE_Y-int(y/HAUTEUR_SPRITE)
	
	def Sol(self, carte):
		sol=False
		if (carte.ligns[self.spritex(self.rect.right-1)].SpriteType(self.spritey(self.rect.bottom+2))[0].material==HERBE or carte.ligns[self.spritex(self.rect.left)].SpriteType(self.spritey(self.rect.bottom+2))[0].material==HERBE
		 or carte.ligns[self.spritex(self.rect.right-1)].SpriteType(self.spritey(self.rect.bottom+2))[0].material==NOIR or carte.ligns[self.spritex(self.rect.left)].SpriteType(self.spritey(self.rect.bottom+2))[0].material==NOIR):
				sol=True
		return sol

		
	def Afficher(self):
		
		#fenetre.blit(self.image, (int(LONGUEUR_FENETRE/2), int(HAUTEUR_FENETRE/2)))
		fenetre.fill((255, 0, 0), (int(LONGUEUR_FENETRE/2), int(HAUTEUR_FENETRE/2), self.rect.w, self.rect.h))
###Health bar	
		fenetre.fill((255, 0, 0), (20, HAUTEUR_FENETRE-50, 2*self.hp, 20))
		fenetre.fill((100, 0, 0), (20+2*self.hp, HAUTEUR_FENETRE-50, 2*(self.max_hp-self.hp), 20))
		text_HP=font.render("HP: "+str(int(self.hp)), True, (0, 0, 0), None)
		fenetre.blit(text_HP, (20+self.hp, HAUTEUR_FENETRE-48))
###EXP bar
		fenetre.fill((0, 0, 255), (20, HAUTEUR_FENETRE-25, self.exp, 20))
		fenetre.fill((0, 0, 100), (20+self.exp, HAUTEUR_FENETRE-25, (self.max_exp-self.exp), 20))
		text_HP=font.render("EXP: "+str(int(self.exp)), True, (0, 0, 0), None)
		fenetre.blit(text_HP, (20+self.max_exp/2, HAUTEUR_FENETRE-23))
		

		if(self.attaque==True):
				fenetre.fill((255, 255, 255), (LONGUEUR_FENETRE/2+self.direction*self.rect.w, HAUTEUR_FENETRE/2+self.rect.h/3, self.weapon_rect.w, self.rect.h/3))
		
		text_l=font.render("l: "+str(self.spritex(self.rect.x)), True, (255,255,255), None)
		text_c=font.render("c: "+str(self.spritey(self.rect.y)), True, (255, 255, 255), None)
		fenetre.blit(text_l, (0, 0))
		fenetre.blit(text_c, (0, font.get_linesize()))


	def Attaque(self, gobelins, plants, fireballs):
		self.weapon_rect=pygame.Rect(self.rect.x + self.direction*self.rect.w, self.rect.y, self.rect.w, self.rect.h)
		self.CollisionMob(gobelins, plants, fireballs)

		
	
	
		
