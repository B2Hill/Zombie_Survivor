

# Game Setup
WIDTH = 1920
HEIGHT = 1080
DEBUG = True
FPS = 60

#Player Settings
PLAYER_START_X = WIDTH // 2
PLAYER_START_Y = HEIGHT // 2
PLAYER_SIZE = 2
PLAYER_SPEED = 8


#Attack Settings
ATTACK_COOLDOWN = 20
BULLET_SCALE = 1
BULLET_SPEED = 5
BULLET_LIFETIME = 750

ATTACK_OFFSET_X = 20
ATTACK_OFFSET_Y = -26

#Enemy Settings
ENEMY_SPEED = 4


#Colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)


game_stats = {
    "enemies_killed_or_removed": 0, "necromancer_death_count": 0, "nightborne_death_count": 0, "coins": 0, "health_potion_heal": 20, "current_wave": 1, "number_of_enemies": [5, 6,7], "wave_cooldown": 6000, "num_health_potions": 3
}