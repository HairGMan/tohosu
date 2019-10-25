import clases
from clases import *

debugbulletcount = 0

eventdict = {
	"enemy" :	createenemy,
	"move" :	move,
	"delete":	delete
	}
eventfile = open("eventos.txt","r")
eventlines = eventfile.readlines()
eventlist = list()

for i in eventlines:
	eventlist.append((i.split()))
	for d in eventlist[eventlines.index(i)]:
		if eventlist[eventlines.index(i)].index(d) != 1:
			d = int(d)

def seekplayer(enemy):
	angle = 0
	return


clock = pygame.time.Clock()
clock
framecount = 0
ev = 0
while 1:
	clock.tick_busy_loop(60)
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

	if framecount == eventlist[ev][0]:
		eventdict[eventlist[ev][1]](*eventlist[ev][2])
		ev += 1

	player.update()
	for i in enemies:
		i.update()
		screen.blit(i.image, i.rect)
	for i in bullets:
		i.update()
		screen.blit(i.image, i.rect)
		
	screen.blit(player.image, player.rect)
		
	fps = font.render(str(int(clock.get_fps()) - 2) + "FPS", True, (255,255,255))
	bulletcountdisp = font.render("Balas:" + str(debugbulletcount), True, (255,255,255))
	screen.blit(fps, area)
	screen.blit(bulletcountdisp, (screen.get_width() - bulletcountdisp.get_width(),screen.get_height() - bulletcountdisp.get_height()))
	if player.invulntime == 0:
		if player.rect.collidelist(htbxlist) != -1:
			player.hit()
	elif player.invulntime > 90:
		for i in bullets:
			i.delete()
	pygame.display.flip()
		
	framecount += 1
	runtime()