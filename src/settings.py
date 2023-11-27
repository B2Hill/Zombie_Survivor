import pygame

# Game Setup
WIDTH = 1920
HEIGHT = 1080
DEBUG = True
FPS = 60
RENDER_DISTANCE = 10

#Player Settings
PLAYER_START_X = WIDTH // 2
PLAYER_START_Y = HEIGHT // 2
PLAYER_SIZE = 2
PLAYER_SPEED = 8


#Attack Settings
ATTACK_COOLDOWN = 20
BULLET_SCALE = 1
BULLET_SPEED = 5
BULLET_LIFETIME = 7500

ATTACK_OFFSET_X = 20
ATTACK_OFFSET_Y = -26

#Enemy Settings
ENEMY_SPEED = 4
ENEMY_SIZE = 1
#Spawn AREA
SPAWN_MIN = 800
SPAWN_MAX = 2000


#Colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

enemy_data = {
    "civ": 
        {"health": 100, 
         "attack_damage": 10, 
         "hunting_speed": [4,4,7,7,7], 
         #"image": pygame.image.load("necromancer/roam/0.png"), 
         "image_scale": 1.5, 
         "hitbox_rect": pygame.Rect(0,0,75,100), 
         "animation_speed": 0.2, 
         "roam_animation_speed": 0.05, 
         "death_animation_speed": 0.12, 
         "notice_radius": 500},

    "Soldier": 
        {"health": 100, 
         "attack_damage": 20,
         "hunting_speed": [4,4,6,6,6], 
         #"image": pygame.image.load("nightborne/hunt/1.png"), 
         "image_scale": 1.9, 
         "hitbox_rect": pygame.Rect(0,0,75,90), 
         "animation_speed": 0.1, 
         "roam_animation_speed": 0.12, 
         "death_animation_speed": 0.2, 
         "notice_radius": 400},
}
game_stats = {
    "enemies_killed_or_removed": 0, 
    "necromancer_death_count": 0, 
    "nightborne_death_count": 0, 
    "coins": 0, 
    "health_potion_heal": 20, 
    "current_wave": 1, 
    "number_of_enemies": [5, 6,7], 
    "wave_cooldown": 6000, 
    "num_health_potions": 3
}