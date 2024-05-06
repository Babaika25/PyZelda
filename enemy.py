import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
	def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, add_exp):
		super().__init__(groups)
		self.sprite_type = 'enemy' #новый тип спрайтов — враги
		self.import_graphics(monster_name) #обращаемся к новой функции перебора картинок
		self.status = 'idle' #установим базовый статус
		self.image = self.animations[self.status][self.frame_index] #перебираем номер фрейма в папке из функции ниже
		self.rect = self.image.get_rect(topleft = pos) #традиционная отрисовка
		self.hitbox = self.rect.inflate(0, -10) #тот же хитбокс, что и ранее
		self.obstacle_sprites = obstacle_sprites #тот же тип тех. спрайта
		self.monster_name = monster_name #имя монстра
		monster_info = monster_data[self.monster_name] #перехват данных монстра по имени
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.vulnerable = True #флаг уязвимости
		self.hit_time = None #время удара
		self.invincibility_duration = 300 #продолжительность неуязвимости
		self.add_exp = add_exp
		self.hit_sound = pygame.mixer.Sound('audio/attack/claw.ogg')
		self.hit_sound.set_volume(0.4)
		self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
		self.attack_sound.set_volume(0.3)

	def import_graphics(self, monster_name):
		self.animations = {'idle': [], 'move': [], 'attack': []} #перебираем возможные варианты анимаций в папках
		main_path = f'graphic/monsters/{monster_name}/' #обращаемся к монстру по имени :)
		for animation in self.animations.keys(): #перебираем все картинки
			self.animations[animation] = import_folder(main_path + animation) #перебор благодаря support-файлу

	def get_player_distance_direction(self, player):
		enemy_vec = pygame.math.Vector2(self.rect.center) #координата врага
		player_vec = pygame.math.Vector2(player.rect.center) #координата Линка
		distance = (player_vec - enemy_vec).magnitude() #Евклидова величина
		if distance > 0:
			direction = (player_vec - enemy_vec).normalize() #вычисление вектора сближения
		else:
			direction = pygame.math.Vector2() #точка, мы друг в друге
		return(distance, direction)

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]
		if distance <= self.attack_radius and self.can_attack:
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self, player):
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage, self.attack_type)
			self.attack_sound.play()
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1] #нанюхивать Линка
		else:
			self.direction = pygame.math.Vector2() #остановиться по координатам

	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldown(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self, player, attack_type):
		if self.vulnerable:	
			self.hit_sound.play()
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.add_exp(self.exp)

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self):
		self.hit_reaction()
		self.move(self.speed)
		self.animate()
		self.cooldown()
		self.check_death()

	def enemy_update(self, player):
		self.get_status(player)
		self.actions(player)