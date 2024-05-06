import pygame #Снова обращаемся к PyGame
pygame.init() #Используем базовый конструктор
font = pygame.font.Font(None, 30) #Указываем шрифт

def debug(info, y = 10, x = 10):  #Сама функция дебага
	display_surface = pygame.display.get_surface() #Получаем ссылку на текущую установленную поверхность отображения в игре
	debug_surf = font.render(str(info), True, "Red") #Рендерим текст (я сделал его красным)
	debug_rect = debug_surf.get_rect(topleft = (x, y)) #Указывамем место отображения инфы на экране (левый верхний угол)
	pygame.draw.rect(display_surface, "White", debug_rect) #Делаем микро-консоль в виде прямоугольника (и да он белый, будет белая консоль с красным текстом)
	display_surface.blit(debug_surf, debug_rect) #Собираем нашу микро-консоль с параметрами текста