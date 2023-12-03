import pygame

# Game Setup
WIDTH = 1920
HEIGHT = 1080
DEBUG = False
DEBUG_TIMER = 300
FPS = 30
RENDER_DISTANCE = 3

#Player Settings
PLAYER_START_X = WIDTH // 2
PLAYER_START_Y = HEIGHT // 2
PLAYER_SIZE = 2
PLAYER_SPEED = 3
XP_MULTI = 1.3
BASE_LEVEL_XP = 100



#Attack Settings
ATTACK_COOLDOWN = 30
BULLET_SCALE = 1
BULLET_SPEED = 3
BULLET_LIFETIME = 2500

ATTACK_OFFSET_X = 20
ATTACK_OFFSET_Y = -26

#Enemy Settings
ENEMY_SPEED = 1
ENEMY_SIZE = 2
#Spawn AREA
SPAWN_MIN = 800
SPAWN_MAX = 2000

#Tile Settins
T_WIDTH = 894
T_HEIGHT = 894

#Colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

game_stats = {
    "enemies_killed_or_removed": 0, 
    "necromancer_death_count": 0, 
    "nightborne_death_count": 0, 
    "coins": 0, 
    "health_potion_heal": 20, 
    "current_wave": 1, 
    "number_of_enemies": [5, 6,7], 
    "wave_cooldown": 6000, 
    "num_health_potions": 3,
    "Current_Level" : 0,

}