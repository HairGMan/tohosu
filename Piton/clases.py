import pygame, sys, math, cmath
from math import *
from cmath import *
from pygame.locals import *
pygame.init()

currentenemyid = 0
debugbulletcount = 0

class Enemy(pygame.sprite.Sprite):
	def __init__(self,startpos,pattern,bullettype,patternspeed,bulletspeed,bulletspeedfrac,delay):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("sprites/placeenemysmall_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-4,-4)
		self.offset = offx, offy = 2, 2
		self.imgpos = (self.rect.x - self.offset[0], self.rect.y - self.offset[1])
		self.init(startpos)
		htbxlist.append(self.rect)
		self.movepos = (0,0)
		self.moveclock = 0
		self.shootclock = delay
		self.pattern = pattern
		self.bullettype = bullettype
		self.patternspeed = patternspeed
		self.bulletspeed = float(bulletspeed) / bulletspeedfrac
		global currentenemyid
		self.id = currentenemyid
		currentenemyid += 1
		self.angleclock = 0.0
		self.angleclockint = 0.0
		self.spirals = 1
		self.patterndict = {
			1:	self.PatternA,
			2:	self.PatternB,
			3:	self.PatternC,
			4:	self.PatternD
		}
		self.bulletdict = {
			1:	BulletA,
			2:	BulletB,
			3:	BulletC,
			4:	BulletD
		}
		
	def init(self,startpos):
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.rect.move([0,0])
		
	def move(self,xy,steps):
		self.moveclock = steps
		self.movepos = xy
		
	def shoot(self):
		if self.pattern != 0:
			self.patterndict[self.pattern]()
		self.shootclock = self.patternspeed
		
	def PatternA(self):
		bullets.append(self.bulletdict[self.bullettype]((0.0,float(self.bulletspeed)),(float(self.rect.x),float(self.rect.y))))
		
	def PatternB(self):
		bullets.append(self.bulletdict[self.bullettype]([1,self.bulletspeed],(self.rect.x,self.rect.y)))
		bullets.append(self.bulletdict[self.bullettype]([-1,self.bulletspeed],(self.rect.x,self.rect.y)))
		
	def PatternC(self):
		bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed)),(float(self.rect.x),float(self.rect.y))))
		
	def PatternD(self):
		for s in range(self.spirals):
			bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed,self.angleclock+360/self.spirals*s)),(float(self.rect.x),float(self.rect.y))))
		self.angleclock += self.angleclockint % 360

	def update(self):
		if self.shootclock == 0:
			self.shoot()
		elif self.shootclock > 0:
			self.shootclock -= 1
		if self.moveclock == 0:
			self.movepos = (0,0)
		else:
			self.moveclock -= 1
		self.rect.move_ip(self.movepos)
		self.imgpos = (self.rect.x - self.offset[0], self.rect.y - self.offset[1])
		pygame.event.pump()
		
	def delete(self):
		enemies.remove(self)
		htbxlist.remove(self.rect)
		
class Bullet(pygame.sprite.Sprite):
	def __init__(self,speed,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.init(speed,startpos)
		htbxlist.append(self.rect)
		self.imgpos = (self.rect.x - self.offset[0], self.rect.y - self.offset[1])
		self.uffeable = True
		global debugbulletcount
		debugbulletcount += 1
	
	def init(self,speed,startpos):
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.movepos = speed
		self.vectpos = [self.rect.x,self.rect.y]
		
	def update(self):
		self.vectpos[0] += self.movepos[0]
		self.vectpos[1] += self.movepos[1]
		self.rect.move_ip((self.vectpos[0] - self.rect.x,self.vectpos[1] - self.rect.y))
		self.imgpos = (self.rect.x - self.offset[0], self.rect.y - self.offset[1])
		pygame.event.pump()
		if not bulletliferect.contains(self.rect):
			self.delete()
		
	def delete(self):
		bullets.remove(self)
		if self.rect in htbxlist:
			htbxlist.remove(self.rect)
		
	def __del__(self):
		global debugbulletcount
		debugbulletcount -= 1
		
class BulletA(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("sprites/bullet4_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-4,-4)
		self.offset = offx, offy = 2, 2
		Bullet.__init__(self,speed,startpos)

class BulletB(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("sprites/bulletbig3_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-12,-12)
		self.offset = offx, offy = 6, 6
		Bullet.__init__(self,speed,startpos)
		
class BulletC(Bullet):
	def __init__(self,speed,startpos):
		self.baseimage = pygame.image.load("sprites/bullet6_p_tr.png").convert_alpha()
		self.image = pygame.transform.rotate(self.baseimage,dirtoangle(*speed))
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-10,-10)
		self.offset = offx, offy = 5, 5
		Bullet.__init__(self,speed,startpos)

class BulletD(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("sprites/bullet5_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-4,-4)
		self.offset = offx, offy = 2, 2
		Bullet.__init__(self,speed,startpos)
		
class Player(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("sprites/placehtbxsmall_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-4,-4)
		self.offset = offx, offy = 2, 3
		self.imgpos = (self.rect.x - self.offset[0], self.rect.y - self.offset[1])
		self.uffhtbx = self.rect.copy()
		self.uffhtbx.inflate_ip(10,10)
		self.invulntime = 0
		self.init()
		
	def init(self):
		self.rect.x = 200
		self.rect.y = 300
		self.state = [0,0,3]
		self.movepos = [0,0]

	def update(self):
		self.movepos = [(self.state[0] * self.state[2]),(self.state[1] * self.state[2])]
		newpos = self.rect.move(self.movepos)
		if playrect.contains(newpos):
			self.rect = newpos
			self.uffhtbx = newpos.inflate(10,10)
			self.imgpos = (self.rect.x - self.offset[0], self.rect.y - self.offset[1])
			pygame.event.pump()
		if not self.invulntime == 0:
			self.invulntime -= 1
			
	def hit(self):
			self.rect.x = 200
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

def createenemy(startposx,startposy,pattern,bullettype,patternspeed,bulletspeed,bulletspeedfrac,delay):
	startpos = (startposx,startposy)
	enemies.append(Enemy(startpos,pattern,bullettype,patternspeed,bulletspeed,bulletspeedfrac,delay))
	return

def move(id,x,y,steps,mode):
	xy = (x,y)
	for e in enemies:
		if e.id == id:
			e.move(xy,steps)
	return

def delete(id):
	for e in enemies:
		if e.id == id:
			e.delete()
	return

def switchshot(id,pattern,bullettype = 1,special = 0,special2 = 0):
	for e in enemies:
		if e.id == id:
			e.pattern = pattern
			e.bullettype = bullettype
			e.shootclock = 0
			if pattern == 4:
				e.angleclockint = float(special)
				e.spirals = special2
	
def trackplayer(enemy,player,speed):
	distance = complex(float((enemy.rect.x - player.rect.x)),float((enemy.rect.y - player.rect.y)))
	b_phase = phase(distance)
	bulletdirection = rect(-speed,b_phase)
	return bulletdirection.real, bulletdirection.imag
	
def angletodir(speed,angle):
	bulletdirection = rect(speed,(angle/180*pi))
	return bulletdirection.real, bulletdirection.imag
	
def dirtoangle(dirx,diry):
	if dirx == 0: return 90
	bulletangle = -atan2(diry,dirx) / pi * 180
	return bulletangle
	
size = width, height = 640, 360
screen = pygame.display.set_mode(size,RESIZABLE)
screentoscale = screen.copy()
player = Player()
area = screen.get_rect()
playrect = Rect(60,10,340,340)
bulletliferect = Rect(30,0,400,360)
font = pygame.font.Font("MSGOTHIC.TTC", 20)
bullets = list()
htbxlist = list()
enemies = list()
