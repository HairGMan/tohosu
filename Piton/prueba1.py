import clases
from clases import *

#========= Que nivel?: ==============
nombreNivel = "../nivelprueba"

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

pygame.mixer.music.load(nombreNivel + "/musica.wav")
pygame.mixer.music.play()
background = pygame.image.load(nombreNivel + "/fondo.jpg").convert()
backgroundoffset = 350.0
gui = pygame.image.load("sprites/gui_place_nochoto_tr.png").convert_alpha()
scoremeter = font.render("Puntaje", True, (255,255,255))
recordmeter = font.render("Record", True, (255,255,255))
while 1:
	clock.tick_busy_loop(60)
	fps = font.render(str(int(clock.get_fps()) - 2) + "FPS", True, (255,255,255))
	bulletcountdisp = font.render("Balas:" + str(clases.debugbulletcount), True, (255,255,255))
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
		if framecount == eventlist[ev][0]:
			eventdict[eventlist[ev][1]](*eventlist[ev][2:])
			ev += 1

	#========= Actualizacion: =========
	
	player.update()
	for i in enemies:
		i.update()
		screentoscale.blit(i.image, i.imgpos)
	for i in bullets:
		i.update()
		screentoscale.blit(i.image, i.imgpos)
		
	screentoscale.blit(player.image, player.imgpos)
	screentoscale.blit(gui, area)
	screentoscale.blit(fps, (2,0))
	screentoscale.blit(bulletcountdisp, (screentoscale.get_width() - bulletcountdisp.get_width(),screentoscale.get_height() - bulletcountdisp.get_height()))
	screentoscale.blit(scoremeter,(480,35))
	screentoscale.blit(recordmeter,(485,90))
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
