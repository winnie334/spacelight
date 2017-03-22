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


