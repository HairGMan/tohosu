import pygame
from pygame.locals import *

class Cursor(pygame.Rect):
	def __init__(self):
		pygame.Rect.__init__(self,0,0,1,1)
	def update(self):
		self.left,self.top=pygame.mouse.get_pos()
       
class boton(pygame.sprite.Sprite):
   def __init__(self,imagen1,imagen2,x=200,y=200):
	   self.imagen_normal=imagen1
	   self.imagen_seleccion=imagen2
	   self.imagen_actual=self.imagen_normal
	   self.rect=self.imagen_actual.get_rect()
	   self.rect.left,self.rect.top=(x,y)
       
   def update(self,pantalla,cursor): 
		if cursor.colliderect(self.rect):
			self.imagen_actual=self.imagen_seleccion
		else: self.imagen_actual=self.imagen_normal 
		 
		 
		pantalla.blit(self.imagen_actual,self.rect)


from pygame.locals import *
def main():
	pygame.init()

	pantalla=pygame.display.set_mode((500,400))

	
	reloj1=pygame.time.Clock()
	reloj1
	rojo1=pygame.image.load("jugar1.png")
	rojo2=pygame.image.load("jugar2.png")
	opciones=pygame.image.load("opciones.png")
	opciones2=pygame.image.load("opciones2.png")
	salir=pygame.image.load("salir.png")
	salir2=pygame.image.load("salir2.png")
	imagenfondo=pygame.image.load("fondo.jpg")
	boton1=boton(rojo1,rojo2,200,100)
	boton2=boton(opciones,opciones2,200,200)
	boton3=boton(salir,salir2,20,350)
	cursor1=Cursor() 
	fondo=(225,225,225)

	salir=False

	while salir!=True:

		for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN
				if cursor.colliderect(boton1.rect):
					pass
			if event.type == pygame.QUIT:
				salir=True 
		 
		reloj1.tick(60) 
		pantalla.blit(imagenfondo,(0,0))
		cursor1.update()
		boton1.update(pantalla,cursor1)
		boton2.update(pantalla,cursor1)
		boton3.update(pantalla,cursor1)

		pygame.display.update()

	pygame.quit()

main()
 
