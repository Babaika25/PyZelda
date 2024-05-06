import asyncio
import pygame, sys #импортируем библиотеки PyGame и Sys
from settings import * #импорт из файла settings
from level import Level #+++ импорт из файла level класс Level +++

class Game: #основной класс игры
	def __init__(self): #создаём конструктор класса
		pygame.init() #конструктор использует конструкции из библиотеки PyGame
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH)) #забирает из нашего проекта экран в виде размеров в ширину и высоту
		pygame.display.set_caption("PyZelda") #Устанавливаем название нашего окна
		self.clock = pygame.time.Clock() #а также, забирает из проекта время
		self.level = Level() #+++ объёвили Level +++
		main_sound = pygame.mixer.Sound('audio/main.ogg')
		main_sound.play(loops = -1)

	async def run(self): #функция запуска игры
		while True: #до выхода из игры она активна
			for event in pygame.event.get(): #просмотр событий в игре
				if event.type == pygame.QUIT: #сейчас мы можем только выйти и при выходе:
					pygame.quit() #вызываем метод закрытия игры
					sys.exit() #и закрываем окно системы
			self.screen.fill('black') #помимо событий, указываем цвет экрана
			self.level.run() #+++ запустили функцию run в файле level в классе Level +++
			pygame.display.update() #обновляем экран
			self.clock.tick(FPS) #запрашиваем FPS
			await asyncio.sleep(0)

asyncio.run(Game().run())