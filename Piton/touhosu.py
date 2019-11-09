import clases
from clases import *

def gameover(score = 0):
	global screen
	pygame.mixer.music.stop()
	cursor = pygame.image.load("sprites/bullet6_p_tr.png").convert_alpha()
	cursorpos = (120,220)
	gameovermask = pygame.Surface((341,340),HWSURFACE)
	gameovermask.fill((0,0,0))
	gameovermask.set_alpha(60)
	screentoscale.blit(gameovermask,(60,10))
	screentoscale.blit(font_bold.render("Fin del juego!", True, (255,255,255)),(120,50))
	screentoscale.blit(font_bold.render("Puntaje: " + str(player.score), True, (255,255,255)),(120,80))
	screenshot = screentoscale.copy()
	options = [Option("Reiniciar",[120,220],0), Option("Ir al menu",[120,250],1)]
	options[0].select()
	selct_option = 0
	while 1:
		clock.tick_busy_loop(60)
		for event in pygame.event.get():		
			if event.type == pygame.QUIT: 
				sys.exit()
			if event.type == pygame.VIDEORESIZE:
				screen = pygame.display.set_mode(event.dict['size'],RESIZABLE)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					options[0].select()
					options[1].deselect()
					cursorpos = (120,220)
				elif event.key == pygame.K_DOWN:
					options[1].select()
					options[0].deselect()
					cursorpos = (120,250)
				if event.key == pygame.K_z:
					for i in options:
						if i.selected:
							selct_option = i.id
							return selct_option
		screentoscale.blit(screenshot,(0,0))
		screentoscale.blit(cursor,cursorpos)
		for i in options:
			screentoscale.blit(i.render(),i.pos)
		screen.blit(pygame.transform.scale(screentoscale, screen.get_size()), (0, 0))
		pygame.display.flip()

#========= Que nivel?: ==============
nombreNivel = "../NivelPrueba"

#========= Funcion de salida:=========
def haltandcatchfire():
        pygame.mixer.music.stop()
#        pygame.mixer.music.unload()
        #aca iria alguna manera de llamar al proximo nivel
		
#========= Lector de eventos: ==========
eventdict = {
	"enemy" :	createenemy,
	"move" :	move,
	"delete":	delete,
    "end":		haltandcatchfire,
	"switch":	switchshot
	}
eventfile = open(nombreNivel + "/eventos.thi","r")
eventlines = eventfile.readlines()
eventfile.close()
eventlist = list()

for i in range(len(eventlines)):
	eventlist.append((eventlines[i].split()))
	for d in range(len(eventlist[i])):
		if d != 1:
			eventlist[i][d] = int(eventlist[i][d])

eventnum = len(eventlist)

#========= Frames, eventos: =========
clock = pygame.time.Clock()
clock

#========= Runtime: =========

def level(lives, screen, screentoscale):
	debugmode = False
	framecount = 0
	ev = 0
	pygame.mixer.music.load(nombreNivel + "/nice_lvl_3.wav")
	pygame.mixer.music.play(-1)
	background = pygame.image.load(nombreNivel + "/fondo.jpg").convert()
	backgroundoffset = 350.0
	record = 999999999
	uff = 0
	gui = pygame.image.load("sprites/gui_place_nochoto_tr.png").convert_alpha()
	lifesprite = pygame.image.load("sprites/place_life_red2_tr.png").convert_alpha()
	scoretext = font.render("Puntaje", True, (255,255,255))
	recordtext = font.render("Record", True, (255,255,255))
	recordamount = font.render(str(record).zfill(10) + "00", True, (255,255,255))
	player.init(lives)
	items.append(Item(3,10,(100,50)))
	while 1:
		clock.tick_busy_loop(60)
		fps = font.render(str(int(clock.get_fps()) - 2) + "FPS", True, (255,255,255))
		bulletcountdisp = font.render("Balas:" + str(clases.debugbulletcount), True, (255,255,255))
		uffmeter = font.render("Uff: " + str(uff), True, (255,255,255))
		scoremeter = font.render(str(player.score).zfill(10) + "00", True, (255,255,255))
		backgroundoffset += 0.05
		
		#========= Eventos de teclado: =========
		
		for event in pygame.event.get():		
			if event.type == pygame.QUIT: 
				sys.exit()
			if event.type == pygame.VIDEORESIZE:
				screen = pygame.display.set_mode(event.dict['size'],RESIZABLE)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LSHIFT:
						player.state[2] = 1
						player.update()
				if event.key == pygame.K_UP:
						player.moveup()
				elif event.key == pygame.K_DOWN:
						player.movedown()
				elif event.key == pygame.K_LEFT:
						player.moveleft()
				elif event.key == pygame.K_RIGHT:
						player.moveright()
				if event.key == pygame.K_F4:
					debugmode = not debugmode
				if event.key == pygame.K_m:
					if debugmode:
						player.image = pygame.image.load("sprites/placekamisama_tr.png").convert_alpha()
						
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LSHIFT:
					player.state[2] = 3
					player.update()
				if event.key == pygame.K_UP:
						player.movedown()
				elif event.key == pygame.K_DOWN:
						player.moveup()
				elif event.key == pygame.K_LEFT:
						player.moveright()
				elif event.key == pygame.K_RIGHT:
						player.moveleft()
						
		screentoscale.blit(background, (0, - background.get_height() + backgroundoffset))
		
		#========= Manejo de eventos: =========
		
		while (framecount == eventlist[ev][0]) & (ev+1 < eventnum):
				eventdict[eventlist[ev][1]](*eventlist[ev][2:])
				if debugmode:
					print(eventlist[ev][1])
				ev += 1

		#========= Actualizacion: =========
		
		player.update()
		for i in enemies:
			i.update()
			screentoscale.blit(i.image, i.imgpos)
		for i in items:
			i.update()
			screentoscale.blit(i.image, i.rect)
		for i in bullets:
			i.update()
			if player.invulntime == 0:
				if i.rect.colliderect(player.uffhtbx):
					if i.uffeable == True:
						i.uffeable = False
						uff += 1
			screentoscale.blit(i.image, i.imgpos)
			
		screentoscale.blit(player.image, player.imgpos)
		screentoscale.blit(gui, area)
		screentoscale.blit(fps, (2,0))
		if debugmode:
			screentoscale.blit(bulletcountdisp, (screentoscale.get_width() - bulletcountdisp.get_width(),screentoscale.get_height() - bulletcountdisp.get_height()))
		screentoscale.blit(scoretext,(450,35))
		screentoscale.blit(scoremeter,(480,60))
		screentoscale.blit(recordtext,(450,90))
		screentoscale.blit(recordamount,(480,115))
		screentoscale.blit(uffmeter,(450,180))
		
		#========= Manejo de vidas: =========
		
		for i in range(player.lives - 1):
			screentoscale.blit(lifesprite,(450 + i*20,155))
			
		if player.lives == 0:
			gameoveroption = gameover(score)
			for i in reversed(xrange(len(enemies))):
				enemies[i].delete()
			for i in reversed(xrange(len(bullets))):
				bullets[i].delete()
			clases.currentenemyid = 0
			return gameoveroption
			
		screen.blit(pygame.transform.scale(screentoscale, screen.get_size()), (0, 0))
		
		if player.invulntime == 0:
			if player.rect.collidelist(htbxlist) != -1:
				player.hit()
		elif player.invulntime > 0:
			if player.invulntime > 90:
				for i in bullets:
					i.delete()
			if player.invulntime % 5 == 0:
				if player.invulntime % 10 == 0:
					player.image = pygame.Surface((0,0))
				else:
					player.image = pygame.image.load("sprites/placehtbxsmall_tr.png")
		
		pygame.display.flip()
		framecount += 1

def scorescreen(screen, screentoscale):
	return

while 1:
	funk = level(2,screen,screentoscale)
	if funk == 1:
		sys.exit()