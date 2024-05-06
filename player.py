import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
	def __init__(self, pos, groups, obstacle_sprites, create_attak, destroy_weapon):
		super().__init__(groups)
		self.image = pygame.image.load('graphic/Test/link.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -26)

		self.import_player_assets()
		self.status = 'down'

		self.attacking = False #статус атаки
		self.attack_cooldown = 400 #кулдаун атаки в милисекундах
		self.attack_time = None #время самой атаки
		self.create_attak = create_attak #создали атаку
		self.destroy_weapon = destroy_weapon #создаём способ удалить оружие
		self.weapon_index = 0 #номер оружия (если у вас будет несколько орудий пыток монстров)
		self.weapon = list(weapon_data.keys())[self.weapon_index] #выбрали конкретное оружие и все его параметры

		self.obstacle_sprites = obstacle_sprites

		self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed': 5} #все параметры героя
		self.health = self.stats['health']#соотношение со здоровьем
		self.energy = self.stats['energy'] #соотношение с энергией
		self.exp = 0 #количество очков
		self.speed = self.stats['speed'] #скорость игрока

		self.vulnerable = True
		self.hurt_time = None
		self.invulnerablity_duration = 500

		self.weapon_attack_sound = pygame.mixer.Sound('audio/attack/slash.ogg')
		self.weapon_attack_sound.set_volume(0.4)

	def import_player_assets(self):
		character_path = 'graphic/Link/'
		self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
		'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
		'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self): #варьируем кнопки
		if not self.attacking:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			elif keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			else:
				self.direction.x = 0

			if keys[pygame.K_SPACE]:
				if self.energy >= 10:
					self.energy -= 10
					self.attacking = True
					self.attack_time = pygame.time.get_ticks()
					self.create_attak()
					self.weapon_attack_sound.play()

	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
		if self.attacking:
			self.direction.x = 0 #координаты по x
			self.direction.y = 0 #координаты по y
			if not 'attack' in self.status: #если нет подписи "attack"
				if 'idle' in self.status: #но есть "idle"
					self.status = self.status.replace('_idle', '_attack') #убираем _idle, но оставляем _attack
				else:
					self.status = self.status + '_attack' #если idle не было, просто стави attack
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack', '') #удаляем attack при завершении статуса

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				self.attacking = False
				self.destroy_weapon()

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerablity_duration:
				self.vulnerable = True

	def animate(self):
		animation = self.animations[self.status] #узнаём статус для ссылки на нужный файл
		self.frame_index += self.animation_speed #добовляем нашу скорость и когда добавится единица (из 0.15), сменяем картинку
		if self.frame_index >= len(animation): #при вылете из массива
			self.frame_index = 0 #возвращаемся к начальной картинке и тем самым зацикливаемся
		self.image = animation[int(self.frame_index)] #указываем картику
		self.rect = self.image.get_rect(center = self.hitbox.center) #указываем хитбокс
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def get_full_weapon_damage(self):
		base_damage = self.stats['attack'] #урон самого Линка
		weapon_damage = weapon_data[self.weapon]['damage'] #урон от выбранного оружия
		return base_damage + weapon_damage

	def energy_recover(self):
		if self.energy < self.stats['energy']:
			self.energy += 0.1
		else:
			self.energy = self.stats['energy']

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.energy_recover()