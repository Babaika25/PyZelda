import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups) #наследуем все группы
		self.sprite_type = sprite_type
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos) #указываем позицию отрисовки (левый верхний угол)
		self.hitbox = self.rect.inflate(0, -10) #делаем по 5 пискселей сверху и снизу от самого объекта, до хитбокса