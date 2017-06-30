#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3


from header import *

class AIManager:
	
	def __init__(self, carte):
		self.gobelins=[]
		self.plants=[]
		for i in range(int(NB_SPRITE_CARTE_X/NB_SPRITE_FEN_X)):
			self.gobelins.append(Gobelin(carte))
			self.plants.append(Plant(carte))
		self.fireballs=[]

	
	def Afficher(self, perso, fenetre):
		
		for gob in self.gobelins:		###gere mobs
			if(gob.OnScreen(perso)==True):
				#fenetre.fill((gob.colour), (int(LONGUEUR_FENETRE/2) - perso.rect.x + gob.rect.x ,  int(HAUTEUR_FENETRE/2) - perso.rect.y + gob.rect.y, gob.rect.w, gob.rect.h));
				fenetre.blit(gob.image, (int(LONGUEUR_FENETRE/2) - perso.rect.x + gob.rect.x ,  int(HAUTEUR_FENETRE/2) - perso.rect.y + gob.rect.y))
		for pl in self.plants:
			if(pl.OnScreen(perso)==True):
				fenetre.fill((pl.colour), (int(LONGUEUR_FENETRE/2) - perso.rect.x + pl.rect.x ,  int(HAUTEUR_FENETRE/2) - perso.rect.y + pl.rect.y, pl.rect.w, pl.rect.h));
		for i,fire in enumerate(self.fireballs):
			if fire.OnScreen(perso)==True :#and fire.Collision(carte) is False:
				fire.Afficher(fenetre, perso)
	
	def PlayTurn(self, carte, perso):
		for gob in self.gobelins:		###gere mobs
			if(gob.OnScreen(perso)==True):
				gob.Bouger(carte)
		for pl in self.plants:
			if(pl.OnScreen(perso)==True):
				pl.Attaque(self.fireballs, perso)
		for i,fire in enumerate(self.fireballs):
			if fire.OnScreen(perso)==True :#and fire.Collision(carte) is False:
				fire.Bouger()
			else: del self.fireballs[i]

		
class Gobelin():
	
	def __init__(self, carte, x=-1):
		if x is -1:
			tmp=rand.randrange(2, NB_PIX_CARTE_X-2)
		else: 
			tmp=x
		self.rect=pygame.Rect(tmp, (NB_SPRITE_CARTE_Y-carte.ligns[int(tmp/LONGUEUR_SPRITE)].altitude)*HAUTEUR_SPRITE-30, 30, 30)
		
		self.image=pygame.image.load("images/mob.bmp").convert()
		self.image.set_colorkey((0, 0, 255))
		
		#self.colour=(100,55,55)
		self.vx=rand.randrange(-4, 4)
		self.vx_max=LONGUEUR_SPRITE/4
		self.vy=0
		self.vy_max=HAUTEUR_SPRITE/2
		self.fx=0
		self.fy=g
		
		self.hp=100
		self.atk=10

	def Bouger(self, carte):
		
		self.dx = self.fx*dt + self.vx
		self.nx = self.rect.x + self.dx
		
		self.dy = self.fy*dt + self.vy
		self.ny = self.rect.y + self.dy
		
		coll = self.Collision(carte)
		self.rect.x+=self.dx
		
		self.rect.y+=self.dy
		if coll[1] is False:
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
		elif self.nx > carte.L*LONGUEUR_SPRITE-self.rect.w: 	
			self.dx=NB_PIX_CARTE_X-self.rect.w-LONGUEUR_FENETRE/2-self.rect.x
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
		for i in range(-10, 10):
			for j in range (-10, 10):
				if carte.ligns[s_x+i].SpriteType(s_y+j)[0].material in [NOIR, HERBE]:
					obstacles.append(pygame.Rect( (s_x+i)*LONGUEUR_SPRITE, NB_PIX_CARTE_Y-(s_y+j)*HAUTEUR_SPRITE, LONGUEUR_SPRITE, HAUTEUR_SPRITE ))
		
		for i in obstacles:
			if i.left-self.rect.w <= self.nx <= i.right and i.top-self.rect.h < self.rect.y < i.bottom and self.rect.x <= i.left-self.rect.w: 		
				self.dx=i.left-self.rect.w-self.rect.x ; self.vx=-self.vx; collision_x=True;
			elif i.left-self.rect.w <= self.nx <= i.right and i.top-self.rect.h < self.rect.y < i.bottom and self.rect.x >= i.right: 				
				self.dx=i.right-self.rect.x ; self.vx=-self.vx; collision_x=True;
			
			if i.left-self.rect.w < self.rect.x < i.right and i.top-self.rect.h <= self.ny <= i.bottom and self.rect.y <= i.top-self.rect.h: 			
				self.dy=i.top-self.rect.h-self.rect.y ; self.vy=0; collision_y=True;
			elif i.left-self.rect.w < self.rect.x < i.right and i.top-self.rect.h <= self.ny <= i.bottom and self.rect.y >= i.bottom: 				
				self.dy=i.bottom-self.rect.y ; self.vy=0; collision_y=True;

		return collision_x, collision_y



	def spritex(self, x):
		return int(x/LONGUEUR_SPRITE)
	def spritey(self, y):
		return NB_SPRITE_CARTE_Y-int(y/HAUTEUR_SPRITE)

	
	def Sol(self, carte):
		sol=False
		if (carte.GetSpriteType(self.spritex(self.rect.right),self.spritey(self.rect.bottom+2)) is HERBE or carte.GetSpriteType(self.spritex(self.rect.left),self.spritey(self.rect.bottom+2)) is HERBE
		 or carte.GetSpriteType(self.spritex(self.rect.right),self.spritey(self.rect.bottom+2)) is NOIR or carte.GetSpriteType(self.spritex(self.rect.left),self.spritey(self.rect.bottom+2)) is NOIR):
				sol=True
		return sol


	def OnScreen(self, perso):
		if(int(perso.rect.x-LONGUEUR_FENETRE/2) < self.rect.x < int(perso.rect.x+LONGUEUR_FENETRE/2)):
			on_screen=True
		else: on_screen=False
		
		return on_screen

class Plant:
	def __init__(self, carte, x=-1):
		if x is -1:
			tmp=rand.randrange(2, NB_PIX_CARTE_X-2)
		else: 
			tmp=x
		self.rect=pygame.Rect(tmp, (NB_SPRITE_CARTE_Y-carte.ligns[int(tmp/LONGUEUR_SPRITE)].altitude)*HAUTEUR_SPRITE-30, 10, 30)
		self.colour=(10,155,55)
		self.hp=50
		self.atk=5
		self.atk_freq=5
		
		self.timer_atk=0

	def OnScreen(self, perso):
		if(int(perso.rect.x-LONGUEUR_FENETRE/2) < self.rect.x < int(perso.rect.x+LONGUEUR_FENETRE/2)):
			on_screen=True
		else: on_screen=False
		
		return on_screen
	
	def Attaque(self, fireballs, perso):
		if time.time()-self.timer_atk > self.atk_freq:
			fireballs.append(Fireball(self.rect.centerx, self.rect.centery, perso))
			self.timer_atk=time.time()
		
		
class Fireball:
	
	def __init__(self, x, y, perso):
		self.speed=5
		self.radius=10
		self.rect=pygame.Rect(x-self.radius*m.sqrt(2), y-self.radius*m.sqrt(2), 2*self.radius, 2*self.radius)
		self.nx=self.rect.centerx
		self.ny=self.rect.centery

		self.colour=(100, 0, 0)
		self.atk=10
		self.hp=1
		
		self.vx= self.speed*(perso.rect.centerx - self.rect.centerx) / m.sqrt( (perso.rect.centerx - self.rect.centerx)**2 + (perso.rect.centery - self.rect.centery)**2 ) 
		self.vy= self.speed*(perso.rect.centery - self.rect.centery) / m.sqrt( (perso.rect.centerx - self.rect.centerx)**2 + (perso.rect.centery - self.rect.centery)**2 ) 
		

	def Afficher(self, fenetre, perso):
		pygame.draw.circle(fenetre, self.colour, (int(LONGUEUR_FENETRE/2) - perso.rect.centerx + self.rect.centerx ,  int(HAUTEUR_FENETRE/2) - perso.rect.centery + self.rect.centery), self.radius)
		
	def Bouger(self):
		

		self.rect.centerx+=int(self.vx)
		self.rect.centery+=int(self.vy)
		self.nx=self.rect.centerx
		self.ny=self.rect.centery
	
	def OnScreen(self, perso):
		if int(perso.rect.x-LONGUEUR_FENETRE) < self.rect.centerx < int(perso.rect.x+LONGUEUR_FENETRE) and int(perso.rect.y-HAUTEUR_FENETRE) < self.rect.centery < int(perso.rect.y+HAUTEUR_FENETRE):
			on_screen=True
		else: on_screen=False;
		return on_screen

	def Collision(self, carte):
		collision=False

		s_x=self.spritex(self.rect.centerx)
		s_y=self.spritey(self.rect.centery)
		obstacles=[]
		for i in range(-2, 2):
			for j in range (-2, 2):
				if carte.GetSpriteType(s_x+i,s_y+j) in [NOIR, HERBE]:
					obstacles.append(pygame.Rect( (s_x+i)*LONGUEUR_SPRITE, NB_PIX_CARTE_Y-(s_y+j)*HAUTEUR_SPRITE, LONGUEUR_SPRITE, HAUTEUR_SPRITE ))
		
		for i in obstacles:
			if i.left-self.rect.w <= self.nx <= i.right and i.top-self.rect.h < self.rect.y < i.bottom and self.rect.x <= i.left-self.rect.w: 		
				collision=True;
			elif i.left-self.rect.w <= self.nx <= i.right and i.top-self.rect.h < self.rect.y < i.bottom and self.rect.x >= i.right: 				
				ollision=True;
			
			if i.left-self.rect.w < self.rect.x < i.right and i.top-self.rect.h <= self.ny <= i.bottom and self.rect.y <= i.top-self.rect.h: 			
				collision=True;
			elif i.left-self.rect.w < self.rect.x < i.right and i.top-self.rect.h <= self.ny <= i.bottom and self.rect.y >= i.bottom: 				
				collision=True;

		return collision

		
	def spritex(self, x):
		return int(x/LONGUEUR_SPRITE)
	def spritey(self, y):
		return NB_SPRITE_CARTE_Y-int(y/HAUTEUR_SPRITE)
		
		
		
