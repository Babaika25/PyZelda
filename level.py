import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from weapon import Weapon
from ui import UI
from enemy import Enemy

class Level: #создали класс
	def __init__(self): #базовые параметры
		self.display_surface = pygame.display.get_surface() #создали новый слой объектов
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group() #создали группу технических элементов
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group() #атакующий спрайт
		self.attackable_sprites = pygame.sprite.Group() #атакуемый спрайт
		self.ui = UI()
		self.create_map()

	def create_map(self):
		layouts = {
				'boundary': import_csv_layout('map/map_Block.csv'),
				'objects': import_csv_layout('map/map_Objects.csv'),
				'entities': import_csv_layout('map/map_Spawn.csv')
		}
		graphics = {
				'objects': import_folder('graphic/Objects')
		}
		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'objects':
							surf = graphics['objects'][int(col)]
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
						if style == 'entities':
							if col == '16':
								self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_weapon)
							else:
								if col == '0':
									monster_name = 'axolot'
								elif col == '4':
									monster_name = 'lizard'
								elif col == '8':
									monster_name = 'snake'
								else:
									monster_name = 'spirit'

								Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.add_xp)

	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])	

	def destroy_weapon(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprites in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprites, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'enemy':
							target_sprite.get_damage(self.player, attack_sprites.sprite_type)

	def damage_player(self, amount, attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()

	def add_xp(self, amount):
		self.player.exp += amount


	def final(self):
		if self.player.health <= 0:
			print('\n', '\n', 'Линк умер. Хана Хайрулу')
			exit()
		if self.player.exp > 5000:
			print('\n', '\n', 'Линк победил')
			exit()

	def run(self): #создали метод в классе
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.visible_sprites.enemy_update(self.player)
		self.player_attack_logic()
		self.final()
		self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2 #середина отрисованного экрана по ширине
		self.half_heigth = self.display_surface.get_size()[1] // 2 #середина отрисованного экрана по высоте
		self.offset = pygame.math.Vector2()
		self.floor_surf = pygame.image.load('graphic/map+det.png').convert() #добавили задник карты
		self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0)) #отрисовка карты с левого верхнего угла


	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - self.half_width #координата x Линка
		self.offset.y = player.rect.centery - self.half_heigth #координата y Линка
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset #определяем позицию путём сравнения верхнего левого угла с вектором направления
			self.display_surface.blit(sprite.image, offset_pos) #прорисуем новую поверхность и отрисуем её

	def enemy_update(self, player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)