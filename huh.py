import pygame


def rot_center(image, angle):
	# imported. No idea how this works.
	orig_rect = image.get_rect()
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = orig_rect.copy()
	rot_rect.center = rot_image.get_rect().center
	rot_image = rot_image.subsurface(rot_rect).copy()
	return rot_image


def playsound(mixer, sound):
	test = pygame.mixer.Sound(sound)
	test.play()


def animate(directory, frames):
	animation = []
	for i in range(frames):
		image = pygame.image.load(directory +  r'\frame' + str(i) + '.gif').convert_alpha()
		animation.append(image)
	return animation


def getpercentages(angle):
	# this returns two values that should give an idea what the rate of the x/y axis is.
	# e.g. if it moves 100 units, how many of those are up and how many are right.
	if 0 <= angle % 360 < 90 or 180 <= angle % 360 < 270:
		ypercent = angle % 90 / 90
		xpercent = 1 - ypercent
	else:
		xpercent = angle % 90 / 90
		ypercent = 1 - xpercent
	if 90 <= angle % 360 <= 270:
		xpercent *= -1
	if 0 <= angle % 360 <= 180:
		ypercent *= -1
	return xpercent, ypercent
