import clases
from clases import *

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
framecount = 0
ev = 0

#========= Runtime: =========
pygame.mixer.pre_init(48000,-16,1,1024)
pygame.mixer.music.load(nombreNivel + "/nice_lvl_3.wav")
pygame.mixer.music.play(-1)
background = pygame.image.load(nombreNivel + "/fondo.jpg").convert()
backgroundoffset = 350.0
score = 3000
record = 999999999
uff = 0
gui = pygame.image.load("sprites/gui_place_nochoto_tr.png").convert_alpha()
lifesprite = pygame.image.load("sprites/place_life_red2_tr.png").convert_alpha()
scoretext = font.render("Puntaje", True, (255,255,255))
scoremeter = font.render(str(score).zfill(10) + "00", True, (255,255,255))
recordtext = font.render("Record", True, (255,255,255))
recordamount = font.render(str(record).zfill(10) + "00", True, (255,255,255))
gameovermask = pygame.Surface((341,340),HWSURFACE)
gameovermask.fill((0,0,0))
gameovermask.set_alpha(60)

while 1:
	clock.tick_busy_loop(60)
	fps = font.render(str(int(clock.get_fps()) - 2) + "FPS", True, (255,255,255))
	bulletcountdisp = font.render("Balas:" + str(clases.debugbulletcount), True, (255,255,255))
	uffmeter = font.render("Uff: " + str(uff), True, (255,255,255))
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
	
        if ev < eventnum:
                while (framecount == eventlist[ev][0]) & (ev+1 < eventnum):
                        eventdict[eventlist[ev][1]](*eventlist[ev][2:])
                        print(eventlist[ev][1])
                        if ev+1 < eventnum:
                                ev += 1
        if framecount == 10000:
                player.image = pygame.image.load("sprites/placekamisama_tr.png").convert_alpha()

	#========= Actualizacion: =========
	
	player.update()
	for i in enemies:
		i.update()
		screentoscale.blit(i.image, i.imgpos)
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
	screentoscale.blit(bulletcountdisp, (screentoscale.get_width() - bulletcountdisp.get_width(),screentoscale.get_height() - bulletcountdisp.get_height()))
	screentoscale.blit(scoretext,(450,35))
	screentoscale.blit(scoremeter,(480,60))
	screentoscale.blit(recordtext,(450,90))
	screentoscale.blit(recordamount,(480,115))
	screentoscale.blit(uffmeter,(450,180))
	for i in range(player.lives - 1):
		screentoscale.blit(lifesprite,(450 + i*20,155))
	if player.lives == 0:
		screentoscale.blit(gameovermask,(60,10))
	screen.blit(pygame.transform.scale(screentoscale, screen.get_size()), (0, 0))
	
	#========= Invulnerabilidad (no se si dejarlo aca) =========
	
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
