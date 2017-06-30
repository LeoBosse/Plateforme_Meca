#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3

from header import *
from items import *
from perso import *
from carte import *
from mob import *
from game import *


font=pygame.font.SysFont(pygame.font.get_default_font(), 25)

fenetre = pygame.display.set_mode((LONGUEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Plateforme")

text_titre="WELCOME!"
text_game1="GAME 1"
text_game2="GAME 2"
text_game3="GAME 3"

surf_titre=font.render(text_titre, True, (255,255,255), None)
s_titre=font.size(text_titre)
surf_game1=font.render(text_game1, True, (255, 255, 255), None)
s_game1=font.size(text_game1)
surf_game2=font.render(text_game2, True, (255, 255, 255), None)
s_game2=font.size(text_game2)
surf_game3=font.render(text_game3, True, (255, 255, 255), None)
s_game3=font.size(text_game3)
continuer_fenetre=True

while continuer_fenetre:
	fenetre.blit(surf_titre, ((LONGUEUR_FENETRE-s_titre[0])/2, 100))
	fenetre.blit(surf_game1, ((LONGUEUR_FENETRE-s_game1[0])/2, 100+font.get_linesize()))
	fenetre.blit(surf_game2, ((LONGUEUR_FENETRE-s_game2[0])/2, 100+2*font.get_linesize()))
	fenetre.blit(surf_game3, ((LONGUEUR_FENETRE-s_game3[0])/2, 100+3*font.get_linesize()))
	pygame.display.flip()

	continuer=1
	wait_event=True
	play=False
	while wait_event:
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				continuer_fenetre=False
				wait_event=False
			elif event.type==KEYDOWN:
				if event.key==K_1 or event.key==K_a:
					game_number=1
					wait_event=False
					play=True
				elif event.key==K_2 or event.key==K_b:
					game_number=2
					wait_event=False
					play=True
				elif event.key==K_3 or event.key==K_c:
					game_number=3
					wait_event=False
					play=True

	if play:				
		game=Game(game_number)
		while game.continuer:
			game.PlayTurn()
			game.Afficher(fenetre)
	
pygame.quit()

