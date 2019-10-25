import pygame, sys
from pygame.locals import *
pygame.init()

class Enemy(pygame.sprite.Sprite):
	def __init__(self,startpos,pattern,patternspeed,delay):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("placeenemy_tr.png")
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-6,-6)
		self.init(startpos)
		htbxlist.append(self.rect)
		
	def init(self,startpos):
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.rect.move([0,0])
		
	def update(self):
		
		if self.rect.collidepoint(600,60):
			self.movepos = [-2,0]
		elif self.rect.collidepoint(20,60):
			self.movepos = [2,0]
			
		self.rect.move_ip(self.movepos)
		pygame.event.pump()
		
	def delete(self):
		enemies.remove(self)
		htbxlist.remove(self.rect)
		
class Bullet(pygame.sprite.Sprite):
	def __init__(self,speed,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.init(speed,startpos)
		htbxlist.append(self.rect)
		global debugbulletcount
		debugbulletcount += 1
	
	def init(self,speed,startpos):
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.movepos = [speed[0],speed[1]]
		
	def update(self):
		self.rect.move_ip(self.movepos)
		pygame.event.pump()
		if not area.contains(self.rect):
			self.delete()
		
	def delete(self):
		bullets.remove(self)
		htbxlist.remove(self.rect)
		
	def __del__(self):
		global debugbulletcount
		debugbulletcount -= 1
		
class BulletA(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("bullet3_tr.png")
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-6,-6)
		Bullet.__init__(self,speed,startpos)

class BulletB(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("bulletbig2_tr.png")
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-25,-25)
		Bullet.__init__(self,speed,startpos)
		
class Player(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("placehtbx2_tr.png")
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-10,-10)
		self.state = [0,0,6]
		self.invulntime = 0
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
		if not self.invulntime == 0:
			self.invulntime -= 1
			
	def hit(self):
			self.rect.x = 300
			self.rect.y = 300
			self.invulntime = 150

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

def createenemy(startpos,pattern,patternspeed,delay):
	enemies.append(Enemy(startpos,pattern,patternspeed,delay))
	return
	
def move():
	return

def delete(id):
	enemies[id].delete()
	return
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
player = Player()
area = screen.get_rect()
font = pygame.font.Font("MSGOTHIC.TTC", 20)
bullets = list()
htbxlist = list()
enemies = list()
