#!/usr/bin/python
# -*-coding:utf-8 -*


from header import *
from items import *
from perso import *
from carte import *
from mob import *


class Game:
	
	def __init__(self, number):
		
		self.continuer = 1
		self.g=1
		self.fu=-3.5
		self.timer_fu=time.time()
		self.up=0
		self.fd=1
		self.timer_fd=time.time()
		self.down=0
		self.fl=-0.8
		self.timer_fl=time.time()
		self.left=0
		self.fr=-self.fl
		self.timer_fr=time.time()
		self.right=0
		
		self.k_control=False
		self.number=number
		
		self.endturn=True
		self.afficher_inventory=False
		
		self.path=os.getcwd()
		self.file_perso=str(self.path) + "/save/perso_" + str(self.number)
		self.file_carte=str(self.path) + "/save/carte_" + str(self.number)
		
		self.carte=Carte() #init carte
		self.perso = Perso(self.carte) #creation perso NEED carte
		#try:
			#self.Load()
		#except:
			#self.carte = Carte() #init carte
			#self.perso = Perso(self.carte) #creation perso NEED carte
			
		
		self.perso.image=pygame.image.load("images/perso.bmp")

		### Creation mobs, number calculated for optimal space
		self.hal=AIManager(self.carte)

	
	
	def Afficher(self, fenetre):
		
		self.carte.Afficher(self.perso, fenetre)
		self.hal.Afficher(self.perso, fenetre)
		self.perso.Afficher()
		if self.afficher_inventory:
			self.perso.inventory.Afficher(fenetre)
		pygame.display.flip()
		
	def PlayTurn(self):
		self.hal.PlayTurn(self.carte, self.perso)
		self.perso.Bouger(self.carte)
		self.perso.CollisionMob(self.hal.gobelins, self.hal.plants, self.hal.fireballs)
		self.GetExternalEvents()
		self.EndTurn()
	
	def EndTurn(self):
### End of turn, set timer to zero if a key's pressed too long	
		tmax=0.1
		if tmax+10*dt > time.time()-self.timer_fu > tmax and self.up==1:		self.perso.fy -= self.fu; self.up=0; #print("TMAX");
		if tmax+10*dt > time.time()-self.timer_fd > tmax and self.down==1:		self.perso.fy -= self.fd; self.down=0;# print("TMAX");
		if tmax+10*dt > time.time()-self.timer_fr > tmax and self.left==1:		self.perso.fx = 0; self.left=0; #print("TMAX");
		if tmax+10*dt > time.time()-self.timer_fl > tmax and self.right==1:		self.perso.fx = 0; self.right=0; #print("TMAX");
		if time.time()-self.perso.timer_atk > self.perso.delai_atk:				self.perso.attaque=False;
### Pause the game a while for a certain fps
		
		if self.perso.hp<=500:
			self.perso.hp += self.perso.heal
		if self.perso.Sol(self.carte)==True: self.perso.double_jump=2; ###re-init double jump if touch the ground

		if self.perso.rect.x > int(self.carte.L*LONGUEUR_SPRITE - LONGUEUR_FENETRE):
			while self.perso.rect.x > int(self.carte.L*LONGUEUR_SPRITE - LONGUEUR_FENETRE):
				self.carte.AddLign(1)
				if rand.random() > 0.95: self.hal.gobelins.append(Gobelin(self.carte, self.carte.L*LONGUEUR_SPRITE))
				elif rand.random() > 0.95: self.hal.plants.append(Plant(self.carte, self.carte.L*LONGUEUR_SPRITE))
		
		if self.carte.time%(6*dt) <= 0.1:
			for i, w in enumerate(self.carte.water):
				if w.OnScreen(self.perso):
					blocked, self.carte.water = w.Move(self.carte)
					#while not blocked and self.carte.water[i].quantity >= 0.05:
						#blocked, self.carte.water = self.carte.water[i].Move(self.carte)
			
			for i, w in enumerate(self.carte.water):
				if w.quantity < 0.05:
					del self.carte.water[i]
		
		time.sleep(dt)
		self.carte.time += dt #time.time()-self.carte.time_seed
	
	def Save(self):
		self.path=os.getcwd()
		#print(str(self.path) + "/save/perso_" + str(self.number))
		self.perso.Save(self.file_perso)
		self.carte.Save(self.file_carte)
		
		
	def Load(self):
		self.carte=Carte(self.file_carte)
		self.perso=Perso(self.carte, self.file_perso)
		
	
	def GetExternalEvents(self):
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				self.continuer=0
			elif event.type==KEYDOWN:
				if event.key==K_UP and self.perso.double_jump!=0:
					self.perso.fy += self.fu ### applied force when up key pressed
					self.perso.vy = self.fu ### always the same speed when jumping
					self.timer_fu=time.time() #### set a timer to end the force after a whle if the key stay pushed
					self.up=1 ### Means up key is active
					self.perso.double_jump-=1
				elif event.key==K_DOWN:
					self.perso.fy += self.fd
					self.timer_fd=time.time()
					self.down=1
				elif event.key==K_LEFT:
					self.perso.fx += fl
					self.perso.vx=fl
					self.timer_fl=time.time()
					self.left=1
					self.perso.direction=-1
				elif event.key==K_RIGHT:
					self.perso.fx += fr
					self.perso.vx=fr
					self.timer_fr=time.time()
					self.right=1
					self.perso.direction=1
				elif event.key==K_SPACE and time.time()-self.perso.timer_atk >self.perso.delai_atk:
					self.perso.Attaque(self.hal.gobelins, self.hal.plants, self.hal.fireballs)
					self.perso.attaque=True
					self.perso.timer_atk=time.time()
				elif event.key==K_c:
					if self.carte.ligns[spritex(self.perso.rect.centerx)].tree and spritey(self.perso.rect.bottom) == self.carte.ligns[spritex(self.perso.rect.centerx)].altitude:
						self.carte.ligns[spritex(self.perso.rect.centerx)].tree = False
						#print(self.carte.time)
						self.carte.time+=3600
						#print(self.carte.time)
						#self.perso.CutTree()
				
				elif event.key==K_LCTRL:
					self.k_control=True
				
				elif event.key==K_s and self.k_control:
					self.Save()
				
				elif event.key==K_i:
					self.afficher_inventory = not self.afficher_inventory
					self.end_turn = not self.endturn
					
			elif event.type==KEYUP:
				if event.key==K_UP and self.up==1:
					self.perso.fy -= fu
					self.timer_fu=0
					self.up=0
				elif event.key==K_DOWN and self.down==1:
					self.perso.fy -= fd
					self.timer_fd=0
					self.down=0
				elif event.key==K_LEFT and self.left==1:
					self.perso.fx -=fl
					self.perso.vx=0
					self.timer_fl=0
					self.left=0
				elif event.key==K_RIGHT and self.right==1:
					self.perso.fx -=fr
					self.perso.vx=0
					self.timer_fr=0
					self.right=0
				elif event.key==K_SPACE:
					self.perso.attaque = False
				elif event.key==K_LCTRL:
					self.k_control=False

			elif event.type==MOUSEBUTTONDOWN and event.button==1:
				l, c = self.GetSpriteClic(event.pos)
				sprite = self.carte.ligns[l].SpriteType(c)[0]
				if l != self.perso.spritex(self.perso.rect.centerx) or c != self.perso.spritey(self.perso.rect.centery):
					if sprite.material == NOIR or sprite.material == DIAMOND or sprite.material == HERBE:
						self.carte.Dig([event.pos[0]+self.perso.rect.x-LONGUEUR_FENETRE/2, event.pos[1]-HAUTEUR_FENETRE/2+self.perso.rect.y], self.perso)
					
					elif sprite.material == AIR or sprite.material == CAVE:
						self.carte.Add([event.pos[0]+self.perso.rect.x-LONGUEUR_FENETRE/2, event.pos[1]-HAUTEUR_FENETRE/2+self.perso.rect.y], self.perso, Sprite(NOIR, c))
				
				
	def GetSpriteClic(self, pos):
		x, y = pos
		sprite_x = int( ( x + self.perso.rect.x - LONGUEUR_FENETRE / 2 ) / LONGUEUR_SPRITE )
		sprite_y = NB_SPRITE_CARTE_Y - int( ( y - HAUTEUR_FENETRE / 2 + self.perso.rect.y ) / HAUTEUR_SPRITE )
		return sprite_x, sprite_y
