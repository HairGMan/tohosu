#encoding: utf-8
import clases
from clases import *

def reescalatodopibe(scalefactor):
	for i in images.keys():
		images[i] = pygame.transform.scale(images[i],resolutions[scalefactor])

def pause():
	global screen
	pygame.mixer.music.pause()
	cursor = clases.images["image_bulletc"]
	cursorpos = [120,200]
	pausemask = pygame.Surface((340,340),HWSURFACE)
	pausemask.fill((0,0,0))
	pausemask.set_alpha(60)
	screentoscale.blit(pausemask,(60,10))
	screentoscale.blit(font_bold.render("Juego en pausa", True, (255,255,255)),(120,50))
	screenshot = screentoscale.copy()
	options = [Option("Reanudar",[120,200],-1), Option("Reiniciar",[120,230],1), Option(u"Ir al menú",[120,260],0)]
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
					if selct_option > 0:
						selct_option -= 1
						cursorpos[1] -= 30
				elif event.key == pygame.K_DOWN:
					if selct_option < 2:
						selct_option += 1
						cursorpos[1] += 30
				elif event.key == pygame.K_ESCAPE:
						return -1
				elif event.key == pygame.K_z or event.key == pygame.K_RETURN:
						return options[selct_option].id
		for i in options:
			i.deselect()
		options[selct_option].select()
		screentoscale.blit(screenshot,(0,0))
		screentoscale.blit(cursor,cursorpos)
		for i in options:
			screentoscale.blit(i.render(),i.pos)
		screen.blit(pygame.transform.scale(screentoscale, screen.get_size()), (0, 0))
		pygame.display.flip()

def highscorescreen(aftergame):
	global screen
	pygame.mouse.set_visible(False)
	background = pygame.image.load("sprites/background_highscores.png").convert_alpha() 
	title = font_bold.render(u"Puntajes más altos",False,(255,255,100))
	currenthighscore = -1
	if aftergame:
		for s in highscores:
			if player.score*10 > s.score:
				currenthighscore = highscores.index(s)
				highscores.insert(highscores.index(s),Highscore(player.score*10,""))
				highscores.pop()
				break
	while 1:
		clock.tick_busy_loop(60)
		for event in pygame.event.get():		
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
					return 0
				else:
					if not currenthighscore == -1:
						if event.key == pygame.K_BACKSPACE:
							if len(highscores[currenthighscore].name) > 0:
								highscores[currenthighscore].name = highscores[currenthighscore].name[:-1]
						else:
							if len(highscores[currenthighscore].name) < 13:
								highscores[currenthighscore].name += event.unicode
						highscores[currenthighscore].updatename()
						
		screentoscale.blit(background,area)
		screentoscale.blit(title,(320-title.get_width()/2,20))
		for s in highscores:
			screentoscale.blit(s.scoretext,(430,30+30*(1+highscores.index(s))))
			screentoscale.blit(s.nametext,(140,30+30*(1+highscores.index(s))))
		pygame.transform.scale(screentoscale, screen.get_size(), screen)
		pygame.display.update()

def mainmenu():
	pygame.mouse.set_visible(True)
	if clases.musica:
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.load("sprites/pantalla_de_titulo_que_no_existe3.wav")
			pygame.mixer.music.play(-1)
	title = font_bold.render("Proyecto TOHOSU",False,(255,255,255))
	subtitle = font.render("Cool danmaku shooter definitivamente terminado",False,(255,255,255))
	rojo1 = pygame.image.load("sprites/jugar1_tr.png").convert_alpha()
	rojo2 = pygame.image.load("sprites/jugar2_tr.png").convert_alpha()
	opciones = pygame.image.load("sprites/opciones_tr.png").convert_alpha()
	opciones2 = pygame.image.load("sprites/opciones2_tr.png").convert_alpha()
	records = pygame.image.load("sprites/records_tr.png").convert_alpha()
	records2 = pygame.image.load("sprites/records2_tr.png").convert_alpha()
	salir = pygame.image.load("sprites/salir_tr.png")
	salir2 = pygame.image.load("sprites/salir2_tr.png")
	imagenfondo = pygame.image.load("sprites/background_main.png")
	botones = [
		Button(rojo1,rojo2,285,210),
		Button(opciones,opciones2,285,240),
		Button(records,records2,285,270),
		Button(salir,salir2,285,300)
	]
	cursor = Cursor()

	while 1:
		clock.tick_busy_loop(60) 
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if cursor.colliderect(botones[0].rect):
					return 1
				elif cursor.colliderect(botones[1].rect):
					return 2
				elif cursor.colliderect(botones[2].rect):
					return 3
				elif cursor.colliderect(botones[3].rect):
					return -1
			if event.type == pygame.QUIT:
				sys.exit()
		 
		screentoscale.blit(imagenfondo,(0,0))
		screentoscale.blit(title,(screentoscale.get_width()/2-title.get_width()/2,30))
		screentoscale.blit(subtitle,(screentoscale.get_width()/2-subtitle.get_width()/2,50))
		cursor.update()
		for b in botones:
			b.update(screentoscale,cursor)
		pygame.transform.scale(screentoscale, screen.get_size(), screen)
		pygame.display.update()

def optionsmenu():
	global screen
	background = pygame.image.load("sprites/background_options.png")
	cursor = clases.images["image_bulletc"]
	cursorpos = [180,50]
	options = [
		Option(u"Resolución",(200,50),0,False),
		Option(u"Música",(200,80),1,False),
		Option(u"Pantalla",(200,110),2,False),
		Option(u"Vidas",(200,140),3,False)
	]
	optionstates = [
		[Option("1080",(400,50),3,False),Option("720",(450,50),2,False),Option("360",(500,50),1,False)],
		[Option(u"Sí",(400,80),0,False),Option("No",(440,80),1,False)],
		[Option("Completa",(400,110),0,False),Option("Ventana",(500,110),1,False)],
		[Option("3",(400,140),0,False)]
	]
	options[0].select()
	optionstates[3][0].string = str(clases.vidasiniciales)
	selct_option = 0
	selct_option_sub = [3-clases.scalefactor,int(not clases.musica),int(not clases.fullscreen),0]
	while 1:
		clock.tick_busy_loop(60)
		for event in pygame.event.get():		
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					if selct_option > 0:
						selct_option -= 1
						cursorpos[1] -= 30
				elif event.key == pygame.K_DOWN:
					if selct_option < 3:
						selct_option += 1
						cursorpos[1] += 30
				elif event.key == pygame.K_ESCAPE:
						return 0
				elif event.key == pygame.K_LEFT:
						if selct_option_sub[selct_option] > 0:
							selct_option_sub[selct_option] -= 1
						if selct_option == 1: 
							clases.musica = True
							pygame.mixer.music.play(-1)
						elif selct_option == 3:
							if clases.vidasiniciales > 3:
								clases.vidasiniciales -= 1
							optionstates[selct_option][0].string = str(clases.vidasiniciales)
				elif event.key == pygame.K_RIGHT:
						if selct_option_sub[selct_option] < len(optionstates[selct_option])-1:
							selct_option_sub[selct_option] += 1
						if selct_option == 1: 
							clases.musica = False
							pygame.mixer.music.stop()
						elif selct_option == 3:
							if clases.vidasiniciales < 5:
								clases.vidasiniciales += 1
							optionstates[selct_option][0].string = str(clases.vidasiniciales)
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:						
						if selct_option == 0:
							clases.scalefactor = optionstates[selct_option][selct_option_sub[selct_option]].id
							if selct_option_sub[2] == 0:
								screen = pygame.display.set_mode(resolutions[clases.scalefactor],RESIZABLE|FULLSCREEN)
							else:
								screen = pygame.display.set_mode(resolutions[clases.scalefactor],RESIZABLE)
						elif selct_option == 2:
							if selct_option_sub[selct_option] == 0:
								screen = pygame.display.set_mode(resolutions[clases.scalefactor],RESIZABLE|FULLSCREEN)
								clases.fullscreen = True
							else:
								screen = pygame.display.set_mode(resolutions[clases.scalefactor],RESIZABLE)
								clases.fullscreen = False
		for i in options:
			i.deselect()
		options[selct_option].select()
		for i in optionstates:
			for j in i:
				j.deselect()
		optionstates[selct_option][selct_option_sub[selct_option]].select()
		screentoscale.blit(background,(0,0))
		screentoscale.blit(cursor,cursorpos)
		for i in options:
			screentoscale.blit(i.render(),i.pos)
		for i in optionstates:
			for j in i:
				screentoscale.blit(j.render(),j.pos)
		screen.blit(pygame.transform.scale(screentoscale, screen.get_size()), (0, 0))
		pygame.display.update()

	
def gameover():
	global screen, musica
	if musica:
		pygame.mixer.music.stop()
	cursor = clases.images["image_bulletc"]
	cursorpos = (120,220)
	gameovermask = pygame.Surface((340,340),HWSURFACE)
	gameovermask.fill((0,0,0))
	gameovermask.set_alpha(60)
	screentoscale.blit(gameovermask,(60,10))
	screentoscale.blit(font_bold.render(u"¡Fin del juego!", True, (255,255,255)),(120,50))
	screentoscale.blit(font_bold.render("Puntaje: " + str(player.score * 10), True, (255,255,255)),(120,80))
	screenshot = screentoscale.copy()
	options = [Option("Reiniciar",[120,220],1), Option(u"Ir al menú",[120,250],0)]
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
				if event.key == pygame.K_z or event.key == pygame.K_RETURN:
					for i in options:
						if i.selected:
							selct_option = i.id
							return selct_option
		screentoscale.blit(screenshot,(0,0))
		screentoscale.blit(cursor,cursorpos)
		for i in options:
			screentoscale.blit(i.render(),i.pos)
		screen.blit(pygame.transform.scale(screentoscale, screen.get_size()), (0, 0))
		pygame.display.update()
	
def victoryscreen(nextlevel):
	global screen, musica
	if musica:
		pygame.mixer.music.stop()
	gameovermask = pygame.Surface((340,340),HWSURFACE)
	gameovermask.fill((0,0,0))
	gameovermask.set_alpha(60)
	screentoscale.blit(gameovermask,(60,10))
	screentoscale.blit(font_bold.render(u"¡Ganaste!", True, (255,255,255)),(120,50))
	if nextlevel == 4:
		screentoscale.blit(font_bold.render("Puntaje final: " + str(player.score * 10), True, (255,255,255)),(120,80))
	else:
		screentoscale.blit(font_bold.render("Siguiente nivel: " + str(nextlevel), True, (255,255,255)),(120,80))
	screenshot = screentoscale.copy()
	while 1:
		clock.tick_busy_loop(60)
		for event in pygame.event.get():		
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z or event.key == pygame.K_RETURN:
							return
		screentoscale.blit(screenshot,(0,0))
		screen.blit(pygame.transform.scale(screentoscale, screen.get_size()), (0, 0))
		pygame.display.update()

#========= Funcion de salida:=========
def haltandcatchfire():
        pygame.mixer.music.stop()
#        pygame.mixer.music.unload()
        #aca iria alguna manera de llamar al proximo nivel
		
#========= Funcion que manda todo al carajo: =========
		
def mandatodoalcarajo():
	for i in reversed(enemies):
		i.delete()
	for i in reversed(bullets):
		i.delete()
	for i in reversed(items):
		i.delete()
	for i in reversed(friendlybullets):
		i.delete()
	for i in reversed(lasers):
		i.delete()
	player.chargeobj.active = False
	clases.currentenemyid = 0
	player.image = pygame.image.load("sprites/placehtbxsmall_tr.png")
	if clases.musica:
		pygame.mixer.music.stop()

#========= Lector de eventos: ==========

eventdict = {
	"enemy" :	createenemy,
	"move" :	move,
	"delete":	delete,
	"end":		haltandcatchfire,
	"switch":	switchshot,
	"laser":	shootlaser
	}
	
def eventread(nombreNivel):
	eventfile = open("../" + nombreNivel + "/eventos.thi","r")
	eventlines = eventfile.readlines()
	eventfile.close()
	eventlist = list()

	for i in range(len(eventlines)):
		eventlist.append((eventlines[i].split()))
		for d in range(len(eventlist[i])):
			if d != 1:
				eventlist[i][d] = int(eventlist[i][d])

	eventnum = len(eventlist)
	return eventlist, eventnum

#========= Frames, eventos: =========
clock = pygame.time.Clock()
clock
debugmode = False
debugenemycount = 0
debugshowhitboxes = False

#========= Runtime: =========

def level(level, lives, screen, screentoscale):
	pygame.mouse.set_visible(False)
	global debugmode, debugenemycount, debugshowhitboxes, musica
	levelfolderdict = {
		0: 	"NivelPrueba",
		1: 	"Nivel1",
		2: 	"Nivel2",
		3: 	"Nivel3"
	}
	levelevents = eventlist, eventnum = eventread(levelfolderdict[level])
	framecount = 0
	ev = 0
	eventend = False
	if musica:
		pygame.mixer.music.load("../" + levelfolderdict[level] + "/nice_lvl_3.wav")
		pygame.mixer.music.play(-1)
	background = pygame.image.load("../" + levelfolderdict[level] + "/fondo.png").convert()
	backgroundheight = background.get_height() + 10
	backgroundoffset = 350.0
	record = 999999999
	uff = 0
	gui = pygame.image.load("sprites/gui_place_final_tr.png").convert_alpha()
	lifesprite = pygame.image.load("sprites/place_life_red2_tr.png").convert_alpha()
	chargesprite = pygame.image.load("sprites/place_life_orange2_tr.png").convert_alpha()
	scoretext = font.render("Puntaje", False, (255,255,255))
	recordtext = font.render(u"Récord", False, (255,255,255))
	recordamount = font.render(str(record).zfill(11) + "0", False, (255,255,255))
	fullpowersign = font_bold.render(u"¡Máximo poder!", False, (255,255,255))
	powermeter = pygame.Surface((128,20))
	powermeter.fill((255,255,255))
	powermeter.set_alpha(150)
	powersprite = pygame.image.load("sprites/item_p_red_tr.png").convert_alpha()
	player.init(lives,player.power,player.charge)
	while 1:
		clock.tick_busy_loop(60)
		fps = font.render(str(int(clock.get_fps()) - 2) + "FPS", False, (255,255,255))
		bulletcountdisp = font.render("Balas:" + str(len(bullets)+len(friendlybullets)), False, (255,255,255))
		enemycountdisp = font.render("Enemigos:" + str(len(enemies)), False, (255,255,255))
		uffmeter = font.render("Uff: " + str(uff), False, (255,255,255))
		scoremeter = font.render(str(player.score).zfill(11) + "0", False, (255,255,255))
		if player.power == 64:
			powermetertext = font_meter.render(str(player.power), False, (255,0,255))
		else:
			powermetertext = font_meter.render(str(player.power), False, (255,255,255))
		if backgroundoffset < backgroundheight:
			backgroundoffset += 0.1
		
		#========= Eventos de teclado: =========
		
		for event in pygame.event.get():		
			if event.type == pygame.QUIT: 
				sys.exit()
			if event.type == pygame.VIDEORESIZE:
				screen = pygame.display.set_mode(event.dict['size'],RESIZABLE|DOUBLEBUF|FULLSCREEN)
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
				elif event.key == pygame.K_z:
						player.shootclock = 1
				elif event.key == pygame.K_x:
						player.shootcharge()
				elif event.key == pygame.K_ESCAPE:
					pauseoption = pause()
					if pauseoption == -1:
						pygame.mixer.music.unpause()
						player.state = [0,0,3]
						if pygame.key.get_pressed()[pygame.K_LSHIFT]:
							player.state[2] = 1
						if pygame.key.get_pressed()[pygame.K_UP]:
							player.moveup()
						if pygame.key.get_pressed()[pygame.K_DOWN]:
							player.movedown()
						if pygame.key.get_pressed()[pygame.K_LEFT]:
							player.moveleft()
						if pygame.key.get_pressed()[pygame.K_RIGHT]:
							player.moveright()
					else:
						mandatodoalcarajo()
						return pauseoption
				elif event.key == pygame.K_F4:
					debugmode = not debugmode
				elif event.key == pygame.K_m:
					if debugmode:
						player.image = pygame.image.load("sprites/placekamisama_tr.png").convert_alpha()
				elif event.key == pygame.K_i:
					if debugmode:
						player.debuginvincible = not player.debuginvincible
						player.invulntime = 15
				elif event.key == pygame.K_f:
					if debugmode:
						backgroundoffset += 100
				elif event.key == pygame.K_h:
					if debugmode:
						debugshowhitboxes = not debugshowhitboxes
				elif event.key == pygame.K_v:
					if debugmode:
						player.lives = 7
				elif event.key == pygame.K_c:
					if debugmode:
						player.charge = 7
				elif event.key == pygame.K_p:
					if debugmode:
						if event.mod == pygame.KMOD_LSHIFT:
							if player.power < 64:
								player.power += 1
						else:
							player.power = 64
						player.changepattern()
				elif event.key == pygame.K_s:
					if debugmode:
						eventend = True
						
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
		
		if pygame.key.get_pressed()[pygame.K_z]:
			player.shoot()
				
		screentoscale.blit(background, (60, - background.get_height() + backgroundoffset))
		
		#========= Manejo de eventos: =========
	
		while (framecount == eventlist[ev][0]) & (ev < eventnum) & (eventend == False):
			eventdict[eventlist[ev][1]](*eventlist[ev][2:])
			if debugmode:
				print str(ev+1) + " de " + str(eventnum) + ":"
				print(eventlist[ev][1:])
			if ev+1 < eventnum:
				ev += 1
			else:
				eventend = True
								
		#========= Actualizacion: =========
		
		player.update()
		if debugshowhitboxes:
			for i in htbxlist:
				debughtbxmarker = pygame.Surface((i.width,i.height))
				debughtbxmarker.fill((255,255,255))
				screentoscale.blit(debughtbxmarker,i)
		for i in lasers:
			i.update()
			if i.active:
				screentoscale.blit(i.image, i.rect)
		for i in enemies:
			i.update()
			screentoscale.blit(i.image, i.imgpos)
		for i in items:
			i.update()
			screentoscale.blit(i.image, i.rect)
		for i in particles:
			i.update()
			screentoscale.blit(i.image, i.rect)
		if player.chargeobj.active:
			player.chargeobj.update()
			screentoscale.blit(player.chargeobj.chargemask,(60,10))
		for i in friendlybullets:
			i.update()
			screentoscale.blit(i.image, i.rect)
		for i in bullets:
			i.update()
			if player.invulntime == 0:
				if i.rect.colliderect(player.uffhtbx):
					if i.uffeable == True:
						i.uffeable = False
						uff += 1
						for x in range(3):
							particles.append(SparkParticle(i.rect.center,(255,255,255)))
			screentoscale.blit(i.image, i.imgpos)
			
		screentoscale.blit(player.image, player.imgpos)
		screentoscale.blit(gui, area)
		screentoscale.blit(fps, (2,0))
		if debugmode:
			screentoscale.blit(bulletcountdisp, (screentoscale.get_width() - bulletcountdisp.get_width(),screentoscale.get_height() - bulletcountdisp.get_height()))
			screentoscale.blit(enemycountdisp, (screentoscale.get_width() - enemycountdisp.get_width(),screentoscale.get_height() - enemycountdisp.get_height() - 20))
		screentoscale.blit(scoretext,(450,35))
		screentoscale.blit(scoremeter,(480,60))
		screentoscale.blit(recordtext,(450,90))
		screentoscale.blit(recordamount,(480,115))
		screentoscale.blit(powermeter,(470,210),(0,0,player.power*2,18))
		screentoscale.blit(powermetertext,(475,210))
		screentoscale.blit(powersprite,(450,211))
		screentoscale.blit(uffmeter,(450,240))
		if player.fullpowersign > 0:
			screentoscale.blit(fullpowersign,(playrect.centerx-fullpowersign.get_width()/2,playrect.centery-fullpowersign.get_height()/2))
		#========= Manejo de vidas: =========
		
		for i in range(player.lives - 1):
			screentoscale.blit(lifesprite,(450 + i*20,155))
		for i in range(player.charge):
			screentoscale.blit(chargesprite,(450 + i*20,180))
			
		if player.lives == 0:
			gameoveroption = gameover()
			mandatodoalcarajo()
			if gameoveroption == 0:
				highscorescreen(True)
			return gameoveroption
			
		pygame.transform.scale(screentoscale, screen.get_size(), screen)
		
		if player.invulntime == 0:
			if player.rect.collidelist(htbxlist) != -1:
				player.hit()
			player.checklasercollision()
		else:
			if player.invulntime > 90:
				for i in reversed(bullets):
					i.delete()
			if player.invulntime % 5 == 0:
				if player.invulntime % 10 == 0:
					player.image = pygame.Surface((0,0))
				else:
					player.image = pygame.image.load("sprites/placehtbxsmall_tr.png")
					if player.debuginvincible:
						player.invulntime = 15
		
		pygame.display.update()
		framecount += 1
		
		if eventend == True:
			if len(enemies) == 0:
				victoryscreen(level+1)
				mandatodoalcarajo()
				return 4


currentlevel = 1
currentscreen = 0
while 1:
	if currentscreen == 0:
		player.charge = 2
		player.power = 0
		currentlevel = 1
		currentscreen = mainmenu()
	elif currentscreen == 1:
		currentscreen = level(currentlevel,clases.vidasiniciales,screen,screentoscale)
		if currentscreen == 4:
			currentlevel += 1
			if currentlevel == 4:
				currentscreen = highscorescreen(True)
			else:
				currentscreen = 1
		elif currentscreen == 1:
			player.charge = 2
			player.power = 0
			currentlevel = 1
	elif currentscreen == 2:
		currentscreen = optionsmenu()
	elif currentscreen == 3:
		currentscreen = highscorescreen(False)
	elif currentscreen == -1:
		sys.exit()
