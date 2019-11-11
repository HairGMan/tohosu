import pygame
from pygame.locals import *
pygame.init()

class Cursor(pygame.Rect):
	def __init__(self):
		pygame.Rect.__init__(self,0,0,1,1)
		
	def update(self):
		self.left,self.top=pygame.mouse.get_pos()

       
class Button(pygame.sprite.Sprite):
   def __init__(self,imagen1,imagen2,x=200,y=200):
	   self.imagen_normal=imagen1
	   self.imagen_seleccion=imagen2
	   self.imagen_actual=self.imagen_normal
	   self.rect=self.imagen_actual.get_rect()
	   self.rect.left,self.rect.top=(x,y)
   
   def select(self):
		self.imagen_actual = self.imagen_seleccion
   
   def deselect(self):
		self.imagen_actual = self.imagen_normal
		
   def update(self,pantalla,cursor): 
		if cursor.colliderect(self.rect):
			select()
		pantalla.blit(self.imagen_actual,self.rect)
	
size = width, height = 640, 360
pantalla = pygame.display.set_mode(size,RESIZABLE|DOUBLEBUF)
clock = pygame.time.Clock()
clock
buttonspritelist = list()
buttonspritelist.append([pygame.image.load("sprites/jugar1_tr.png").convert_alpha(),pygame.image.load("sprites/jugar2_tr.png").convert_alpha()])
buttonspritelist.append([pygame.image.load("sprites/jugar1_tr.png").convert_alpha(),pygame.image.load("sprites/jugar2_tr.png").convert_alpha()])
buttonspritelist.append([pygame.image.load("sprites/jugar1_tr.png").convert_alpha(),pygame.image.load("sprites/jugar2_tr.png").convert_alpha()])
buttonlist = list()
pos = [80,200]
for i in buttonspritelist:
	buttonlist.append(Button(i[0],i[1],pos[0],pos[1]))
	pos[1] += 30
cursor = Cursor() 

while 1:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
	 
	clock.tick(60)
	pantalla.fill((225,225,225))
	cursor.update()
	for i in buttonlist:
		i.update(pantalla,cursor)
	

	pygame.display.update()

