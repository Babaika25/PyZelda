WIDTH = 1280 #Ширина экрана
HEIGTH = 720 #Высота экрана
FPS = 60 #Число FPS
TILESIZE = 64 #Размер тайла (квадрата текстуры)

BAR_HEIGHT = 20 #толщина всех панелек
HEALTH_BAR_WIDTH = 200  #длина панельки здоровья
ENERGY_BAR_WIDTH = 140 #длина панельки энергии
ITEM_BOX_SIZE = 80 #размер значка под предмет
UI_FONT = 'graphic/font/joystix.ttf' #основной шрифт
UI_FONT_SIZE = 18 #кегель шрифта

UI_BG_COLOR = '#222222' #цвет задника
UI_BORDER_COLOR = '#111111' #цвет обводки
TEXT_COLOR = '#EEEEEE' #цвет текста

HEALTH_COLOR = 'red' #цвет здоровья
ENERGY_COLOR = 'green' #цвет энергии

weapon_data = {'sword': {'cooldown': 300, 'damage': 15, 'graphic':'graphic/weapons/sword/full.png'}}

monster_data = {
	'axolot': {'health': 200, 'exp': 400, 'damage': 40, 'attack_type': 'slash', 'attack_sound': 'audio/attack/slash.ogg', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 300},
	'lizard': {'health': 50, 'exp': 100, 'damage': 15,'attack_type': 'claw',  'attack_sound': 'audio/attack/claw.ogg', 'speed': 2, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 400},
	'snake': {'health': 100,'exp':100,'damage': 10,'attack_type': 'claw', 'attack_sound': 'audio/attack/claw.ogg', 'speed': 4, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 350},
	'spirit': {'health': 150,'exp':200,'damage': 15,'attack_type': 'claw', 'attack_sound': 'audio/attack/claw.ogg', 'speed': 3, 'resistance': 3, 'attack_radius': 100, 'notice_radius': 400}}