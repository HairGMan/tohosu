import pygame, sys, math, cmath, random
from math import *
from cmath import *
from pygame.locals import *
from random import *
pygame.mixer.init(frequency=44100,buffer=1024)
pygame.init()

currentenemyid = 0
seed()

class Particle(pygame.sprite.Sprite):
	def __init__(self,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.rect.move_ip(startpos)
		self.vectpos = [self.rect.x,self.rect.y]
		
	def update(self):
		self.vectpos[0] += self.movepos[0]
		self.vectpos[1] += self.movepos[1]
		self.rect.move_ip((self.vectpos[0] - self.rect.x,self.vectpos[1] - self.rect.y))
		self.duration -= 1
		if self.duration == 0:
			self.delete()
		
	def delete(self):
		particles.remove(self)
		del self
		
class CollectParticle(Particle):
	def __init__(self,drop,startpos):
		self.image = font_small.render(drop,True,(255,255,255))
		self.duration = 60
		self.movepos = [0.0,-2.0]
		Particle.__init__(self,startpos)
		
	def update(self):
		self.movepos[1] = self.movepos[1] * self.duration / 60
		Particle.update(self)

class Cursor(pygame.Rect):
	def __init__(self):
		pygame.Rect.__init__(self,0,0,1,1)
		
	def update(self):
		self.left,self.top=pygame.mouse.get_pos()
		
class SparkParticle(Particle):
	def __init__(self,startpos,color):
		self.color = color
		self.image = pygame.Surface((4,4))
		self.image.fill(self.color)
		self.duration = 20
		self.movepos = angletodir(uniform(2,3),uniform(0,360))
		Particle.__init__(self,startpos)
		
class Item(pygame.sprite.Sprite):
	def __init__(self,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.pos = startpos
		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]
		self.init(startpos)
		
	def init(self,startpos):
			self.rect.x = startpos[0]
			self.rect.y = startpos[1]
			self.movepos = (0,2)
			self.vectpos = [self.rect.x,self.rect.y]
			self.autocollected = False
		
	def collect(self):
		player.score += self.score
		particles.append(CollectParticle(self.dropstring,self.rect.center))
		self.delete()
		return
		
	def update(self):
		if self.autocollected == True:
			 self.movepos = trackplayer(self,player,4)
		self.vectpos[0] += self.movepos[0]
		self.vectpos[1] += self.movepos[1]
		self.rect.move_ip((self.vectpos[0] - self.rect.x,self.vectpos[1] - self.rect.y))
		pygame.event.pump()
		if not bulletliferect.contains(self.rect):
			self.delete()
		if self.rect.colliderect(player.uffhtbx):
			self.collect()
			
	def delete(self):
		items.remove(self)
		del self
		
class ItemPower(Item):
	def __init__(self,startpos):
		self.image = pygame.image.load("sprites/item_p_red_tr.png").convert_alpha()
		self.score = 2
		self.dropstring = "+1"
		Item.__init__(self,startpos)
		
	def collect(self):
		if player.power < 64:
			player.power += 1
		Item.collect(self)

class ItemPoint(Item):
	def __init__(self,startpos):
		self.image = pygame.image.load("sprites/item_p_blue_tr.png").convert_alpha()
		self.score = 100
		self.dropstring = str(self.score*10)
		Item.__init__(self,startpos)
		
	def update(self):
		self.score = 25000 * 10 / self.rect.y
		self.dropstring = str(self.score*10)
		Item.update(self)
		
class ItemCharge(Item):
	def __init__(self,startpos):
		self.image = pygame.image.load("sprites/item_c_green_tr.png").convert_alpha()
		self.score = 20
		self.dropstring = "Carga"
		Item.__init__(self,startpos)
		
	def collect(self):
		player.charge += 1
		Item.collect(self)
		
class ItemExtend(Item):
	def __init__(self,startpos):
		self.image = pygame.image.load("sprites/item_1up_tr.png").convert_alpha()
		self.score = 20
		self.dropstring = "1UP"
		Item.__init__(self,startpos)
		
	def collect(self):
		player.lives += 1
		Item.collect(self)

class Option():
	def __init__(self,string,pos,id):
		self.string = string
		self.pos = pos
		self.selected = False
		self.color = (255,255,255)
		self.id = id
		
	def select(self):
		if not self.selected:
			self.pos[0] += 20
			self.selected = not self.selected
			self.color = (128,255,128)
		
	def deselect(self):
		if self.selected:
			self.pos[0] -= 20
			self.selected = not self.selected
			self.color = (255,255,255)
	
	def render(self):
		return font.render(self.string, True, self.color)

class Enemy(pygame.sprite.Sprite):
	def __init__(self,startpos,pattern,bullettype,instances,angleinterval,rotation,patternspeed,bulletspeed,bulletspeedfrac,delay,health,drop,killpoint):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("sprites/placeenemysmall_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-4,-4)
		self.init(startpos)
		self.imagecenter = [self.image.get_width()/2, self.image.get_height()/2]
		self.imgpos = (self.rect.centerx - self.imagecenter[0], self.rect.centery - self.imagecenter[1])
		htbxlist.append(self.rect)
		enemyhtbxlist.append(self.rect)
		self.movepos = (0,0)
		self.moveclock = 0
		
		#=======Variables del patron=======
		
		self.shootclock = delay
		self.pattern = pattern
		self.bullettype = bullettype
		self.patternspeed = patternspeed
		self.bulletspeed = float(bulletspeed) / bulletspeedfrac
		self.patternrotation = rotation
		self.angleinterval = float(angleinterval)
		
		#=======Variables del enemigo======
		
		self.drop = drop
		self.health = health
		self.killpoint = killpoint
		global currentenemyid
		self.id = currentenemyid
		
		currentenemyid += 1
		self.angleclock = 0.0
		self.patterninstances = instances
		self.patterndict = {
			1:	self.Pattern1Bullet,
			2:	self.Pattern2Bullets,
			3:	self.PatternTrack1,
			4:	self.PatternTrack2,
			5:	self.PatternSpiral,
			6:	self.PatternRandom
		}
		self.bulletdict = {
			1:	BulletA,
			2:	BulletB,
			3:	BulletC,
			4:	BulletD,
			5:	BulletE
		}
		self.dropdict = {
			1:	ItemPoint,
			2:	ItemPower,
			3:	ItemCharge,
			4:	ItemExtend
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
		
	def Pattern1Bullet(self):
		for s in range(self.patterninstances - 1):
			bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed,self.patternrotation+self.angleinterval*(s+1))),(float(self.rect.centerx),float(self.rect.centery))))
			bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed,self.patternrotation-self.angleinterval*(s+1))),(float(self.rect.centerx),float(self.rect.centery))))
		bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed,self.patternrotation)),(float(self.rect.centerx),float(self.rect.centery))))

	def Pattern2Bullets(self):
		for s in range(self.patterninstances - 1):
			bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed,self.patternrotation+self.angleinterval*(s+1.5))),(float(self.rect.centerx),float(self.rect.centery))))
			bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed,self.patternrotation-self.angleinterval*(s+1.5))),(float(self.rect.centerx),float(self.rect.centery))))
		bullets.append(self.bulletdict[self.bullettype](angletodir(self.bulletspeed,self.patternrotation+self.angleinterval/2),self.rect.center))
		bullets.append(self.bulletdict[self.bullettype](angletodir(self.bulletspeed,self.patternrotation-self.angleinterval/2),self.rect.center))
			
	def PatternTrack1(self):
		for s in range(self.patterninstances - 1):
			bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed,self.patternrotation+self.angleinterval*(s+1))),(float(self.rect.centerx),float(self.rect.centery))))
			bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed,self.patternrotation-self.angleinterval*(s+1))),(float(self.rect.centerx),float(self.rect.centery))))
		bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed,self.patternrotation)),(float(self.rect.centerx),float(self.rect.centery))))
	
	def PatternTrack2(self):
		bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed,self.patternrotation+self.angleinterval/2)),(float(self.rect.centerx),float(self.rect.centery))))
		bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed,self.patternrotation-self.angleinterval/2)),(float(self.rect.centerx),float(self.rect.centery))))
		for s in range(self.patterninstances - 1):
			bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed,self.patternrotation+self.angleinterval*(s+1.5))),(float(self.rect.centerx),float(self.rect.centery))))
			bullets.append(self.bulletdict[self.bullettype]((trackplayer(self,player,self.bulletspeed,self.patternrotation-self.angleinterval*(s+1.5))),(float(self.rect.centerx),float(self.rect.centery))))
			
	def PatternSpiral(self):
		for s in range(self.patterninstances):
			bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed,self.patternrotation+self.angleclock+360/self.patterninstances*s)),(float(self.rect.centerx),float(self.rect.centery))))
		self.angleclock += self.angleinterval % 360
	
	def PatternRandom(self):
		for s in range(self.patterninstances):
			bullets.append(self.bulletdict[self.bullettype]((angletodir(self.bulletspeed * uniform(0.5,2),uniform(0,360))),(float(self.rect.centerx),float(self.rect.centery))))

	def die(self):
		items.append(self.dropdict[self.drop](self.rect.center))
		particles.append(CollectParticle(str(self.killpoint*10),self.rect.center))
		for i in range(15):
			particles.append(SparkParticle(self.rect.center,(225,225,255)))
		player.score += self.killpoint
		self.delete()

	def update(self):
		if self.shootclock == 0:
			self.shoot()
		elif self.shootclock > 0:
			self.shootclock -= 1
		if self.moveclock == 0:
			self.movepos = (0,0)
		else:
			self.moveclock -= 1
		if self.health <= 0:
			self.die()
		self.rect.move_ip(self.movepos)
		self.imgpos = (self.rect.centerx - self.imagecenter[0], self.rect.centery - self.imagecenter[1])
		pygame.event.pump()
		
	def delete(self):
		enemies.remove(self)
		htbxlist.remove(self.rect)
		enemyhtbxlist.remove(self.rect)
		del self
		
class Bullet(pygame.sprite.Sprite):
	def __init__(self,speed,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.init(speed,startpos)
		self.imagecenter = [self.image.get_width()/2, self.image.get_height()/2]
		self.imgpos = (self.rect.centerx - self.imagecenter[0], self.rect.centery - self.imagecenter[1])
		htbxlist.append(self.rect)
		self.uffeable = True
	
	def init(self,speed,startpos):
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.movepos = speed
		self.vectpos = [self.rect.x,self.rect.y]
		
	def update(self):
		self.vectpos[0] += self.movepos[0]
		self.vectpos[1] += self.movepos[1]
		self.rect.move_ip((self.vectpos[0] - self.rect.x,self.vectpos[1] - self.rect.y))
		self.imgpos = (self.rect.centerx - self.imagecenter[0], self.rect.centery - self.imagecenter[1])
		pygame.event.pump()
		if not bulletliferect.contains(self.rect):
			self.delete()
		
	def delete(self):
		htbxlist.remove(self.rect)
		bullets.remove(self)
		del self
		
class BulletA(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("sprites/bullet4_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-4,-4)
		Bullet.__init__(self,speed,startpos)

class BulletB(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("sprites/bulletbig3_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-12,-12)
		Bullet.__init__(self,speed,startpos)
		
class BulletC(Bullet):
	def __init__(self,speed,startpos):
		self.baseimage = pygame.image.load("sprites/bullet6_p_tr.png").convert_alpha()
		self.image = pygame.transform.rotate(self.baseimage,dirtoangle(*speed))
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-10,-10)
		Bullet.__init__(self,speed,startpos)

class BulletD(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("sprites/bullet5_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-4,-4)
		Bullet.__init__(self,speed,startpos)

class BulletE(Bullet):
	def __init__(self,speed,startpos):
		self.image = pygame.image.load("sprites/bulletsmol_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		Bullet.__init__(self,speed,startpos)
		
class BulletFriendly(Bullet):
	def __init__(self,speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("sprites/bulletfriendly_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		friendlyhtbxlist.append(self.rect)
		self.init(speed,(player.rect.centerx-self.rect.centerx,player.rect.top))
		self.imgpos = self.rect
		
	def update(self):
		self.vectpos[0] += self.movepos[0]
		self.vectpos[1] += self.movepos[1]
		self.rect.move_ip((self.vectpos[0] - self.rect.x,self.vectpos[1] - self.rect.y))
		self.imgpos = self.rect
		pygame.event.pump()
		if not bulletliferect.contains(self.rect):
			self.delete()
		elif self.rect.collidelist(enemyhtbxlist) != -1:
			enemies[self.rect.collidelist(enemyhtbxlist)].health -= 1
			player.score += 1
			self.delete()
			
	def delete(self):
		if self.rect in friendlyhtbxlist:
			friendlyhtbxlist.remove(self.rect)
		friendlybullets.remove(self)
		del self
		
class Charge(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.chargemask = pygame.Surface((340,340),SRCALPHA,32)
		self.chargemask.convert_alpha()
		self.active = False
		
	def locate(self):
		self.active = True
		self.duration = 15
		self.thunderpoints = [(player.rect.centerx-60,player.rect.centery-10)]
		self.rects = [player.rect.inflate(60,60)]
		if len(enemies) != 0:
			for h in enemyhtbxlist:
				if playrect.colliderect(h):
					self.thunderpoints.append((h.centerx-60,h.centery-10))
					self.rects.append((h.inflate(30,30)))
			funcionparamezclarlistasporqueelprofequierequeusemospython2quenotieneesafuncionperopython3si(self.thunderpoints)
			pygame.draw.lines(self.chargemask,(255,255,150),False,self.thunderpoints,6)
			for e in reversed(xrange(len(enemies))):
				if playrect.colliderect(enemies[e].rect):
					enemies[e].die()
					player.score += 100
			
	def update(self):
		pygame.event.pump()
		for b in bullets:
			if not b.rect.collidelist(self.rects) == -1:
				b.delete()
		self.duration -= 1
		if self.duration == 6:
			self.chargemask.fill((0,0,50,0),None,BLEND_RGBA_ADD)
			self.chargemask.fill((0,0,0,150),None,BLEND_RGBA_SUB)
		if self.duration == 0:
			self.active = False
			self.chargemask.fill((0,0,0,0))
	
class Player(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("sprites/placehtbxsmall_tr.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.inflate_ip(-8,-8)
		self.imagecenter = [self.image.get_width()/2, self.image.get_height()/2]
		self.imgpos = (self.rect.centerx - self.imagecenter[0], self.rect.centery - self.imagecenter[1])
		self.uffhtbx = self.rect.copy()
		self.uffhtbx.inflate_ip(10,10)
		self.init()
		
	def init(self,lives = 1):
		self.score = 0
		self.rect.x = 230
		self.rect.y = 300
		self.state = [0,0,3]
		if pygame.key.get_pressed()[pygame.K_LSHIFT]:
			self.state[2] = 1
		if pygame.key.get_pressed()[pygame.K_UP]:
			self.moveup()
		if pygame.key.get_pressed()[pygame.K_DOWN]:
			self.movedown()
		if pygame.key.get_pressed()[pygame.K_LEFT]:
			self.moveleft()
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			self.moveright()
		self.movepos = [0,0]
		self.invulntime = 0
		self.power = 64
		self.score = 0
		self.shootclock = 5
		self.debuginvincible = False
		self.lives = lives
		self.charge = 2
		self.chargeobj = Charge()

	def update(self):
		self.movepos = [(self.state[0] * self.state[2]),(self.state[1] * self.state[2])]
		newpos = self.rect.move(self.movepos)
		if playrect.contains(newpos):
			self.rect = newpos
			self.uffhtbx = newpos.inflate(10,10)
			self.imgpos = (self.rect.centerx - self.imagecenter[0], self.rect.centery - self.imagecenter[1])
			pygame.event.pump()
		if not self.invulntime == 0:
			self.invulntime -= 1
		if (self.power == 64) & (self.rect.centery < 50):
			self.autocollect()
			
	def hit(self):
			self.rect.x = 230
			self.rect.y = 300
			self.invulntime = 150
			self.lives -= 1
			self.charge = 2
			self.power = 0
			
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
	
	def shoot(self):
		self.shootclock -= 1
		if self.shootclock == 0:
			friendlybullets.append(BulletFriendly((0.5,-6)))
			friendlybullets.append(BulletFriendly((-0.5,-6)))
			friendlybullets.append(BulletFriendly((0,-6)))
			self.shootclock = 5
			
	def shootcharge(self):
		if self.charge > 0:
			if not self.chargeobj.active:
				self.chargeobj.locate()
				self.charge -= 1
				
	def autocollect(self):
		for i in items:
			i.autocollected = True
				
def createenemy(startposx,startposy,pattern,bullettype,instances = 1,angleinterval = 0,rotation = 0,patternspeed = 10,bulletspeed = 3,bulletspeedfrac = 1,delay = 0,health = 1,drop = 1,killpoint = 300):
	startpos = (startposx,startposy)
	enemies.append(Enemy(startpos,pattern,bullettype,instances,angleinterval,rotation,patternspeed,bulletspeed,bulletspeedfrac,delay,health,drop,killpoint))
	return

def move(id,x,y,steps,mode = 0):
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

def switchshot(id,pattern,bullettype = 1,instances = 1,interval = 0,rotation = 0,patternspeed = 10,bulletspeed = 3,bulletspeedfrac = 1):
	for e in enemies:
		if e.id == id:
			e.pattern = pattern
			if pattern != 0:
				e.bullettype = bullettype
				e.patterninstances = instances
				e.angleinterval = float(interval)
				e.patternrotation = rotation
				e.patternspeed = patternspeed
				e.bulletspeed = float(bulletspeed) / bulletspeedfrac
				e.shootclock = 0
			
def trackplayer(enemy,player,speed,offset = 0.0):
	distance = complex(float((enemy.rect.centerx - player.rect.x)),float((enemy.rect.centery - player.rect.y)))
	b_phase = phase(distance) + (offset/180*pi)
	bulletdirection = rect(-speed,b_phase)
	return bulletdirection.real, bulletdirection.imag
	
def angletodir(speed,angle):
	bulletdirection = rect(speed,(angle/180*pi))
	return bulletdirection.real, bulletdirection.imag
	
def dirtoangle(dirx,diry):
	if dirx == 0: return 90
	bulletangle = -atan2(diry,dirx) / pi * 180
	return bulletangle

def funcionparamezclarlistasporqueelprofequierequeusemospython2quenotieneesafuncionperopython3si(list,offset = 0):
	for i in range(offset,len(list)):
		j = randrange(offset,i+1)
		list[i], list[j] = list[j], list[i]

size = width, height = 640, 360
screen = pygame.display.set_mode(size,RESIZABLE|DOUBLEBUF|FULLSCREEN)
screentoscale = screen.copy()
screen = pygame.display.set_mode((1920,1080),RESIZABLE|DOUBLEBUF|FULLSCREEN)
area = screen.get_rect()
playrect = Rect(60,10,340,340)
bulletliferect = Rect(30,0,400,360)
font = pygame.font.Font("sprites/MSGOTHIC.TTC", 20)
font_small = pygame.font.Font("sprites/MSGOTHIC.TTC", 10)
font_bold = pygame.font.Font("sprites/MSGOTHIC.TTC", 20)
font_bold.set_bold(True)
font_meter = pygame.font.Font("sprites/MSGOTHIC.TTC", 18)
bullets = list()
enemies = list()
enemyhtbxlist = list()
bullethtbxlist = list()
items = list()
particles = list()
htbxlist = list()
friendlybullets = list()
friendlyhtbxlist = list()
player = Player()