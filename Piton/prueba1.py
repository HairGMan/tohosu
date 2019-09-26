import pygame, sys
from pygame.locals import *
pygame.init()

class Bullet(pygame.sprite.Sprite):
	def __init__(self,speed,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("bullet3_tr.png")
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-8,-8)
		self.init(speed,startpos)
	
	def init(self,speed,startpos):
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.movepos = [speed[0],speed[1]]
		
	def update(self):
		self.rect.move_ip(self.movepos)
		pygame.event.pump()
		
class Player(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("placehtbx2_tr.png")
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-10,-10)
		self.state = [0,0,6]
		self.init()
		
	def init(self):
		self.rect.x = 300
		self.rect.y = 300
		self.state = [0,0,6]
		self.movepos = [0,0]

	def update(self):
		self.movepos = [(self.state[0] * self.state[2]),(self.state[1] * self.state[2])]
		newpos = self.rect.move(self.movepos)
		if area.contains(newpos):
			self.rect = newpos
			pygame.event.pump()
		
	def moveup(self):
		if self.state[1] == 1:
			self.state[1] = 0
		else:
			self.state[1] = -1
			
	def movedown(self):
		if self.state[1] == -1:
			self.state[1] = 0
		else:
			self.state[1] = 1
	
	def moveleft(self):
		if self.state[0] == 1:
			self.state[0] = 0
		else:
			self.state[0] = -1
			
	def moveright(self):
		if self.state[0] == -1:
			self.state[0] = 0
		else:
			self.state[0] = 1
		
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
player = Player()
area = screen.get_rect()
clock = pygame.time.Clock()
clock
font = pygame.font.Font("C:\Windows\Fonts\MSGOTHIC.TTC", 20)
bullet = [None,None,None,None]
bullet[0] = Bullet([0,0],[200,100])
bullet[1] = Bullet([2,4],[250,100])
bullet[2] = Bullet([-2,4],[300,100])
bullet[3] = Bullet([0,8],[350,100])
bullethtbxlist = list()
counter = 0
for i in bullet:
	bullethtbxlist.append(i.rect)

while 1:
	clock.tick_busy_loop(60)
	counter += 1
	if counter == 100:
		bullet[1].init([2,4],[250,100])
		bullet[2].init([-2,4],[300,100])
		bullet[3].init([0,8],[350,100])
		counter = 0
	for event in pygame.event.get():
	
		if event.type == pygame.QUIT: sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LSHIFT:
				player.state[2] = 2
				player.update()
			if event.key == pygame.K_UP:
					player.moveup()
			elif event.key == pygame.K_DOWN:
					player.movedown()
			elif event.key == pygame.K_LEFT:
					player.moveleft()
			elif event.key == pygame.K_RIGHT:
					player.moveright()
					
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LSHIFT:
				player.state[2] = 6
				player.update()
			if event.key == pygame.K_UP:
					player.movedown()
			elif event.key == pygame.K_DOWN:
					player.moveup()
			elif event.key == pygame.K_LEFT:
					player.moveright()
			elif event.key == pygame.K_RIGHT:
					player.moveleft()
					
	screen.fill(0)
	
	player.update()
	for i in bullet:
		i.update()
		screen.blit(i.image, i.rect)
		
	screen.blit(player.image, player.rect)
	
	fps = font.render(str(int(clock.get_fps()) - 2) + "FPS", True, (255,255,255))
	screen.blit(fps, area)
	if player.rect.collidelist(bullethtbxlist) != -1:
		player.rect.x = 300
		player.rect.y = 300
	pygame.display.flip()