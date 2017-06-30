#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3


from header import *

class Carte:
	
	def __init__(self, load=False):
		
		self.L=NB_SPRITE_CARTE_X
		self.H=NB_SPRITE_CARTE_Y
		#self.fichier=fichier
		self.time=0
		#print(self.time_seed, self.time)
		if load:
			self.Load(load)
		else:
			self.Creer()
		
	def Creer(self):
		
		self.seed=Seed()
		self.ligns=[self.seed]
		self.water_proba=0.05
		self.water=[]
		
		for l in range(self.L):
			self.ligns.append(Lign(self.ligns[-1]))		
			if rand.random() < self.water_proba:
				for i in range(rand.randrange(4)):
					self.water.append(Water(l+1, self.ligns[-1].altitude+1+i))

#### Move the water	
		for i, w in enumerate(self.water):
			blocked, self.water = w.Move(self)
			while not blocked and self.water[i].quantity >= 0.05:
				blocked, self.water = self.water[i].Move(self)
		
		for i, w in enumerate(self.water):
			if w.quantity < 0.05:
				del self.water[i]
			

	def Save(self, fichier):
		"""Save the game in the file "fichier" """
		with open(fichier, "w") as save_file:
			sys.stdout=save_file
			print("time:{}".format(self.time))
			for i, lign in enumerate(self.ligns):
				print(lign)
					
			sys.stdout=sys.__stdout__
	
	def Load(self, fichier):
		"""Load the game from "fichier" """
		with open(fichier, "r") as load_file:
			raw=load_file.read()
		
		self.ligns=[]		
		load_ligns=raw.split("\n")
		self.time=float(load_ligns[0].split(":")[1])
		i=1
		lign=load_ligns[i]
		while lign != "":
			
			self.ligns.append(Lign(lign))
			i+=1
			lign = load_ligns[i]
	
		
	def Afficher(self, perso, fenetre):
		
		fenetre.fill((0,0, abs(int(50+200*m.sin(self.time*m.pi/(3600*24) + m.pi/4)))))
		
		x, y = perso.rect.x-LONGUEUR_FENETRE/2, perso.rect.y-HAUTEUR_FENETRE/2
		
		spritex = int(x/LONGUEUR_SPRITE)
		spritey = int((NB_PIX_CARTE_Y-y)/HAUTEUR_SPRITE)+1
		
		dx=spritex*LONGUEUR_SPRITE-x
		dy=(NB_SPRITE_CARTE_Y-spritey)*HAUTEUR_SPRITE-y
		
		pygame.draw.circle(fenetre, (255, 255, 0), 
		(int(LONGUEUR_FENETRE/2*(1-m.cos((self.time)*2*m.pi/(3600*24)))), 
		#(-(perso.rect.centerx+LONGUEUR_SPRITE/2)%LONGUEUR_SPRITE)*int((self.ligns[perso.spritex(perso.rect.centerx)+1].altitude - self.ligns[perso.spritex(perso.rect.centerx)].altitude)*float(HAUTEUR_SPRITE/LONGUEUR_SPRITE)) + 
		(NB_PIX_CARTE_Y-perso.rect.bottom - HAUTEUR_SPRITE*self.ligns[perso.spritex(perso.rect.centerx)].altitude) + 
		int(HAUTEUR_FENETRE/2*(1-m.sin((self.time)*2*m.pi/(3600*24))))), 
		
		
		30)
		pygame.draw.circle(fenetre, (255, 255, 255), 
		(int(LONGUEUR_FENETRE/2*(1+m.cos((self.time)*2*m.pi/(3600*24)))),  
		(NB_PIX_CARTE_Y-perso.rect.bottom - HAUTEUR_SPRITE*self.ligns[perso.spritex(perso.rect.centerx)].altitude) + 
		int(HAUTEUR_FENETRE/2*(1+m.sin((self.time)*2*m.pi/(3600*24))))), 
		30)
		
		i=0
		while i<=NB_SPRITE_FEN_X:
			j=0
			while j<=NB_SPRITE_FEN_Y:
				x=i*LONGUEUR_SPRITE+dx
				y=j*HAUTEUR_SPRITE+dy
				sprite=self.ligns[spritex+i].SpriteType(spritey-j)[0]
				#if sprite.material 	== AIR:		fenetre.blit(I_AIR, (x,y));
				#if sprite.material 	== AIR:		fenetre.fill((0, 0, 255-NB_SPRITE_FEN_Y+j), (x,y, LONGUEUR_SPRITE, HAUTEUR_SPRITE)); #print( int(255.*(1.-float(spritey-j)/float(NB_SPRITE_CARTE_Y))));
				
				if sprite.material == NOIR:	fenetre.blit(I_NOIR, (x,y));
				elif sprite.material == CAVE and self.ligns[spritex+i].Visibility(perso, spritey-j)==True:	fenetre.blit(I_CAVE, (x,y));
				elif sprite.material == CAVE:	fenetre.blit(I_NOIR, (x,y));
				elif sprite.material == HERBE:	fenetre.blit(I_HERBE, (x,y)); 
				
				#elif sprite.material == TREE:	fenetre.blit(I_AIR, (x,y)); fenetre.blit(sprite.image, (x, y-ARBRE_H+HAUTEUR_SPRITE)); 
				elif sprite.material == TREE:	fenetre.blit(sprite.image, (x, y-ARBRE_H+HAUTEUR_SPRITE)); 
				
							
				j+=1
			i+=1
		
		for w in self.water:
			if w.OnScreen(perso) and (w.height >= self.ligns[w.lign].altitude or self.ligns[w.lign].Visibility(perso, w.height)):
				x, y = w.AfficherXY(perso)
				fenetre.fill((10, 10, 100), (x, y, w.rect.w, w.rect.h));
				
	
	def AddLign(self, position):
		"""Add a lign at the end of the map, and add some water"""
		self.L+=1		
		if position==1:
			self.ligns.append(Lign(self.ligns[-1]))
		else:
			self.ligns.insert(0, Lign(self.ligns[0]))
		
		if rand.random() < self.water_proba:
			for i in range(rand.randrange(4)):
				self.water.append(Water(len(self.ligns)-1, self.ligns[-1].altitude+1+i))

		
		
			
	def Dig(self, pos, perso):
		distance=m.sqrt(((spritex(pos[0])-perso.spritex(perso.rect.centerx))**2)*LONGUEUR_SPRITE/HAUTEUR_SPRITE+((spritey(pos[1])-perso.spritey(perso.rect.centery))**2)*HAUTEUR_SPRITE/LONGUEUR_SPRITE)
		if distance <= 5:
			self.ligns[spritex(pos[0])].Dig(spritey(pos[1]))

	def Add(self, pos, perso, sprite):
		distance=m.sqrt(((spritex(pos[0])-perso.spritex(perso.rect.centerx))**2)*LONGUEUR_SPRITE/HAUTEUR_SPRITE+((spritey(pos[1])-perso.spritey(perso.rect.centery))**2)*HAUTEUR_SPRITE/LONGUEUR_SPRITE)
		if distance <= 5:
			self.ligns[spritex(pos[0])].Add(sprite)
			
	def MergeWater(self):
		for i, w in enumerate(self.water):
			for j, x in enumerate(self.water):
				if i < j and w.lign == x.lign and w.height == x.height:
					if w.quantity + x.quantity <=1:
						self.water[i].quantity += x.quantity
					else:
						self.water[i].quantity = 1
						self.water[j].quantity = w.quantity + x.quantity - 1
					del self.water[j]
		
	def IsSpriteWater(self, l, c):
		"""Test if a sprite has water on it and if so, resturn its place in the carte.water list. If not return -1"""
		test=-1
		i=0
		while i < len(self.water) and ( self.water[i].lign != l or self.water[i].height != c ):
			i+=1
		if i != len(self.water):
			test=i
		return test
				
	

class Lign:
	
	def __init__(self, l_pre):
		
		if type(l_pre) == type(str()):
			self.Load(l_pre)
		else:
			self.Creer(l_pre)
	
	def Creer(self, l_pre):
		self.number=l_pre.number+1
		self.length=NB_SPRITE_CARTE_Y
		
		self.cave_proba=0.05
		self.diamond_proba=0.5
		self.diamond_max_height=NB_SPRITE_CARTE_Y/5
		self.water_proba=0.1
		self.pente=0.6
		self.cave_height=13
		
		
		if rand.random() > self.pente: 	da=rand.randrange(-2, 3)
		else:						da=0
		self.altitude = l_pre.altitude+da
		while self.altitude+da >= self.length-NB_SPRITE_FEN_Y/2 or self.altitude+da <= NB_SPRITE_FEN_Y/2:
			if rand.random() > self.pente: 	da=rand.randrange(-2, 3)
			else:						da=0
		
			self.altitude = l_pre.altitude+da

		self.compo=[Noir(0)]
		
		for i, c in enumerate(l_pre.compo):
			if c.height < self.altitude and c.material == CAVE: 
				if NB_SPRITE_FEN_Y/2-10 < c.height < l_pre.altitude+20:
					if c.direction==1:
						self.compo.append(Cave(c.height+rand.randint(-3, 2)))
						while self.compo[-1].height > self.altitude:
							self.compo.append(Cave(c.height+rand.randint(-3, 2)))
						roof=c.height+rand.randint(-2, 3)+self.cave_height
						if roof < l_pre.altitude:
							self.compo.append(Noir(roof))
						else:
							self.compo.append(Air(self.altitude+1))
					else:
						self.compo.append(Cave(c.height+rand.randint(-1, 4)))
						while self.compo[-1].height > self.altitude:
							self.compo.append(Cave(c.height+rand.randint(-2, 3)))
						roof = c.height+rand.randint(-2, 3)+self.cave_height
						if roof < l_pre.altitude:
							self.compo.append(Noir(roof))
						else:
							self.compo.append(Air(self.altitude+1))
				
				elif c.height <= NB_SPRITE_FEN_Y/2-10:
					
						self.compo.append(Cave(c.height+rand.randint(0, 3)))
						while self.compo[-1].height > self.altitude:
							self.compo.append(Cave(c.height+rand.randint(0, 3)))
						roof=c.height+rand.randint(-2, 3)+self.cave_height
						if roof < l_pre.altitude:
							self.compo.append(Noir(roof))
						else:
							self.compo.append(Air(self.altitude+1))
						
				elif c.height >= altitude[l]-10:
						self.compo.append(Cave(c.height+rand.randint(-3, 0)))
						while self.compo[-1].height > self.altitude:
							self.compo.append(Cave(c.height+rand.randint(-3, 0)))
						roof=c.height+rand.randint(-2, 3)+self.cave_height
						if roof < l_pre.altitude:
							self.compo.append(Noir(roof))
						else:
							self.compo.append(Air(self.altitude+1))

		if rand.random() < self.cave_proba:
			new_cave=rand.randrange(0, self.altitude)
			self.compo.append(Cave(new_cave))
			roof=new_cave+rand.randint(-2, 3)+self.cave_height
			if roof < l_pre.altitude:
				self.compo.append(Noir(roof))
			else:
				self.compo.append(Air(self.altitude+1))
				
		if rand.random() < self.diamond_proba:
			h=rand.randrange(0, self.diamond_max_height)
			while self.SpriteType(h)[0].material != NOIR:
				h=rand.randrange(0, self.altitude)
			self.compo.append(Diamond(h, 0))
			end=h+rand.randint(0, 2)
			if end < l_pre.altitude:
				self.compo.append(Noir(end))
			else:
				self.compo.append(Air(self.altitude+1))
			
		self.compo.append(Air(self.altitude+1))
		self.compo=sorted(self.compo, key=lambda col: col.height)
		
		self.Merge()
		#print(self.compo)
		
		if self.SpriteType(self.altitude)[0].material==HERBE and rand.random()>0.8: self.tree=True
		else: self.tree=False
	
						
	def SpriteType(self, c):
		
		i=-1
		while -i <= len(self.compo) and c < self.compo[i].height:
			i-=1
		sprite=self.compo[i]
		
		if (sprite.material == NOIR and c == self.altitude) or (i < len(self.compo)-1 and sprite.material == NOIR and (self.compo[i+1].material, self.compo[i+1].height) == (CAVE, c+1) and self.compo[i+2].material == AIR):
			sprite=Grass(c)
		
		elif c == self.altitude+1 and self.tree == True:
			sprite=Tree(c)

		return sprite, i

	def InCave(self, c):
		test=False
		if self.SpriteType(c)[0].material == CAVE and c <= self.altitude:
			test=True
		return test
	
	def PlainAir(self, c):
		test=False
		sprite, i = self.SpriteType(c) 
		if sprite.material==CAVE and self.compo[i+1].material == AIR:
			test=True
		return test
		
	def Visibility(self, perso, c):
		test=False
		sprite, i = self.SpriteType(c)
		distance=m.sqrt(((self.number-perso.spritex(perso.rect.centerx))**2)*LONGUEUR_SPRITE/HAUTEUR_SPRITE+((c-perso.spritey(perso.rect.centery))**2)*HAUTEUR_SPRITE/LONGUEUR_SPRITE)
##BUGGED
		#if self.PlainAir(c)==True or (self.InCave(perso.spritey(perso.rect.centery)) and distance<=perso.cave_view):
		if self.PlainAir(c)==True or (distance<=perso.cave_view):
			test=True
		
		return test

	def Dig(self, c):
		"""Take off a sprite in the lign"""
		sprite, i=self.SpriteType(c)
		if sprite.material in [NOIR, DIAMOND, HERBE]:
			#st = self.SpriteType(c+1)[0].__class__(c+1)
			st = Sprite(self.SpriteType(c+1)[0].material, c+1)
			#st = self.SpriteType(c+1)[0]
			#st.height=c+1
			self.compo.append(Cave(c))
			if st.material==TREE:
				self.compo.append(Air(c+1))
			else:
				self.compo.append(st)
			self.compo=sorted(self.compo, key=lambda col: col.height)
			if c == self.altitude:
				self.tree=False
			self.Merge()
					
	def Add(self, good_sprite_class):
		
		h=good_sprite_class.height
		
		#tmp = self.SpriteType(h+1)[0].__class__(h+1)
		tmp = Sprite(self.SpriteType(h+1)[0].material, h+1)
		#tmp.height = h + 1
		#if h < self.altitude - 1 and self.SpriteType(h+1)[0]:
			#tmp = Sprite(CAVE, h+1)
		#elif h < self.altitude - 1:
		
		self.compo.append(good_sprite_class)
		self.compo.append(tmp)

		self.compo=sorted(self.compo, key=lambda col: col.height)
		self.Merge()
					
	def Merge(self):
		"""Merge two different caves that join        SHOULD TAKE A LOOK AGAIN...."""
		for i, sprite in enumerate(self.compo):
			if i < len(self.compo)-1 and sprite.material==self.compo[i+1].material==CAVE:
				del self.compo[i+1]
			elif i < len(self.compo)-1 and sprite.material==self.compo[i+1].material==NOIR:
				del self.compo[1]

	
	def __repr__(self):
		str_sprite=""
		for sprite in self.compo:
			str_sprite = str_sprite + ":" + str(sprite)
		return("{0}:{1}:{3}{2}".format(self.number, self.altitude, str_sprite, int(self.tree)))
	
	
	def Load(self, string):
		"""load a lign from  string o fthe save file"""
		datas=string.split(":")
		self.number=int(datas[0])
		self.altitude=int(datas[1])
		self.tree=int(datas[2])
		self.compo=[]
		
		for i, sprite in enumerate(datas):
			if i >2:
				t=sprite.split(",")
				mat=int(t[0])
				h=int(t[1])
				if mat == AIR:
					self.compo.append(Air(h))
				if mat == CAVE:
					self.compo.append(Cave(h))
				if mat == NOIR:
					self.compo.append(Noir(h))
				if mat == HERBE:
					self.compo.append(Grass(h))
				if mat == DIAMOND:
					self.compo.append(Diamond(h, 0))
				#if mat == TREE:
					#self.compo.append(Tree(h))
			
		
class Seed(Lign):
		
	def __init__(self):
		self.number=0
		self.length=NB_SPRITE_CARTE_Y
		self.altitude=int(self.length/2)
		self.compo=[Noir(0), Air(self.altitude+1)]
		self.tree=False


class Sprite:
	
	def __init__(self, sprite_type, height, colour=(0,0,0)):
		self.material = sprite_type
		self.height = height
		self.colour = colour
	
	
	def __repr__(self):
		return "{0},{1}".format(self.material, self.height)
	
class Noir(Sprite):
	
	def __init__(self, height):
		Sprite.__init__(self, NOIR, height,(25,25,0))

class Cave(Sprite):

	def __init__(self, height):
		Sprite.__init__(self, CAVE, height, (100,100,0))
		self.direction=rand.choice([-1, 1])
		
class Grass(Sprite):
	
	def __init__(self, height):
		Sprite.__init__(self, HERBE, height, (0,255,0))
		self.colour_grass=(0,255,0)
		self.colour_noir=(25,25,0)
		
class Air(Sprite):
	
	def __init__(self, height):
		Sprite.__init__(self, AIR, height, (0,0,255))
		

class Diamond(Sprite):
	
	def __init__(self, height, repeat):
		Sprite.__init__(self, DIAMOND, height, (0, 100, 100))
		self.repeated=repeat
		
class Tree(Sprite):
	
	def __init__(self, height):
		Sprite.__init__(self, TREE, height, (0, 0, 255))
		self.image=I_ARBRE

class Water():
	
	def __init__(self, lign, height, quantity=1):
		self.lign=lign
		self.height=height
		self.quantity=float(quantity)
		self.last_move=""
		self.rect=pygame.Rect(self.lign*LONGUEUR_SPRITE, int((NB_SPRITE_CARTE_Y - self.height + 1 - self.quantity) * HAUTEUR_SPRITE ),   LONGUEUR_SPRITE, HAUTEUR_SPRITE*self.quantity)
		self.rect=pygame.Rect(self.lign*LONGUEUR_SPRITE, int((NB_SPRITE_CARTE_Y - self.height + 1 - self.quantity) * HAUTEUR_SPRITE ), LONGUEUR_SPRITE, HAUTEUR_SPRITE*self.quantity)
	
	def Move(self, carte):
		try:
			bottom_type	=	carte.ligns[self.lign].SpriteType(self.height-1)[0].material
		except:
			bottom_type	=	NOIR
		try:
			right_type	=	carte.ligns[self.lign+1].SpriteType(self.height)[0].material
		except:
			right_type	=	NOIR
		try:
			left_type	=	carte.ligns[self.lign-1].SpriteType(self.height)[0].material
		except:
			left_type	=	NOIR
		
		list_permeable=[CAVE, AIR, TREE]
		
		try_water_b = carte.IsSpriteWater(self.lign, self.height-1)
		move_bottom		=	bottom_type in list_permeable  
		
		try_water_r = carte.IsSpriteWater(self.lign+1, self.height)
		move_right		=	right_type in list_permeable   
		
		try_water_l = carte.IsSpriteWater(self.lign-1, self.height)
		move_left		=	left_type in list_permeable   

		#new=[]
		block=True
		
		if move_bottom and try_water_b == -1:
			self.height -= 1
			block=False
		
		elif move_bottom and carte.water[try_water_b].quantity != 1:
			carte.water[try_water_b].quantity += self.quantity
			if carte.water[try_water_b].quantity >= 1:
				self.quantity = carte.water[try_water_b].quantity - 1
				carte.water[try_water_b].quantity = 1
			else: self.quantity = 0

		elif move_right and not move_left and try_water_r == -1:
			self.quantity = self.quantity / 2
			carte.water.append(Water(self.lign + 1, self.height, self.quantity))
			#print("flop")
			
		elif move_left and not move_right and try_water_l == -1:
			self.quantity = self.quantity/2
			carte.water.append(Water(self.lign - 1, self.height, self.quantity))
			#print("flap")
		
		elif move_left and move_right and try_water_l == -1 and try_water_r == -1:
			self.quantity = self.quantity/3
			carte.water.append(Water(self.lign + 1, self.height, self.quantity))
			self.lign += 1

		elif move_right and not move_left and try_water_r != -1:
			self.quantity						= (self.quantity + carte.water[try_water_r].quantity)/2
			carte.water[try_water_r].quantity 	= self.quantity
		
		elif move_left and not move_right and try_water_l != -1:
			self.quantity 						= (self.quantity + carte.water[try_water_l].quantity)/2
			carte.water[try_water_l].quantity 	= self.quantity

		elif move_left and move_right and try_water_r != -1 and try_water_l == -1:
			self.quantity 						= (self.quantity + carte.water[try_water_r].quantity)/3
			carte.water.append(Water(self.lign-1, self.height, self.quantity))
			carte.water[try_water_r].quantity 	= self.quantity

		elif move_left and move_right and try_water_l != -1 and try_water_r == -1:
			self.quantity 						= (self.quantity + carte.water[try_water_l].quantity)/3
			carte.water.append(Water(self.lign+1, self.height, self.quantity))
			carte.water[try_water_l].quantity 	= self.quantity
		
		elif move_left and move_right and try_water_l != -1 and try_water_r != -1:
			self.quantity 						= (self.quantity + carte.water[try_water_l].quantity + carte.water[try_water_r].quantity)/3
			carte.water[try_water_l].quantity 	= self.quantity
			carte.water[try_water_r].quantity 	= self.quantity

		self.rect=pygame.Rect(self.lign*LONGUEUR_SPRITE, int((NB_SPRITE_CARTE_Y - self.height + 1 - self.quantity) * HAUTEUR_SPRITE ), LONGUEUR_SPRITE, HAUTEUR_SPRITE*self.quantity)
		
		return block, carte.water

	def OnScreen(self, perso):
		if int(perso.rect.x-LONGUEUR_FENETRE) < self.rect.centerx < int(perso.rect.x+LONGUEUR_FENETRE) and int(perso.rect.y-HAUTEUR_FENETRE) < self.rect.centery < int(perso.rect.y+HAUTEUR_FENETRE):
			on_screen=True
		else: on_screen=False;
		return on_screen
		
	
	def AfficherXY(self, perso):
		
		x = self.rect.x - perso.rect.x + LONGUEUR_FENETRE/2
		y = self.rect.y - perso.rect.y + HAUTEUR_FENETRE/2
		return x, y
		
		
	def __repr__(self):
		return "{0}:{1}:{2}".format(self.lign, self.height, self.quantity)





