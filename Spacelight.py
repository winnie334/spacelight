"""
FYI, I'm not super happy with the name either.

also, note to self: if you use init it's only for that instance, accessable with self from within
otherwise, you can use it from anywhere.

full list of TODOs:
make the deathstar killable?
add more EXPLOSIONS!! to hide the bugs
add some sort of storyline/progress
add sounds
improve the menu

full list of MAYBES:
powerups
fuel concept
shield for the player
nerf deathstar damage a bit/make it a more lategame enemy
warning sign for meteorites
bingo active sign
"""

import pygame
from random import randint
import os
from huh import rot_center, playsound, animate, getpercentages
from math import sin, cos, radians, degrees, atan

gamewidth = 1280
gameheight = 800
fps = 60

x = pygame.init()
gamesurface = pygame.display.set_mode([gamewidth, gameheight])
pygame.display.set_caption('Spacelight Alpha')
clock = pygame.time.Clock()
soundmixer = pygame.mixer.init()


class Menu:
	def __init__(self):
		playsound(0, "soundtrack.wav")
		self.inmenu = 1
		self.hoverover = [0]
		self.sb = pygame.image.load('button0d.png')
		self.sbsize = self.sb.get_rect().size
		self.buttonlist = [self.sb]
		self.buttonsizelist = [self.sbsize]
		self.draw()
		self.buttonposlist = [self.sbpos]
		while self.inmenu == 1:
			self.inmenu = self.getinput()
			self.draw()
			pygame.display.update()
			clock.tick(60)
		if self.inmenu == 2:
			pygame.quit()
			quit()

	def draw(self):
		for i, value in enumerate(self.hoverover):
			if value == 1:
				self.buttonlist[i] = pygame.image.load('button' + str(i) + 'a.png')
			if value == 0:
				self.buttonlist[i] = pygame.image.load('button' + str(i) + 'd.png')
		a = gamewidth / 10
		b = gameheight / 10
		c = gamewidth - a * 2
		d = gameheight - b * 2
		gamesurface.fill(Colors.space)
		pygame.draw.rect(gamesurface, Colors.black, [a, b, c, d], 10)
		pygame.draw.rect(gamesurface, Colors.white, [a + 6, b + 6, c - 12, d - 12], 10)
		pygame.draw.rect(gamesurface, Colors.black, [a + 12, b + 12, c - 24, d - 24], 5)
		pygame.draw.rect(gamesurface, Colors.menu_background, [a + 17, b + 17, c - 34, d - 34])
		for i, button in enumerate(self.buttonlist):
			self.sbpos = gamesurface.blit(button, [c - self.buttonsizelist[i][0], d - self.buttonsizelist[i][1]])

	def getinput(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 2
			x, y = pygame.mouse.get_pos()
			for index, button in enumerate(self.buttonposlist):
				if button.collidepoint(x, y):
					if event.type == pygame.MOUSEBUTTONDOWN:
						if index == 0:
							playsound(0, 'menu.ogg')
							return
					else:
						self.hoverover[index] = 1
				else:
					self.hoverover = [0 for _ in self.hoverover]
		return True


class Colors:
	# here we keep all the colors we're going to use in the game
	space = (20, 20, 40)
	red = (255, 0, 0)
	black = (0, 0, 0)
	white = (255, 255, 255)
	hb_background = (250, 200, 100)
	hb_green = (50, 200, 10)
	hb_red = (253, 44, 38)
	menu_background = (189, 188, 246)
	deathstar_laser = (70, 250, 2)


class Stars:
	# makes a list of all the background stars in the game
	# each star has its own list assigned, each with the follwing information:
	# [[xpos, ypos], (color), size, speed]

	speed = 1

	def __init__(self):
		self.starlist = []
		self.staramount = 150
		for star in range(self.staramount):
			newstar = self.generatenewstar(1)
			self.starlist.append(newstar)

	def generatenewstar(self, start):
		# generates random values for each parameter of the star. The value start determines
		# whether it spawns in the middle of the screen or out of bounds to the right
		if start:
			pos = [randint(0, gamewidth), randint(0, gameheight - 10)]
		else:
			pos = [gamewidth + 10, randint(0, gameheight - 10)]
		size = randint(2, 5)
		speed = randint(1, 5)
		if 0 != randint(0, self.staramount):
			color = (randint(245, 255), randint(245, 255), randint(245, 255))
		else:
			color = (randint(30, 255), randint(30, 255), randint(30, 255))
		return [pos, color, size, speed]

	def drawstars(self):
		for index, star in enumerate(self.starlist):
			newwidth = star[2] + (2 * Stars.speed - 2) * star[3] / 2
			pygame.draw.rect(gamesurface, star[1], [star[0][0], star[0][1], newwidth, star[2]])
			star[0][0] -= star[3] * Stars.speed
			star[1] = (star[1][0], 255 - Stars.speed * 28, 255 - Stars.speed * 28)
			if star[0][0] < -10:
				newstar = self.generatenewstar(0)
				self.starlist[index] = newstar


class HealthBars:
	# Draws the health for each ship.

	size = 3
	list = []

	def __init__(self, health, pos, number):
		# the var pos causes the health bar to appear either left or right on the screen
		# with a value of respectively -1 or 1.
		# number is the value of what healthbar it is, meaning if there are 3 enemy ships it can have a position
		# of up to 2. The Y pos is adjusted by this value so the healthbars don't overlap.

		self.left = pos
		self.size = HealthBars.size
		self.healthboxes = []
		for _ in range(health):
			self.healthboxes.append(1)
		self.bonushp = [1, 1, 1, 1, 1, 1, 1, 1, 1]
		self.currenthp = len(self.healthboxes)
		self.cube = self.size * 30
		self.hbheight = self.cube / 3 + 10
		self.ypos = gameheight / 20 + (gameheight / 9 * number)
		self.adjy = self.ypos + 2 / 3 * self.cube - 10
		if pos == -1:
			self.xpos = gamewidth / 20
			# the adj values indicate where the actual health bar should start (not the bingo card).
			self.adjx = self.xpos + self.size * 30
		if pos == 1:
			self.xpos = 19 * gamewidth / 20
			self.adjx = self.xpos - self.size * 30
		self.hboxsizex = self.size * 4
		self.hbwidth = (self.hboxsizex + 2) * len(self.healthboxes) + (self.hboxsizex / 3 * 2)
		self.hboxsizey = self.hbheight / 2
		self.hboxbonusx = (self.cube - 24) / 3
		self.hboxbonusy = (self.cube - 25) / 3

	def draw(self, color, xpos, ypos, width, height):
		pygame.draw.rect(gamesurface, color, [xpos, ypos, width, height])

	def update(self):
		a = -self.left
		self.draw(Colors.black, self.xpos, self.ypos, a * self.cube, self.cube)
		self.draw(Colors.black, self.adjx, self.adjy, a * self.hbwidth, self.hbheight)
		self.draw(Colors.hb_background, self.xpos + 5 * a, self.ypos + 5, a * (self.cube - 10), self.cube - 10)
		self.draw(Colors.hb_background, self.adjx - 5 * a, self.adjy + 5, a * self.hbwidth, self.hbheight - 10)
		for index, healthbox in enumerate(self.healthboxes):
			hboxposx = self.adjx + (self.hboxsizex + 2) * index * a - (self.hboxsizex + 2) * (a == -1)
			if healthbox == 1:
				self.draw(Colors.hb_green, hboxposx, self.adjy + 10, self.hboxsizex, self.hboxsizey)
			if healthbox == 0:
				self.draw(Colors.hb_red, hboxposx, self.adjy + 10, self.hboxsizex, self.hboxsizey)
		for index, healthbox in enumerate(self.bonushp):
			hboxposx = self.xpos + 10 * a + (self.hboxbonusx + 2) * (index % 3) * a
			hboxposy = self.ypos + 10 + (self.hboxbonusy + 3) * int(index / 3)
			if healthbox == 1:
				self.draw(Colors.hb_green, hboxposx, hboxposy, self.hboxbonusx * a + 2 * (a == -1), self.hboxbonusy)
			if healthbox == 0:
				self.draw(Colors.hb_red, hboxposx, hboxposy, self.hboxbonusx * a + 2 * (a == -1), self.hboxbonusy)
		# pygame.draw.rect(gamesurface, Colors.red, [self.adjx, self.ypos + self.size * 30, 5, 5])

	def damage(self, health, amount):
		self.currenthp = health
		for _ in range(amount):
			if self.currenthp > 0:
				self.healthboxes[self.currenthp - 1] = 0
				self.currenthp -= 1
			elif not self.checkforbingo():
				# get a list of all the positions of green bonus hp's, then takes a random position of those
				# and makes it 0 in the list self.bonushp
				greenones = [i for i, x in enumerate(self.bonushp) if x == 1]
				self.bonushp[greenones[randint(0, len(greenones) - 1)]] = 0
				if self.checkforbingo():
					self.currenthp = -10

	def checkforbingo(self):
		for i in range(3):
			if self.bonushp[0 + 3 * i] == self.bonushp[1 + 3 * i] == self.bonushp[2 + 3 * i] == 0:
				return 1
			if self.bonushp[i] == self.bonushp[i + 3] == self.bonushp[i + 6] == 0:
				return 1
		if self.bonushp[0] == self.bonushp[4] == self.bonushp[8] == 0:
			return 1
		if self.bonushp[2] == self.bonushp[4] == self.bonushp[6] == 0:
			return 1
		return 0


class EnemyShip(pygame.sprite.Sprite):
	# an enemy, hooray!
	# health is quite selfexplanatory.
	# boost is the average amount the ship will jump with.
	# speed is the rate at it will jump. The higher it is, the longer it will take for the enemy to jump.
	# speed must be higher than 10.

	shipspritelist = pygame.sprite.Group()
	list = []
	difficulty = 0

	def __init__(self, health, boost, mspeed, aspeed, healthbar):
		pygame.sprite.Sprite.__init__(self)
		EnemyShip.shipspritelist.add(self)
		self.health = health
		self.healthbar = healthbar
		self.isdead = 0
		self.xpos = gamewidth + randint(0, 200)
		self.targetx = 3 * gamewidth / 4
		self.angle = 0
		self.rotatingtarget = 0
		self.currentframe = 1
		self.currentframecounter = 0
		self.maxboost = boost
		self.boostamount = 0
		self.timestill = 0
		self.speed = mspeed
		self.attackspeed = aspeed
		self.timenotshot = 0

		# this here will get our fancy ship animated
		self.enemyshipanimation = []
		for file in os.listdir('enemyship'):
			frame = pygame.image.load(r'enemyship\\' + file).convert_alpha()
			self.enemyshipanimation.append(frame)
		self.image = self.enemyshipanimation[0]
		self.mask = pygame.mask.from_surface(self.image)
		self.ypos = randint(0, gameheight - self.enemyshipanimation[0].get_rect().height)

	def update(self, mainship):
		self.xpos += (self.targetx - self.xpos) * 0.03
		self.rotate(mainship)
		if self.boostamount != 0:
			self.ypos += self.boostamount
			self.boostamount = (self.boostamount / 1.05) * (self.boostamount > 0.2 or self.boostamount < -0.2)
			# dividing it by 1.05 will make it have a smooth acceleration. Note that you'll need to find the limit
			# in the move() function if you change this value. The limit of 1.05 is 21.
		else:
			if randint(self.timestill, self.speed) == self.speed and self.timestill > 10:
				self.move()
				self.timestill = 0
			else:
				self.timestill += 1
		if randint(1, self.attackspeed) == 1 and self.timenotshot > 10:
			self.shoot()
			self.timenotshot = 0
		else:
			self.timenotshot += 1
		self.currentframecounter += 1
		if self.currentframecounter % (round(self.speed / 20, 0)) == 0:
			# every few frames, change the sprite. The speed is based on the speed of the ship itself.
			self.currentframe = (self.currentframe + 1) % 13
			self.image = self.enemyshipanimation[self.currentframe]
			self.image = rot_center(self.image, -self.angle)
		gamesurface.blit(self.image, [self.xpos, self.ypos])
		self.mask = pygame.mask.from_surface(self.image)

	def boost(self, up):
		# changes the boost amount so it'll get moving. Var up makes it go up/down with a value of either 1/0
		if up == 1:
			self.boostamount = -randint(self.maxboost - 5, self.maxboost)
		else:
			self.boostamount = randint(self.maxboost - 5, self.maxboost)

	def move(self):
		# will try to detect if it's too high/low and boost accordingly. If it can choose, it'll do something random.
		if self.ypos + 21 * self.maxboost + 140 > gameheight:
			self.boost(1)
		elif self.ypos - 21 * self.maxboost < 0:
			self.boost(0)
		else:
			self.boost(randint(0, 1))

	def rotate(self, mainship):
		ydif = self.ypos - mainship.ypos
		xdif = self.xpos - mainship.xpos
		preciseangle = degrees(atan(ydif / xdif))
		self.rotatingtarget = (self.rotatingtarget + preciseangle) / 2
		self.angle += (self.rotatingtarget - self.angle) * 0.05

	def shoot(self):
		laser = Shoot(self.xpos, self.ypos, -1, -self.angle)
		laser2 = Shoot(self.xpos, self.ypos, -1, -self.angle)
		Shoot.laserlist.append(laser)
		Shoot.laserlist.append(laser2)

	def takedamage(self, dmg):
		self.healthbar.damage(self.health, dmg)
		self.health -= dmg
		if self.healthbar.currenthp == -10:
			print('enemy down')
			self.isdead = 1


class MainShip:
	# this is the class for the main ship the player will be playing with

	def __init__(self, health, speed, fuel, healthbar):
		self.health = health
		self.isdead = 0
		self.healthbar = healthbar
		self.fuel = fuel
		self.bullets = 0
		self.isshooting = 0
		self.cooldown = 0
		self.xpos = gamewidth / 8
		self.ypos = gameheight / 2
		self.speed = speed
		self.currentspeed = 0
		self.ismoving = 0
		self.isrotating = 0
		self.rotatingtarget = 0
		self.angle = 0
		self.posnextframe = self.ypos
		# self.original = pygame.image.load('spaceshipmain2.png')
		# self.image = self.original
		self.justcrashed = 0
		self.framecounter = 0
		self.shipanimation = animate('mainship')
		self.original = self.shipanimation[0]
		self.image = self.original
		self.mask = pygame.mask.from_surface(self.image)

	def takedamage(self, dmg):
		self.healthbar.damage(self.health, dmg)
		self.health -= dmg
		if self.healthbar.currenthp == -10:
			print('ooh no im dead')
			self.isdead = 1

	def shoot(self):
		laser = Shoot(self.xpos, self.ypos, 1, self.angle)
		Shoot.laserlist.append(laser)

	def move(self, up):
		if up != 0:
			self.ismoving = up
			self.currentspeed += self.speed * -self.ismoving
		if up == 0:
			self.ismoving = 0

	def rotate(self, clockwise):
		if clockwise != 0:
			self.isrotating = clockwise
		if clockwise == 0:
			self.isrotating = 0

	def update(self):
		# this one is going to need some explaining.
		# note that after every update, your speed is going to approach 0. You will always slow down.
		# first off, your speed will be changed based on the ismoving variable.

		if self.isrotating != 0:
			self.rotatingtarget -= self.speed * self.isrotating * 5
		self.fuel -= (self.ismoving != 0) * 0.05
		self.angle += (self.rotatingtarget - self.angle) * 0.1
		self.currentspeed += self.speed * -self.ismoving
		self.posnextframe = self.ypos + self.currentspeed
		if self.currentspeed != 0:
			# if you're in the game frame and haven't recently crashed, update your ship position.
			if -20 < self.posnextframe < gameheight - 140 and self.justcrashed == 0:
				self.ypos += self.currentspeed
			if self.justcrashed == 0:
				# if you haven't just crashed, update this variable. If you're out of bounds (or will be),
				# this will flip to 1.
				self.justcrashed = -20 > self.posnextframe or self.posnextframe > gameheight - 140
			if self.justcrashed == 1:
				# if you actually DID just crash, bounce the ship back in the opposite direction, with the same speed.
				self.currentspeed *= -1
			if self.justcrashed != 0:
				# this will make your justcrashed variable revert to 0 every two updates.
				self.justcrashed -= 0.5
			self.currentspeed = self.currentspeed / 1.05 * (self.currentspeed > 0.2 or self.currentspeed < -0.2)
			# same as with enemyship. Lower the speed decreasingly, until it's so low it's not worth calculating anymore
		self.cooldown += 1 * (self.cooldown < 10)
		if self.isshooting == 0 or (self.bullets == 0 and self.isshooting != 0):
			self.framecounter += 1
			if self.framecounter % 40 == 1 and self.bullets <= 9:
				self.bullets += 1
		else:
			if self.cooldown == 10 and self.bullets > 0:
				self.cooldown = 0
				self.shoot()
				self.bullets -= 1
		self.original = self.shipanimation[self.bullets]
		self.image = rot_center(self.original, self.angle)
		gamesurface.blit(self.image, [self.xpos, self.ypos])
		self.mask = pygame.mask.from_surface(self.image)


class Shoot(pygame.sprite.Sprite):
	# shoots, but no idea how
	laserlist = []
	laserspritelist = []
	currentlaser = False
	currentenemylaser = False
	shiporientation = [(50, -35), (50, 30), (-75, -15), (-75, 10)]
	# this list we'll keep in case we ever need it. It shows the x and y values you need to add to 80
	# to become the point of origin of the laser the ship shoots. I honestly hope you'll never need this again.

	def __init__(self, xpos, ypos, isityou, angle):
		# isityou makes the laser go left/right, with a value of -1/1
		pygame.sprite.Sprite.__init__(self)
		Shoot.laserspritelist.append(self)
		self.angle = angle
		self.rad = radians(self.angle)
		self.xangle, self.yangle = getpercentages(self.angle)
		self.xspeed = 22 * isityou * self.xangle
		self.yspeed = 22 * isityou * self.yangle
		if isityou == 1:
			self.image = pygame.image.load('laser2.png')
			# these formulas calculate where the position of the laser is after rotating the image
			# so the lasers actually start at the 'guns'
			self.firstlaser = (-32.5 * sin(self.rad) + 87 * cos(self.rad), -32.5 * cos(self.rad) - 87 * sin(self.rad))
			self.secondlaser = (32.5 * sin(self.rad) + 87 * cos(self.rad), 32.5 * cos(self.rad) - 87 * sin(self.rad))
			self.laserpositions = [self.firstlaser, self.secondlaser]
			self.xpos = xpos + self.laserpositions[Shoot.currentlaser][0] + 80
			self.ypos = ypos + self.laserpositions[Shoot.currentlaser][1] + 80
			Shoot.currentlaser = not Shoot.currentlaser  # switches between guns
		if isityou == -1:
			self.image = pygame.image.load('enemylaser.png')
			self.firstlaser = (-15 * sin(self.rad) - 75 * cos(self.rad), -15 * cos(self.rad) + 75 * sin(self.rad))
			self.secondlaser = (10 * sin(self.rad) - 75 * cos(self.rad), 10 * cos(self.rad) + 75 * sin(self.rad))
			self.laserpositions = [self.firstlaser, self.secondlaser]
			self.xpos = xpos + self.laserpositions[Shoot.currentenemylaser][0] + 80
			self.ypos = ypos + self.laserpositions[Shoot.currentenemylaser][1] + 80
			Shoot.currentenemylaser = not Shoot.currentenemylaser  # also switches, but should get called again instantly
		self.isityou = isityou
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.blitx, self.blity = self.xpos, self.ypos

	def update(self, mainship):
		self.xpos += self.xspeed
		self.ypos += self.yspeed
		if self.xpos + 50 < 0 or self.xpos > gamewidth or self.ypos < 0 or self.ypos > gameheight + 50:
			self.kill()
			Shoot.laserlist.remove(self)
		else:
			Shoot.checkforcollision(self, mainship)
			# absolutely no idea how this works. It tries to blit in a location so that the actual x and y pos seem
			# more clear, but it's more guesswork. Use the following command here to see where the actual positions are
			# pygame.draw.rect(gamesurface, Colors.red, [self.xpos - 2.5, self.ypos - 2.5, 5, 5])
			if self.isityou == 1:
				self.blitx = self.xpos - 25 * self.xangle
				self.blity = self.ypos - 25 * self.yangle - 2.5 if self.yangle >= 0 else self.ypos - 2.5
			elif self.isityou == -1:
				self.blitx = self.xpos
				self.blity = self.ypos - 5 * self.yangle - 2.5 if self.yangle >= 0 else self.ypos + 25 * self.yangle - 2.5
			gamesurface.blit(self.image, [self.blitx, self.blity])

	def checkforcollision(self, mainship):
		if self.isityou == 1:
			for enemyship in EnemyShip.list:
				try:
					if enemyship.mask.get_at((int(self.xpos - enemyship.xpos), int(self.ypos - enemyship.ypos))):
						enemyship.takedamage(1)
						self.hit()
						return
				except IndexError:
					pass
			for deathstar in Deathstar.list:
				if (self.xpos - deathstar.centerx)**2 + (self.ypos - deathstar.centery)**2 <= deathstar.radius**2:
					deathstar.takedamage(1)
					self.hit()
		if self.isityou == -1:
			try:
				if mainship.mask.get_at((int(self.xpos - mainship.xpos), int(self.ypos - mainship.ypos))):
					mainship.takedamage(1)
					self.hit()
					return
			except IndexError:
				pass
		for laser in Shoot.laserlist:
			if laser != self:
				if laser.xpos - 5 < self.xpos < laser.xpos + 5 and laser.ypos - 5 < self.ypos < laser.ypos + 5:
					self.kill()
					laser.kill()
					try:
						Shoot.laserlist.remove(self)
						Shoot.laserlist.remove(laser)
					except ValueError:
						pass

		for meteorite in Meteorite.list:
			try:
				if meteorite.mask.get_at((int(self.xpos - meteorite.xpos), int(self.ypos - meteorite.ypos))):
					self.hit()
					meteorite.kill()
					Meteorite.list.remove(meteorite)
					return
			except IndexError:
				pass

	def hit(self):
		self.kill()
		Shoot.laserlist.remove(self)
		Explosion([self.xpos, self.ypos], 0)


class Meteorite(pygame.sprite.Sprite):
	# meteorites, because more chaos is better.

	list = []

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		Meteorite.list.append(self)
		rarity = randint(1, 100)
		dir = 'meteorites\\'
		if 1 <= rarity < 70:
			dir += '0'
		if 70 <= rarity < 95:
			dir += '1'
		if 95 <= rarity:
			dir += '2'
		dirsize = len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])
		self.original = pygame.image.load(dir + '\\' + str(randint(0, dirsize - 1)) + '.png')
		self.size = randint(60, 80)
		self.rotspeed = randint(5, 30) / 10
		self.original = pygame.transform.scale(self.original, [self.size, self.size])
		self.original = pygame.transform.rotate(self.original, randint(0, 360))
		self.image = self.original
		self.angle = 0
		self.mask = pygame.mask.from_surface(self.original)
		if randint(0, 1):
			self.xpos = randint(0, gamewidth)
			self.ypos = -250 if randint(0, 1) else gameheight + 250
		else:
			self.xpos = gamewidth + 250
			self.ypos = randint(0, gameheight)
		self.offsetx = 0
		self.offsety = 0
		# we're going to take a target position to make sure it shows up on the screen
		self.targetx = randint(gamewidth / 5, 4 * gamewidth / 5)
		self.targety = randint(gameheight / 5, 4 * gameheight / 5)
		self.speedx = (self.targetx - self.xpos) / 100
		self.speedy = (self.targety - self.ypos) / 100
		# this loop will make sure the speeds are reasonably high.
		while abs(self.speedx) + abs(self.speedy) < 10:
			self.speedx *= 1.01
			self.speedy *= 1.01
		dmgsp = max([abs(self.speedx), abs(self.speedy)])
		self.damage = 1 * (0 < dmgsp <= 6) + 2 * (6 < dmgsp <= 8) + 3 * (8 < dmgsp)

	def update(self, mainship):
		self.xpos += self.speedx
		self.ypos += self.speedy
		self.angle += self.rotspeed
		self.image = rot_center(self.original, self.angle)
		if self.xpos + 250 < 0 or self.xpos - 250 > gamewidth or self.ypos + 250 < 0 or self.ypos - 250 > gameheight:
			self.kill()
			Meteorite.list.remove(self)
		else:
			self.checkforcollision(mainship)
			gamesurface.blit(self.image, [self.xpos, self.ypos])
		# this last line may not be needed
		self.mask = pygame.mask.from_surface(self.image)

	def checkforcollision(self, mainship):
		self.offsetx = int(mainship.xpos - self.xpos)
		self.offsety = int(mainship.ypos - self.ypos)
		if self.mask.overlap(mainship.mask, (self.offsetx, self.offsety)) is not None:
			self.kill()
			Meteorite.list.remove(self)
			mainship.takedamage(self.damage)
			Explosion([self.xpos, self.ypos], 0)
			return
		for enemyship in EnemyShip.list:
			self.offsetx = int(enemyship.xpos - self.xpos)
			self.offsety = int(enemyship.ypos - self.ypos)
			if self.mask.overlap(enemyship.mask, (self.offsetx, self.offsety)) is not None:
				self.kill()
				try:
					Meteorite.list.remove(self)
				except ValueError:
					pass
				enemyship.takedamage(self.damage)
				Explosion([self.xpos, self.ypos], 0)
				return
		for meteorite in Meteorite.list:
			if meteorite != self:
				self.offsetx = int(meteorite.xpos - self.xpos)
				self.offsety = int(meteorite.ypos - self.ypos)
				if self.mask.overlap(meteorite.mask, (self.offsetx, self.offsety)) is not None:
					self.kill()
					try:
						Meteorite.list.remove(self)
						Meteorite.list.remove(meteorite)
						Explosion([self.xpos, self.ypos], 0)
					except ValueError:
						pass
					return


class Deathstar(pygame.sprite.Sprite):
	# A sprite so good it needed functionality.

	list = []

	def __init__(self, pos, attackspeed):
		pygame.sprite.Sprite.__init__(self)
		self.xpos, self.ypos = pos[0], pos[1]
		self.health = 5
		self.targetx, self.targety = gamewidth / 8, gameheight / 2
		self.aimpointx, self.aimpointy = gamewidth / 8, gameheight / 2
		self.laserx, self.lasery = self.xpos - 33, self.xpos - 15
		self.attackspeed = attackspeed
		self.beamlength = 3 / self.attackspeed	 # the smaller beamlength, the longer the beam will be fired.
		self.laserspeed = 10			 # this is the time it takes to get to the target
		self.animation = animate('deathstar')
		self.image = self.animation[0]
		self.centerx = self.xpos + self.image.get_rect().width / 2
		self.centery = self.ypos + self.image.get_rect().height / 2
		self.radius = self.image.get_rect().width / 2
		self.aimpoint = pygame.image.load('aimpoint.png')
		self.charge = 0
		self.isshooting = 0
		self.angle = 0
		self.xangle, self.yangle = getpercentages(self.angle)
		self.rotatingtarget = 0
		self.aimingup = randint(0, 1)
		self.beamparticles = []
		self.beamsize = 6
		self.beamdetail = 20
		self.newtarget()

	def update(self, objectslist):
		self.checkhealth()
		self.rotate()
		self.moveaimpoint()
		if self.isshooting <= 0:
			# if self.charge == 0:
			# 	self.newtarget()
			self.charge += 1
			self.isshooting = self.charge == self.attackspeed
		if self.isshooting > 0:
			self.shoot()
			self.isshooting -= self.beamlength
			self.charge = 0
		self.image = self.animation[int(self.charge / self.attackspeed * 10)]
		self.image = rot_center(self.image, self.angle)
		gamesurface.blit(self.image, [self.xpos, self.ypos])
		self.updatebeam(objectslist)

	def newtarget(self):
		# gets a random new target location. Note that the +80 for the x value is hardcoded, this is the half of the
		# width of the mainship to make the aimpoint and ship match.
		self.targetx = gamewidth / 8 + 80
		self.targety = randint(gameheight / 8, 7 * gameheight / 8)

	def updateaimpoint(self):
		self.aimpointx = self.targetx - self.aimpoint.get_rect().width / 2
		self.aimpointy = self.targety - self.aimpoint.get_rect().height / 2
		gamesurface.blit(self.aimpoint, [self.aimpointx, self.aimpointy])

	def moveaimpoint(self):
		if self.aimingup:
			self.targety -= 1
			if self.targety - self.aimpoint.get_rect().height / 2 <= 0:
				self.aimingup = 0
		else:
			self.targety += 1
			if self.targety + self.aimpoint.get_rect().height / 2 >= gameheight:
				self.aimingup = 1

	def rotate(self):
		ydif = self.ypos - self.targety
		xdif = self.xpos - self.targetx
		preciseangle = degrees(atan(ydif / xdif))
		self.rotatingtarget = - (self.rotatingtarget + preciseangle) / 2
		self.angle += (self.rotatingtarget - self.angle) / self.attackspeed
		rad = radians(self.angle)
		self.laserx = -15 * sin(rad) + (-33) * cos(rad) + 74 + self.xpos
		self.lasery = -15 * cos(rad) - (-33) * sin(rad) + 74 + self.ypos
		self.xangle, self.yangle = getpercentages(self.angle)

	def shoot(self):
		xspeed = (self.targetx - self.laserx) / self.laserspeed
		yspeed = (self.targety - self.lasery) / self.laserspeed
		self.beamparticles.append([self.laserx, self.lasery, xspeed, yspeed])

	def updatebeam(self, objectslist):
		for particle in self.beamparticles:
			delayx = particle[2] / self.beamdetail
			delayy = particle[3] / self.beamdetail
			for i in range(self.beamdetail):
				x, y = particle[0], particle[1]
				addx, addy = i * delayx, i * delayy
				offset = - self.beamsize / 2
				size = self.beamsize
				pygame.draw.rect(gamesurface, Colors.deathstar_laser, [x + addx + offset, y + addy + offset, size, size])
			particle[0] += particle[2]
			particle[1] += particle[3]
			if (particle[0] < -50 or particle[0] > gamewidth + 50) and \
				(particle[1] < -50 or particle[1] > gameheight + 50):
				self.beamparticles.remove(particle)
			self.checkforcollision(particle, objectslist)

	def checkforcollision(self, particle, objectslist):
		mainship = objectslist[0][0]
		for objects in objectslist:
			for object in objects:
				try:
					if object.mask.get_at((int(particle[0] - object.xpos), int(particle[1] - object.ypos))):
						self.beamparticles.remove(particle)
						Explosion([particle[0], particle[1]], 0)
						if object == mainship:
							mainship.takedamage(1)
				except IndexError:
					pass
				# commented code for if you want collision with lasers
				# except AttributeError:
				# 	if particle[0] - 10 < object.xpos < particle[0] + 10 and \
				# 		particle[1] - 10 < object.ypos < particle[1] + 10:
				# 		self.beamparticles.remove(particle)

	def takedamage(self, amount):
		self.health -= 1

	def checkhealth(self):
		if self.health <= 0:
			self.health -= 1
			if randint(0, self.health % 7) == 0:
				x, y = 0, 0
				while (x - self.centerx)**2 + (y - self.centery)**2 >= self.radius**2:
					x = randint(self.xpos, self.xpos + 2 * self.radius)
					y = randint(self.ypos, self.ypos + 2 * self.radius)
				Explosion([x, y], 0)
			if self.health <= -100:
				self.kill()
				Deathstar.list.remove(self)


class Explosion(pygame.sprite.Sprite):
	# yay, explosions! The more the better, as chaos hides the countless bugs.

	list = []

	def __init__(self, centerpos, size):
		pygame.sprite.Sprite.__init__(self)
		Explosion.list.append(self)
		self.centerx, self.centery = centerpos[0], centerpos[1]
		self.animation = animate('explosions\\' + str(size))
		self.currentframe = 0
		self.delay = 0
		self.image = self.animation[0]
		r = randint(-4, 4)
		self.size = [self.image.get_rect().width + r, self.image.get_rect().height + r]
		for i in range(len(self.animation)):
			self.animation[i] = pygame.transform.scale(self.animation[i], self.size)
		self.image = self.animation[0]
		self.xpos = self.centerx - self.image.get_rect().width / 2
		self.ypos = self.centery - self.image.get_rect().height / 2

	def update(self):
		gamesurface.blit(self.animation[self.currentframe], [self.xpos, self.ypos])
		self.currentframe += (self.delay % 5 == 0)
		self.delay += 1
		if self.currentframe >= len(self.animation):
			Explosion.list.remove(self)
			self.remove()


class Event:
	def __init__(self, chaoslevel):
		self.timenoevent = 0
		self.chaos = chaoslevel

	def check(self):
		if randint(self.timenoevent, self.chaos) == self.chaos:
			self.new()
			self.timenoevent = 0
		else:
			self.timenoevent += 1

	def new(self):
		Meteorite()


def getinput(mainship):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				mainship.move(0)
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				mainship.rotate(0)
			if event.key == pygame.K_SPACE:
				mainship.isshooting = 0
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				mainship.move(1)
			if event.key == pygame.K_DOWN:
				mainship.move(-1)
			if event.key == pygame.K_SPACE:
				mainship.isshooting = 1
			if event.key == pygame.K_RETURN:
				Meteorite()
			if event.key == pygame.K_LEFT:
				mainship.rotate(-1)
			if event.key == pygame.K_RIGHT:
				mainship.rotate(1)
	return False


def drawstuff(mainship, stars, event, warp):
	# draws everything that needs to be drawn in the right order
	# actually does a lot, lot more
	# as in, run the entire game
	event.check()
	gamesurface.fill(Colors.space)
	stars.drawstars()
	for deathstar in Deathstar.list:
		deathstar.update([[mainship], Meteorite.list])
	if mainship.isdead == 0:
		mainship.update()
	for enemyship in EnemyShip.list:
		if enemyship.isdead == 1:
			EnemyShip.list.remove(enemyship)
		else:
			enemyship.update(mainship)
	for laser in Shoot.laserlist:
		laser.update(mainship)
	for meteorite in Meteorite.list:
		meteorite.update(mainship)
	for deathstar in Deathstar.list:
		deathstar.updateaimpoint()
	for explosion in Explosion.list:
		explosion.update()
	for healthbar in HealthBars.list:
		healthbar.update()
	if not EnemyShip.list:
		HealthBars.list = [HealthBars.list[0]]
		warp.update()
	pygame.display.update()


def countdown(mainship, stars, event, warp):
	# we will draw the first frame, then save that as an image to constantly draw our numbers onto.
	drawstuff(mainship, stars, event, warp)
	pygame.image.save(gamesurface, 'startview.jpg')
	startview = pygame.image.load('startview.jpg')
	displayspeed = 800
	for number in range(3):
		original_image = pygame.image.load('countdown' + str(number) + '.gif')
		shrinkspeed = original_image.get_rect().width / displayspeed
		size = original_image.get_rect().width
		for frame in range(displayspeed):
			newsize = int(size - shrinkspeed * frame)
			if newsize < 0:
				continue
			image = pygame.transform.scale(original_image, [newsize, newsize])
			size = image.get_rect().width
			xpos = gamewidth / 2 - size / 2
			ypos = gameheight / 2 - size / 2
			gamesurface.blit(startview, [0, 0])
			gamesurface.blit(image, [xpos, ypos])
			pygame.display.update()
			clock.tick(60)
	os.remove('startview.jpg')


class Warp:
	# totally not stolen from Warblade

	def __init__(self):
		self.modifier = 0.3
		self.warptime = 0 	# will go to 100, to see what % of the warp we are in.
		self.timescalled = 0

	def update(self):
		if self.timescalled % 4 == 0:
			Stars.speed += self.modifier
			self.modifier -= 0.006	 # should be half the starting modifier when in 50%
			self.warptime += 1
			if self.warptime == 100:
				number = 0
				EnemyShip.difficulty += 1
				newenemy(number)
				for i in range(EnemyShip.difficulty):
					if 1 == randint(1, 5):
						number += 1
						newenemy(number)
				self.warptime = 0
				self.modifier = 0.3
				Stars.speed = 1
		self.timescalled += 1


def newenemy(number):
	health = 3 + (EnemyShip.difficulty - number * randint(1, 2)) * 2
	boost = 10 + EnemyShip.difficulty - number * randint(1, 2)
	mspeed = 151 - (EnemyShip.difficulty - number * randint(1, 2)) * 10 * (EnemyShip.difficulty < 15)
	aspeed = 150 - (EnemyShip.difficulty - number * randint(1, 2)) * 15 * (EnemyShip.difficulty < 10)
	healthbarenemy = HealthBars(health, 1, number)
	HealthBars.list.append(healthbarenemy)
	enemyship = EnemyShip(health, boost, mspeed, aspeed, healthbarenemy)
	EnemyShip.list.append(enemyship)
	if EnemyShip.difficulty >= 3 and len(EnemyShip.list) <= 2 and randint(0, 1):
		dsaspeed = 500 - EnemyShip.difficulty * 50 * (EnemyShip.difficulty < 10)
		if randint(0, 1):
			dspos = randint(0, gameheight / 10)
		else:
			dspos = randint(7 * gameheight / 10, 8 * gameheight / 10)
		deathstar = Deathstar([800, dspos], dsaspeed)
		Deathstar.list.append(deathstar)


def gameloop():
	game_exit = 0
	loop = 1
	healthbarmain = HealthBars(20, -1, 0)
	HealthBars.list = [healthbarmain]
	for i in range(1):
		newenemy(i)
	mainship = MainShip(healthbarmain.currenthp, 0.3, 200, healthbarmain)
	# ds = Deathstar([800, 600], 300)
	stars = Stars()
	event = Event(2000)
	warp = Warp()
	countdown(mainship, stars, event, warp)

	while not game_exit:
		game_exit = getinput(mainship)
		drawstuff(mainship, stars, event, warp)
		clock.tick(fps)
		loop += 1
	pygame.quit()
	quit()

Menu()
gameloop()
