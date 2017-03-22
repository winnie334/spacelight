import pygame, random

x = pygame.init()

gamewidth = 1000
gameheight = 800


gameboard = pygame.display.set_mode((gamewidth, gameheight))
pygame.display.set_caption('Screw copying everything!!')
clock = pygame.time.Clock()


def newcolor():
	return [random.randint(0,255), random.randint(0,255), random.randint(0,255)]


def display_message(msg, color, fontsize=20, xpos=gamewidth/2, ypos=gamewidth/2):
	font = pygame.font.SysFont(None, fontsize)
	text = font.render(msg, True, color)
	gameboard.blit(text, [xpos, ypos])


def gameloop():
	gameExit = False
	color = [255, 0, 255]
	xpos = gamewidth/2
	ypos = gameheight/2
	xchange = 0
	ychange = 0
	loop = 1
	size = 5
	speed = 50
	while gameExit is False:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					ychange = 5
				if event.key == pygame.K_DOWN:
					ychange = -5
				if event.key == pygame.K_RIGHT:
					xchange = 5
				if event.key == pygame.K_LEFT:
					xchange = -5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					ychange = 0
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					xchange = 0

		ypos -= ychange
		xpos += xchange
		#gameboard.fill((255,255,255))
		if not loop % 60:
			display_message('FASTER!!', newcolor(), size, ypos=40)
			color = newcolor()
			size += 2
			speed += loop/100
		pygame.draw.rect(gameboard, color, [xpos, ypos, size, size])
		pygame.display.update()
		clock.tick(speed)
		loop += 1
	pygame.quit()
	quit()

gameloop()