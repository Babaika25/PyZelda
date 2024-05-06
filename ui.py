import pygame
from settings import *

class UI:
	def __init__(self):
		self.display_surface = pygame.display.get_surface() #прорисовка самого экрана
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE) #добавление стандартного шрифта
		self.healt_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT) #панелька для здоровья
		self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT) #панелька для энергии
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

	def show_bar(self, current, max_amountm, bg_rect, color):
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect) #отрисовка задника панельки
		ratio = current / max_amountm
		current_with = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_with
		pygame.draw.rect(self.display_surface, color, current_rect) #рисование панельки
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3) #рисование обводки панельки

	def show_exp(self, exp):
		text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR) #рендер шрифта с экспой, без сглаживания и с цветом
		x = self.display_surface.get_size()[0] - 20 #отступ снизу на 20 пикселей по x
		y = self.display_surface.get_size()[1] - 20 #отступ снизу на 20 пикселей по y
		text_rect = text_surf.get_rect(bottomright = (x, y)) #цепляемся за низ экрана справа

		pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20)) #цепляемся за низ экрана справа
		self.display_surface.blit(text_surf, text_rect) #отображаем панельку
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3) #обводка панели

	def weapon_overlay(self, weapon_index):
		bg_rect = pygame.Rect(10, 630, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf, weapon_rect)

	def display(self, player):
		self.show_bar(player.health, player.stats['health'], self.healt_bar_rect, HEALTH_COLOR) #обращение к отрисовке панели здоровья
		self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR) #обращение к отрисовке панели энергии
		self.show_exp(player.exp)
		self.weapon_overlay(player.weapon_index)