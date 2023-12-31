from typing import Iterable, Union
import pygame as pyg
from sys import exit
import math
import json
import random

##from pygame.sprite import _Group

from settings import *
from spritesheet import *

pyg.init()
#Create window
screen = pyg.display.set_mode((WIDTH, HEIGHT), flags= pygame.RESIZABLE | pygame.SCALED)
pyg.display.set_caption("Zombie Survior")
clock = pyg.time.Clock()

#loads images
#background = pyg.transform.scale(pyg.image.load(rf'src/background/Dirt_Background.jpg').convert(), (WIDTH, HEIGHT)) #use rf'src/{folder_path}...' for local testing

#Font Load
font = pyg.font.Font("src/font/PublicPixel.ttf",20)
small_font = pyg.font.Font("src/font/PublicPixel.ttf",15)
title_font = pyg.font.Font("src/font/PublicPixel.ttf",60)
score_font = pyg.font.Font("src/font/PublicPixel.ttf",50)

#Group Initialization
background_group = pyg.sprite.Group()
all_sprites_group = pyg.sprite.Group()
Player_bullet_group = pyg.sprite.Group()
Enemy_bullet_group = pyg.sprite.Group()
enemy_group = pyg.sprite.Group()
enemy_group_dead = pyg.sprite.Group()
obstacles_group = pygame.sprite.Group()
player_group = pyg.sprite.Group()
Button_Group = pyg.sprite.Group()
enviroment_group = pyg.sprite.Group()

#Collider
def hitbox_collide(sprite1, sprite2):
    return sprite1.hitbox_rect.colliderect(sprite2.rect)



#Character Class
class Player(pyg.sprite.Sprite):
    def __init__(self, Sprite_Location=rf'src\sprites\Player\Option_1\Zombie_Player.png', pos = (WIDTH // 2, HEIGHT //2)):
        super().__init__(all_sprites_group, player_group)
        self.zombiesheet = Spritesheet(Sprite_Location)
        #Init Vars
        self.currentFrame = 0
        self.actions = ["Idle","Walk","Attack","Hurt","Die"]
        self.currentAction = self.actions[0]
        self.currentActionState = 0
        self.name = "Player"

        ### SPRITESHEET DATA ###
        self.idle = [pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, PLAYER_SIZE)]
        
        ##################################
        #    UPDATE WITH NEW JSON DATA   #
        ##################################
        self.walking = [pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-0.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-1.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-2.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-3.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-4.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-5.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-6.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[1]}-7.png').convert_alpha(), 0, PLAYER_SIZE)]
        
        self.attacking = [pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, PLAYER_SIZE),pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, PLAYER_SIZE)]
        
        self.hurting = [pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, PLAYER_SIZE)]
        
        self.dying = [pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, PLAYER_SIZE)]
        
        #Image variables
        self.image = self.idle[0]
        
        
        #Location Variables
        self.pos = pyg.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED
        self.angle = 0

        #Attack Variables
        self.attack = False
        self.attack_cooldown = 100
        self.attack_offset = pyg.math.Vector2(ATTACK_OFFSET_X, ATTACK_OFFSET_Y)
        self.targetlocation = pyg.math.Vector2(ATTACK_OFFSET_X, ATTACK_OFFSET_Y)
        self.Base_CD = ATTACK_COOLDOWN
        #MOVE Variables
        self.velocity_x = 0
        self.velocity_y = 0
        #Hitbox Variables
        self.pos = pos
        self.vec_pos = pygame.math.Vector2(pos)
        self.hitbox_rect = self.image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.flipped = False

        #idle Var
        self.idletick = 0

        #player stats
        self.health = 100
        self.xp = 0
        self.dmg = 10
        self.isDead = False


    def player_facing(self):
        self.mouse_coords = pyg.mouse.get_pos()

        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - WIDTH // 2)
        self.y_change_mouse_player = (self.mouse_coords[1] - HEIGHT// 2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))

        if(self.mouse_coords[0] < WIDTH // 2 and self.flipped == False):
            self.flipped = True
            #print("LEFT!")
        elif(self.mouse_coords[0] > WIDTH // 2 and self.flipped == True):
            self.flipped = False
            #print("RIGHT!")
            self.rect = self.image.get_rect(center = self.hitbox_rect.center)
        self.flip_image()

    def flip_image(self):
        if self.flipped == True:
            self.image = self.image = pyg.transform.flip(self.image, 1,0)
            #print("FLIP!")
        else:
            self.image = self.image
            #print("NO FLIP!")
        
    def update_frame(self):
        if self.currentAction == self.actions[self.currentActionState]:
                #print(f"{self.currentAction} || {self.actions[self.currentActionState]}")
                if self.currentActionState == 0:
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.idle)) 
                    self.image = self.idle[(self.currentFrame)]
                    
                elif self.currentActionState == 1:
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.walking)) 
                    self.image = self.walking[(self.currentFrame)]
                    
        #Walking load
                elif self.currentActionState == 2:
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.attacking)) 
                    self.image = self.attacking[(self.currentFrame)]
                    
        #Attacking load
                elif self.currentActionState == 3:
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.hurting)) 
                    self.image = self.hurting[(self.currentFrame)]
                    
        #Hurting load
                elif self.currentActionState == 4:
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.dying)) 
                    self.image = self.dying[(self.currentFrame)]
                    
        #Dying load
                else:
                    exit()
        else:
            #print(f"{self.currentAction} || {self.actions[self.currentActionState]}")
            self.currentFrame = 0
        #SKIP
                
    def user_input(self):
        if self.attack_cooldown == 0 and ui.Current_State == 1:
            self.velocity_x = 0
            self.velocity_y = 0
            #print("MOVE!")
            keys = pyg.key.get_pressed()

            if keys[pyg.K_w]:
                self.velocity_y = -self.speed
                self.idletick = 0
                self.update_action(1)
            if keys[pyg.K_s]:
                self.velocity_y = self.speed
                self.idletick = 0
                self.update_action(1)
            if keys[pyg.K_a]:
                self.velocity_x = -self.speed
                self.idletick = 0
                self.update_action(1)
            if keys[pyg.K_d]:
                self.velocity_x = self.speed
                self.idletick = 0
                self.update_action(1)

            if self.velocity_x != 0 and self.velocity_y != 0:
                self.velocity_x /= math.sqrt(2)
                self.velocity_y /= math.sqrt(2)

            if (pyg.mouse.get_pressed() == (1,0, 0) or keys[pyg.K_SPACE]):
                self.attack = True
                self.idletick = 0
                #print(self.angle)
                self.is_attacking()
            else:
                self.attack = False
            if self.idletick > 60 and (keys[pyg.K_w] or keys[pyg.K_a] or keys[pyg.K_s] or keys[pyg.K_d]) == False:
                self.get_closeset_Target()
    def is_idle(self):
        if self.idletick < 500:
            self.idletick += 1
        else:
            self.update_action(0)
        #print(self.idletick)

    def reset(self):
        #Attack Variables
        self.attack = False
        self.attack_cooldown = 100
        self.Base_CD = ATTACK_COOLDOWN
        
        #MOVE Variables
        self.velocity_x = 0
        self.velocity_y = 0
        #Hitbox Variables
        self.hitbox_rect = self.image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.flipped = False

        #idle Var
        self.idletick = 0

        #player stats
        self.health = 100
        self.xp = 0
        self.dmg = 10
        self.isDead = False

        game_level.difficulty = 8

    def update_action(self,ACTIONSTATE):
        if ACTIONSTATE != self.currentActionState:
            #print(f"ACTIONSTATE CHANGE: \n {self.actions[self.currentActionState]} to {self.actions[ACTIONSTATE]}")
            self.currentFrame = 0
            self.currentActionState = ACTIONSTATE
            self.currentAction = self.actions[ACTIONSTATE]

    def get_closeset_Target(self):
        closest_BadGuyVect = (0,0)
        Closest_Distance = 5000000.0
        player_vector = pyg.math.Vector2(self.rect.center)
        if self.attack_cooldown <=0:
            for badguy in enemy_group:
                try:
                    if  badguy.isDead == False and badguy.rect.center != ValueError:
                        enemy_vector = pyg.math.Vector2(badguy.rect.center)
                        try:
                            Distance = (player_vector -  enemy_vector).magnitude()
                        except:
                            print("Taraget find fail")
                        if Distance < Closest_Distance:
                            Closest_Distance = Distance
                            closest_BadGuyVect = enemy_vector
                except:
                    pass
                dx = player_vector[0] - enemy_vector[0]
                dy = enemy_vector[1] - player_vector[1]
                rads = math.atan2(-dy,dx)
                rads %= 2 * math.pi
                self.angle = math.degrees(rads) -180
                if int(Closest_Distance) < 500:
                    self.autoAttack()

            
    def autoAttack(self):
        if self.attack_cooldown <=0:
            self.update_action(2)         
            spawn_bullet_pos = list(self.vec_pos)            
            if self.flipped == False:
                spawn_bullet_pos[0] = self.vec_pos[0] + self.attack_offset[0]
                spawn_bullet_pos[1] = self.vec_pos[1] + self.attack_offset[1]
            else:
                spawn_bullet_pos[0] = self.vec_pos[0] - self.attack_offset[0]
                spawn_bullet_pos[1] = self.vec_pos[1] + self.attack_offset[1]
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, owner=0, damage=self.dmg)
            Player_bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)
        self.attack_cooldown = self.Base_CD

    def is_attacking(self):
            
        self.update_action(2)
        self.attack_cooldown = self.Base_CD
        spawn_bullet_pos = list(self.vec_pos)            
        if self.flipped == False:
            spawn_bullet_pos[0] = self.vec_pos[0] + self.attack_offset[0]
            spawn_bullet_pos[1] = self.vec_pos[1] + self.attack_offset[1]
        else:
            spawn_bullet_pos[0] = self.vec_pos[0] - self.attack_offset[0]
            spawn_bullet_pos[1] = self.vec_pos[1] + self.attack_offset[1]
        self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, damage=self.dmg, owner=0)
        Player_bullet_group.add(self.bullet)
        all_sprites_group.add(self.bullet)


    def get_dmg(self, ammmount):
        if ui.current_health > 0:
            ui.current_health -= ammmount
            self.health= ui.current_health
            if ui.current_health <= 0:
                self.health = 0
                self.isDead = True
    
    def check_collision(self, direction):
        for sprite in obstacles_group:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.velocity_x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.velocity_x < 0:
                        self.hitbox_rect.left = sprite.rect.right
    
    def movement(self):
        if self.velocity_x or self.velocity_y != 0:
            self.update_action(1)
        else:
            self.update_action(0)
        self.hitbox_rect.centerx += self.velocity_x

        self.hitbox_rect.centery += self.velocity_y

        self.rect.center = self.hitbox_rect.center


        #self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        #self.hitbox_rect.center = self.pos
        #self.rect.center = self.hitbox_rect.center

        self.vec_pos = (self.hitbox_rect.centerx, self.hitbox_rect.centery)
        #print(self.vec_pos[0])

    def update(self):
        self.update_frame()
        self.is_idle()
        #self.DEBUG()
        self.user_input()
        self.movement()
        self.player_facing()

        if self.attack_cooldown > 0:
            if self.attack_cooldown > self.Base_CD:
                self.attack_cooldown = self.Base_CD
            self.attack_cooldown -= 1


#Enemy Class
class Enemy(pyg.sprite.Sprite):

    def __init__(self,name = "civ", position=(500,500),Sprite_Location=rf'src\sprites\Player\Option_1\Zombie_Player.png', MinDist = 0):
        super().__init__(enemy_group, all_sprites_group)
        self.Enemysheet = Spritesheet(Sprite_Location)
        self.currentFrame = 0
        self.actions = ["Idle","Walk","Attack","Hurt","Die"]
        self.currentAction = self.actions[0]
        self.currentActionState = 0
        self.name = name

        ### SPRITESHEET DATA ###
        ### Defaults to Civilian Type###
        self.idle = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, ENEMY_SIZE),
                      pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, ENEMY_SIZE),
                      pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, ENEMY_SIZE),
                      pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, ENEMY_SIZE)]
        
        #Image variables
        self.image = self.idle[0]
        
        

        #Hitbox Variables
        self.hitbox_rect = self.image.get_rect(center = position)
        self.rect = self.hitbox_rect.copy()
        self.flipped = False
        self.isDead = False
        self.deathtrigger = False
        #idle Var
        self.idletick = 0
        self.CD_Timer = 0

        #Enemy Stats
        self.health = 20
        self.movement_speed = ENEMY_SPEED
        self.position = pygame.math.Vector2(position)
        self.dmg = 10
        self.xp = 10
        self.xp_given = False
        self.strength = 1

        #Enemy Movement
        self.direction = pyg.math.Vector2()
        self.velocity = pyg.math.Vector2()
        self.min_distance = MinDist
        self.max_distance = 2000

        self.set_EnemyType(self.name)

    def set_EnemyType(self, name):
            if name == "Civ":  ###Civilian Enemy###
                # redo initilization
                self.Enemysheet = Spritesheet(rf'src\sprites\Player\Option_1\Zombie_Player.png')
                self.currentFrame = 0
                self.actions = ["Idle","Walk","Attack","Hurt","Die"]
                self.currentAction = self.actions[0]
                self.currentActionState = 0

                ### SPRITESHEET DATA ###
                self.idle = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, ENEMY_SIZE)]
                self.walk = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, ENEMY_SIZE)]
                self.attack = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, ENEMY_SIZE)]
                self.hurt = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, ENEMY_SIZE)]
                self.die = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, ENEMY_SIZE), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, ENEMY_SIZE),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, ENEMY_SIZE)]
                #Enemy Stats
                self.health = 20
                self.movement_speed = ENEMY_SPEED *1
                self.dmg = 10
                self.xp = 10
                self.xp_given = False
                self.strength = 1
                self.is_Ranged = False
                self.CD = 500

            elif name == "Sold":  ###Soldier Enemy###
                # redo initilization
                self.Enemysheet = Spritesheet(rf'src\sprites\Enemy\Soldier\spritesheet.png')
                self.currentFrame = 0
                self.actions = ["Idle","Walk","Attack","Hurt","Die"]
                self.currentAction = self.actions[0]
                self.currentActionState = 0

                Size = ENEMY_SIZE + 1

                ### SPRITESHEET DATA ###
                self.idle = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-0.png').convert_alpha(), 0, Size),
                             pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-1.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-1.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-1.png').convert_alpha(), 0, Size),
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-2.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-2.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[0]}-2.png').convert_alpha(), 0, Size)]
                
                self.walk = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-0.png').convert_alpha(), 0, Size), 
                             pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-1.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-1.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-1.png').convert_alpha(), 0, Size), 
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-2.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-2.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[1]}-2.png').convert_alpha(), 0, Size)]
                
                self.attack = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-0.png').convert_alpha(), 0, Size), 
                               pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-1.png').convert_alpha(), 0, Size),  pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-1.png').convert_alpha(), 0, Size),  pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-1.png').convert_alpha(), 0, Size), 
                               pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-0.png').convert_alpha(), 0, Size),  pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-0.png').convert_alpha(), 0, Size),pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-0.png').convert_alpha(), 0, Size),
                               pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-1.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-1.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[2]}-1.png').convert_alpha(), 0, Size)]

                self.hurt = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[3]}-0.png').convert_alpha(), 0, Size), 
                             pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[3]}-1.png').convert_alpha(), 0, Size)]
                
                self.die = [pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[4]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[4]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[4]}-0.png').convert_alpha(), 0, Size), 
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[4]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[4]}-0.png').convert_alpha(), 0, Size), pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[4]}-0.png').convert_alpha(), 0, Size), 
                            pyg.transform.rotozoom(self.Enemysheet.parse_sprite(f'Soldier_{self.actions[4]}-1.png').convert_alpha(), 0, Size)]


                                #Enemy Stats
                self.health = 20
                self.movement_speed = ENEMY_SPEED +1
                self.dmg = 20
                self.xp = 30
                self.xp_given = False
                self.strength = 2
                self.min_distance = 300
                self.is_Ranged = True
                self.CD = 300

    def check_alive(self):
        if self.health <=0:
            self.isDead = True
            self.update_action(4)

    def is_attacking(self, EnemyVect, PlayerVect):
            spawn_bullet_pos = list(self.position)
            
            dx = PlayerVect[0] - EnemyVect[0]
            dy = EnemyVect[1] - PlayerVect[1]
            rads = math.atan2(-dy,dx)
            rads %= 2 * math.pi
            angle = math.degrees(rads) -180

            if self.flipped == False:
                spawn_bullet_pos[0] = self.position[0] #+ self.attack_offset[0]
                spawn_bullet_pos[1] = self.position[1] #+ self.attack_offset[1]
            else:
                spawn_bullet_pos[0] = self.position[0] #- self.attack_offset[0]
                spawn_bullet_pos[1] = self.position[1] #+ self.attack_offset[1]
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], angle, owner=1, damage=self.dmg)
            Enemy_bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)

    def hunt_player(self):
        
        player_vector = pyg.math.Vector2(player.rect.center)
        enemy_vector = pyg.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)
        
        if distance > self.min_distance:
            self.direction = (player_vector - enemy_vector).normalize()
            if self.isDead == False : self.update_action(1)
                
        else:
            self.direction = pyg.math.Vector2(0,0)
            if self.CD_Timer <= 0:
                if self.isDead == False: 
                    self.update_action(2)
                    self.CD_Timer = self.CD
                    self.is_attacking(player_vector, enemy_vector)
            if self.currentFrame == len(self.attack)-1:
                if self.isDead == False: 
                    self.update_action(0)
            if self.CD_Timer > 0:
                self.CD_Timer -= 1

        if (distance > self.max_distance):
            self.isDead = True
            self.xp_given = True
           
        self.velocity = self.direction * self.movement_speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        self.hitbox_rect.center = self.rect.center

    def get_vector_distance(self, Vect_1, Vect_2):
        if int(Vect_1[0] - Vect_2[0]) < 0:
            self.flipped = True
        else: 
            self.flipped = False
        return (Vect_1 - Vect_2).magnitude()

    def update_action(self,ACTIONSTATE):
        if ACTIONSTATE != self.currentActionState:
            #print(f"ACTIONSTATE CHANGE: \n {self.actions[self.currentActionState]} to {self.actions[ACTIONSTATE]}")
            self.currentFrame = 0
            self.currentActionState = ACTIONSTATE
            self.currentAction = self.actions[ACTIONSTATE]

            self._reset_idle()

    def is_idle(self):
        if self.isDead == False:
            if self.idletick < 500:
                self.idletick += 1
            else:
                self.update_action(0)
    
    def _reset_idle(self):
        self.idletick = 0
    
    def update_frame(self):
        
        if self.currentAction == self.actions[self.currentActionState]:
                #print(f"{self.currentAction} || {self.actions[self.currentActionState]}")
                if self.currentActionState == 0:  ##IDLE
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.idle)) 
                    self.image = self.idle[(self.currentFrame)]
         #Walking load           
                elif self.currentActionState == 1:  ##Walk
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.walk)) 
                    self.image = self.walk[(self.currentFrame)]
                    
        #Attacking load
                elif self.currentActionState == 2:  ##Attack
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.attack)) 
                    self.image = self.attack[(self.currentFrame)]

                    
        #Hurting load
                elif self.currentActionState == 3: ##Hurt
                    self.currentFrame = ((self.currentFrame + 1)) % (len(self.hurt)) 
                    self.image = self.hurt[(self.currentFrame)]
                    
        #Dying load
                elif self.currentActionState == 4: ##Die
                    if self.currentFrame < len(self.die)-1:
                        self.currentFrame = ((self.currentFrame + 1)) % (len(self.die)) 
                        self.image = self.die[(self.currentFrame)]
                    
        ##Something wihen terribly wrong
                else:
                    exit()
        else:
            #print(f"{self.currentAction} || {self.actions[self.currentActionState]}")
            self.currentFrame = 0
        #SKIP
   
    def flip_image(self):
        if self.flipped == True:
            self.image = self.image = pyg.transform.flip(self.image, 1,0)
            #print("FLIP!")
        else:
            self.image = self.image

    def player_collision(self):
        
        if self.isDead == False:
            if pyg.Rect.colliderect(self.hitbox_rect, player.hitbox_rect):
                player.get_dmg(self.dmg)
                self.isDead = True
                self.xp = 0

    def update(self,cleanup = False):
        if cleanup == True:
                self.kill()
        else:
            self.check_alive()
            self.update_frame()
            if self.isDead == False:
                if self.get_vector_distance(pyg.math.Vector2(player.hitbox_rect.center), pygame.math.Vector2(self.hitbox_rect.center)) < 100:
                    self.player_collision()
                    
                self.is_idle()
                self.hunt_player()
                self.flip_image()
            else: 
                #random Chance to drop power up give player XP
                #play death animation
                if self.xp_given == False:
                    player.xp += self.xp
                    self.xp_given = True
                    #print(f'{self.name}: Gave {self.xp}.')
                if self.deathtrigger == False:
                    self.idletick = 0
                    enemy_group.remove(self)
                    enemy_group_dead.add(self)
                    self.deathtrigger = True
                    game_level.num_of_enemies_spawned -=1
                    game_level.difficulty +=.3
                    game_level.number_of_enemiesMax = game_level.difficulty
                if self.idletick < 500:
                    self.idletick += 1
                else:
                    self.kill()
            
#Bullet Class
class Bullet(pyg.sprite.Sprite):
    def __init__(self, x, y, angle,owner = 0, damage = 0):
        super().__init__()
        self.image =pygame.image.load("src\sprites\FX\Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y 
        self.owner = owner ## 0 = player
        
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x_vel = math.cos(self.angle * (2 * math.pi/360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi/360)) * self.speed

        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pyg.time.get_ticks()
        self.dmg = damage
    
    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.pos =  pyg.math.Vector2(self.x, self.y)
        #print(self.pos)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if pyg.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()
            #print("bullet dead")

    def collisions(self):
        if self.owner == 0:
            hits = pyg.sprite.groupcollide(enemy_group, Player_bullet_group, False, True, hitbox_collide)

            for hit in hits:
                if hit.isDead == False:
                    hit.health -= self.dmg
        else:
            hits = pyg.sprite.groupcollide(player_group, Enemy_bullet_group, False, True, hitbox_collide)

            for hit in hits:
                if hit.isDead == False:
                    player.get_dmg(self.dmg)
                    
                

            
        if pyg.sprite.spritecollide(self, obstacles_group, False): #Wall Collisions
            self.kill()
    
    def update(self):
        self.bullet_movement()
        self.collisions()

class UI():
    def __init__(self):
        self.current_health = 100
        self.max_health = 100
        self.bar_lenth = 100
        self.health_ratio = self.max_health / self.bar_lenth
        self.current_color = None
        self.time = 0
        self.lastroundtime = 0
        self.LVL = 1

        #DEBUG INFO
        self.debugtimer = DEBUG_TIMER
        self.debugtimerbool = False
        self.debugTXT = ""

        #Game States
        self.Game_state = ["Main_Menu", "Playing", "Paused", "Game_Over","LevelUP"]
        self.Current_State = 0 ## Change this once the main menu is working


    def Count_debug_timer(self):
        self.debugtimer -= 1
        if self.debugtimer == 0:
            self.stop_debug_timer()

    def stop_debug_timer(self, timer = DEBUG_TIMER):
        self.debugtimer = timer
        self.debugtimerbool = False

    def display_Debug_txt(self):
        
        debug_txt_surface = font.render(f"{self.debugTXT}", False, RED) #DEBUG TEXT
        debug_rect = debug_txt_surface.get_rect(center = (player.pos[0],player.pos[1]-100))
        screen.blit(debug_txt_surface, debug_rect)

    def display_HP_bar(self):
        pyg.draw.rect(screen, BLACK, (10,15, self.bar_lenth * 3, 20)) #Black

        if self.current_health >= self.max_health * .75:
            pyg.draw.rect(screen, GREEN, (10,15,(self.current_health/self.max_health)*100 * 3, 20)) #Green
            self.current_color = GREEN
        elif self.current_health >= self.max_health * .25:
            pyg.draw.rect(screen, YELLOW, (10,15, (self.current_health/self.max_health)*100 * 3, 20))#YELLOW
            self.current_color = YELLOW
        elif self.current_health >= 0:
            pyg.draw.rect(screen, RED, (10, 15, (self.current_health/self.max_health)*100 * 3, 20))#RED
            self.current_color = RED
        
        pyg.draw.rect(screen, WHITE, (10,15, self.bar_lenth * 3,  20), 4)

    def display_HP_txt(self):
        hp_surface = font.render(f"{player.health} / {self.max_health}", False,self.current_color)
        hp_rect = hp_surface.get_rect(center = (410,25))
        screen.blit(hp_surface, hp_rect)

    def display_XP_txt(self):
        XP_surface = font.render(f"{int(self.NextLVL - player.xp)} XP needed", False, GREEN)
        XP_rect = XP_surface.get_rect(center = (1162 , 30))
        screen.blit(XP_surface, XP_rect)
    
    def display_Level_txt(self):
        self.update_level()
        Level_surface = font.render(f"Level: {self.LVL}",False, GREEN)
        lvl_rect = Level_surface.get_rect(center = (745,28)) ### Set to Adjust with screen Size
        screen.blit(Level_surface, lvl_rect)

    def display_timer(self):
        text_1 = font.render(f'{int(self.time / 1000)} Seconds', True, RED)
        screen.blit(text_1, (10, 50))
        
    def update_level(self):
        self.NextLVL = (BASE_LEVEL_XP * 1.3) * (1 + .2 * self.LVL)
        if player.xp >= self.NextLVL:
            player.xp = 0
            self.LVL += 1
            ui.Current_State = 4 ## Level up State
            self.LVL_UP()

    def LVL_UP(self):
        Button1TXT_surface_Top = font.render("Upgrade", False, RED)
        Button1TXT_rect_Top = Button1TXT_surface_Top.get_rect(center = (WIDTH//2-350,HEIGHT//2-30))
        Button1TXT_surface_Bot = font.render("Health", False, RED)
        Button1TXT_rect_Bot = Button1TXT_surface_Bot.get_rect(center = (WIDTH//2-350,HEIGHT//2+120))

        Button2TXT_surface_Top = font.render(f"Upgrade", False, RED)
        Button2TXT_rect_Top = Button2TXT_surface_Top.get_rect(center = (WIDTH//2,HEIGHT//2-30))
        Button2TXT_surface_Bot = font.render(f"Damage!", False, RED)
        Button2TXT_rect_Bot = Button2TXT_surface_Bot.get_rect(center = (WIDTH//2,HEIGHT//2+120))

        Button3TXT_surface_Top = font.render("Upgrade", False, RED)
        Button3TXT_rect_Top = Button3TXT_surface_Top.get_rect(center = (WIDTH//2+400,HEIGHT//2-20))
        Button3TXT_surface_Bot = font.render("Attack Speed", False, RED)
        Button3TXT_rect_Bot = Button3TXT_surface_Bot.get_rect(center = (WIDTH//2+400,HEIGHT//2+120))
        
        LVLUP_surface = font.render("Level UP!", False, GREEN)
        lvlup_rect = LVLUP_surface.get_rect(center = (WIDTH//2,HEIGHT//2-200))
        screen.blit(LVLUP_surface, lvlup_rect)

        screen.blit(Button1TXT_surface_Top, Button1TXT_rect_Top)
        screen.blit(Button1TXT_surface_Bot, Button1TXT_rect_Bot)

        screen.blit(Button2TXT_surface_Top, Button2TXT_rect_Top)
        screen.blit(Button2TXT_surface_Bot, Button2TXT_rect_Bot)
        if player.Base_CD >= 30:
            screen.blit(Button3TXT_surface_Top, Button3TXT_rect_Top)
            screen.blit(Button3TXT_surface_Bot, Button3TXT_rect_Bot)


    def update_time(self, time):
        self.time = time - self.lastroundtime

    def update(self):
        if player.isDead == False:
            self.display_HP_bar()
            self.display_HP_txt()
            self.display_timer()
            self.display_Level_txt()
            self.display_XP_txt()
            if self.debugtimerbool:
                self.Count_debug_timer()
                
            if self.debugtimer > 0 and self.debugtimerbool:
                self.display_Debug_txt()
               # print(f'{self.debugtimer} || {self.debugtimerbool}')
        else:
            self.debugTXT = "DEFEAT"
            self.display_Debug_txt()
            self.Current_State = 3
            
class enviroment(pyg.sprite.Sprite):
    def __init__(self, x, y, name='Tree'):## Name = Tree, DeadTree, Stump
        super().__init__(enviroment_group, background_group)
        
        self.name = name
        self.image = pyg.image.load('src\sprites\Enviroment\stump.png').convert()
        self.get_IMG(self.name)
        self.pos = (x,y)
        self.distance_from_player = 0
        self.isDead = False
        self.ismoving = False

        self.rect = self.image.get_rect(center = self.pos)

    def get_IMG(self, name):
        if name.lower() == "tree" or "stump" or "deadtree":  ## add more for additional assets
            self.image = pyg.transform.rotozoom(pyg.image.load(f'src\sprites\Enviroment\{name}.png').convert_alpha(), 0, PLAYER_SIZE)
        else:  
            self.image = pyg.image.load(f'src\sprites\Enviroment\stump.png').convert()
            print("ERROR: IMG failed to load || check:  src\sprites\Enviroment\{name}.png")

    def get_distance(self, Vect_1, Vect_2, XYAbs):
        var = 0.0
        if XYAbs == 0:
            var = (Vect_1[0] - Vect_2[0])
            return var
        elif XYAbs == 1:
            var = (Vect_1[1] - Vect_2[1])
            return var
        else:
            var = (Vect_1 - Vect_2).magnitude()
            #print(var)
            return var
        
    def update_distance(self):
        player_vector = pyg.math.Vector2(player.rect.center)
        Tile_vector = pyg.math.Vector2(self.rect.center)
        distance_from_player = self.get_distance(player_vector, Tile_vector, 99)##Absolute Value

        #print(self.distance_from_player)
        if distance_from_player > 8000.0:
            #print("Too Far")
            self.kill()
            
    def update(self):
        self.update_distance()
    
class tile(pyg.sprite.Sprite):
    def __init__(self, size = (T_WIDTH, T_HEIGHT), IMG = 'src/background/Dirt_Background.png', pos = (0,0)):
        super().__init__(background_group)
        self.tile_size = size
        self.image = pyg.image.load(rf'{IMG}').convert()
        self.tile_pos = pos
        self.distance_from_player = 0
        self.isDead = False
        self.ismoving = False
        self.movecheck = False

        self.rect = self.image.get_rect(center = self.tile_pos)
        self.spawn_eviroment()

    def get_distance(self, Vect_1, Vect_2, XYAbs):
        var = 0.0
        if XYAbs == 0:
            var = (Vect_1[0] - Vect_2[0])
            return var
        elif XYAbs == 1:
            var = (Vect_1[1] - Vect_2[1])
            return var
        else:
            var = (Vect_1 - Vect_2).magnitude()
            #print(var)
            return var
              
    def update_tile_pos(self, pos):
        self.rect.centerx =  pos[0]
        self.rect.centery = pos[1]

    def update_distance(self):
        player_vector = pyg.math.Vector2(player.rect.center)
        Tile_vector = pyg.math.Vector2(self.rect.center)
        self.distance_from_player = self.get_distance(player_vector, Tile_vector, 99)##Absolute Value
        self.distance_from_playerX = self.get_distance(player_vector, Tile_vector, 0)#X Value
        self.distance_from_playerY = self.get_distance(player_vector, Tile_vector, 1)#Y Value
        #print(self.distance_from_player)

    def is_moving(self):
        if player.velocity_x or player.velocity_y != 0:
            self.ismoving = True
        else:
            self.ismoving = False

    def move_tile(self,resetbool = False):
        if math.fabs(self.distance_from_playerX) > self.tile_size[0]*2 or math.fabs(self.distance_from_playerY) > self.tile_size[1]*2:
            if self.isDead == False:
                self.isDead = True
        if self.isDead and (self.ismoving or resetbool) == True:
            if self.distance_from_playerX > 2000 and player.velocity_x > 0:
                TMP_Tuple = list(self.tile_pos)
                TMP_Tuple[0] = self.tile_pos[0] + 894 * game_level.max_X_Tiles
                self.tile_pos = TMP_Tuple

            elif self.distance_from_playerX < -2000 and player.velocity_x < 0:
                TMP_Tuple = list(self.tile_pos)
                TMP_Tuple[0] = self.tile_pos[0] - 894 * game_level.max_X_Tiles
                self.tile_pos = TMP_Tuple

            if self.distance_from_playerY > 2000 and player.velocity_y > 0:
                TMP_Tuple = list(self.tile_pos)
                TMP_Tuple[1] = self.tile_pos[1] + 894 * game_level.max_Y_tiles
                self.tile_pos = TMP_Tuple

            elif self.distance_from_playerY < -1800 and player.velocity_y < 0:
                TMP_Tuple = list(self.tile_pos)
                TMP_Tuple[1] = self.tile_pos[1] - 894 * game_level.max_Y_tiles
                self.tile_pos = TMP_Tuple

            self.update_tile_pos(self.tile_pos)
            self.isDead = False
            

    def update(self):
        self.is_moving()
        self.update_distance()
        self.move_tile()
        self.spawn_eviroment()
    
    def spawn_eviroment(self):
        NumberofObjects = random.randrange(4,8)
        CurrentNumberofObjects = 0
        if pyg.sprite.spritecollideany(self, enviroment_group) == None:
            while CurrentNumberofObjects < NumberofObjects:
                Object_posX = random.randrange(-417,417)
                Object_posY = random.randrange(-380,380)

                Enviromenttypes = ['Tree', 'DeadTree', 'Stump']

                Object_posX += self.rect.center[0]
                Object_posY += self.rect.center[1]
                EnviromentObject = enviroment(Object_posX, Object_posY,random.choice(Enviromenttypes))

                CurrentNumberofObjects += 1

class Gamelevel(pyg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pyg.math.Vector2(0,0)
        #self.floor_rect = background.get_rect(topleft = (0,0))

        self.circle_center = player.hitbox_rect.center
        self.enemy_spawn_radius_min = SPAWN_MIN
        self.enemy_spawn_radius_max = SPAWN_MAX
        self.num_of_enemies_spawned = 0
        self.number_of_enemiesMax = 8
        self.difficulty = 8.0
        
        
        self.max_X_Tiles = 4
        self.max_Y_tiles = 4
        self.number_of_tiles_max = self.max_X_Tiles * self.max_Y_tiles
        self.number_of_X_tiles = 0
        self.number_of_Y_tiles = 0
        self.next_tile_x = -T_WIDTH
        self.next_tile_y = -T_HEIGHT
        

        self.enemy_spawn_pos = []
        self.health_spawn_pos = []
        self.create_map()
        self.spawn_timer = 0


    def create_map(self):
        #self.spawn_hp_pots()
        self.spawn_enemies()
        self.create_tiles_INIT()
        pass
    def increaseDifficulty(self):
        self.number_of_enemiesMax += self.difficulty

    def create_tiles_INIT(self):
        while self.number_of_Y_tiles < self.max_Y_tiles:
            if self.number_of_X_tiles < self.max_X_Tiles:
                tile(pos = (self.next_tile_x, self.next_tile_y))
                self.number_of_X_tiles += 1
                self.next_tile_x +=894
            else:
                self.number_of_X_tiles = 0
                self.number_of_Y_tiles += 1
                self.next_tile_x = 0
                self.next_tile_y += 894

    def spawn_enemies(self):
        enemy_name = ["Civ", "Sold"]
        
        while self.num_of_enemies_spawned <= self.number_of_enemiesMax:
            self.circle_center = player.hitbox_rect.center
            rand_angle = 2 * math.pi * random.random()
            r= random.randrange(self.enemy_spawn_radius_min, self.enemy_spawn_radius_max)
            x = r * math.cos(rand_angle) + self.circle_center[0]
            y = r * math.sin(rand_angle) + self.circle_center[1]
            Enemy(name = random.choice(enemy_name), position= (x,y))
            self.num_of_enemies_spawned += 1

    def C_draw(self):
        self.offset.x = player.hitbox_rect.centerx - WIDTH // 2
        self.offset.y = player.hitbox_rect.centery - HEIGHT // 2

        
        for sprite in background_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)


        if DEBUG == True:

            Player_Rect = player.hitbox_rect.copy().move(-self.offset.x, -self.offset.y)
            pyg.draw.rect(screen, RED, Player_Rect, width=2)
            for badguy in enemy_group:
                Enemy_Rect = badguy.rect.copy().move(-self.offset.x, -self.offset.y)
                pyg.draw.rect(screen, RED, Enemy_Rect, width=2)
            for sprite in Player_bullet_group:
                bullet_rect = sprite.rect.copy().move(-self.offset.x, -self.offset.y)
                pyg.draw.rect(screen, WHITE, bullet_rect, width=1)
            for Bg in background_group:
                background_rect = Bg.rect.copy().move(-self.offset.x, -self.offset.y)
                pyg.draw.rect(screen, GREEN, background_rect, width=2)

class Button(pyg.sprite.Sprite):
    def __init__(self, Xpos, Ypos, img=rf"src\sprites\Buttons\Button-Start.png",function = 0):
        self.img = pyg.image.load(img)
        self.rect = self.img.get_rect()
        self.pos = (Xpos, Ypos)
        self.rect.topleft =self.pos
        self.isClicked=False
        self.buttonFunction = ["Start","Quit","Restart","Main Menu","none"]
        self.assignedFunction = function
            
    def update(self):
        screen.blit(self.img, self.pos)
        if DEBUG == True:
            pyg.draw.rect(screen, RED, self.rect, width = 2)

    def ButtonAction(self):
        if self.buttonFunction[self.assignedFunction] == self.buttonFunction[0]:  ##Start Button
            ui.Current_State = 1
        elif self.buttonFunction[self.assignedFunction] == self.buttonFunction[1]:  ##Quit Button
            quit()
        elif self.buttonFunction[self.assignedFunction] == self.buttonFunction[2]:  ##Restart Button
            self.ResetGame()
            ui.Current_State = 1
        elif self.buttonFunction[self.assignedFunction] == self.buttonFunction[3]:  ##Main Menu Button
            self.ResetGame()
            ui.Current_State = 0
        elif self.buttonFunction[self.assignedFunction] == self.buttonFunction[4]: #No Function
            pass

    def ResetGame(self):
        for enemy in enemy_group:
            enemy.isDead = True
            enemy.xp_given = True
            enemy.update(True)
        for enemy in enemy_group_dead:
            enemy.isDead = True
            enemy.xp_given = True
            enemy.update(True)
        for bullet in Player_bullet_group:
            Player_bullet_group.remove(bullet)
            bullet.kill()
        for bullet in Enemy_bullet_group:
            Enemy_bullet_group.remove(bullet)
            bullet.kill()
        player.reset()
        ui.current_health = player.health
        ui.update_time(pyg.time.get_ticks())
        ui.lastroundtime = ui.time + ui.lastroundtime
        ui.LVL = 0
        ui.max_health = 100
        game_level.num_of_enemies_spawned = 0

    def levelup(self, button = 99):
        if button == 0: ## Health Up
                player.health += 50
                ui.max_health += 50
                ui.current_health += 50
        elif button == 1: ## Damage Up
                player.dmg += 5
        elif button == 2: ## Attack Speed up
                player.Base_CD -= 5
        else:
            pass
        ui.Current_State = 1


player = Player()
#Testbadguy = Enemy(MinDist= 200, position=(600,600))
ui = UI()
game_level = Gamelevel()

def main():
    Start_Button = Button((WIDTH//2)-200, HEIGHT//2-150, function=0)
    Quit_Button_1 = Button(WIDTH//2 -200, HEIGHT//2+200, img="src\sprites\Buttons\Button-Quit.png", function=1)
    Restart_Button = Button(100, HEIGHT//2+200, img="src\sprites\Buttons\Button-Restart.png", function=2)
    Quit_Button_2 = Button(WIDTH//2 +400, HEIGHT//2+200, img="src\sprites\Buttons\Button-Quit.png", function=1)
    Menu_Button_2 = Button(WIDTH//2-200, HEIGHT//2, img="src\sprites\Buttons\Button-MainMenu.png", function=3)

    Upgrade_1_Button = Button(WIDTH//2-400, HEIGHT//2, img=rf"src\sprites\Buttons\UpArrow.png", function=4)
    Upgrade_2_Button = Button(WIDTH//2-50, HEIGHT//2, img=rf"src\sprites\Buttons\UpArrow.png", function=4)
    Upgrade_3_Button = Button(WIDTH//2+350, HEIGHT//2, img=rf"src\sprites\Buttons\UpArrow.png", function=4)
    clock.tick(FPS)
    
    
    
   
    while True:
        while ui.Game_state[ui.Current_State] == ui.Game_state[0]:  ## Main Menu state
            keys = pyg.key.get_pressed()
            mouseLoc = pyg.mouse.get_pos() 
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
                if Start_Button.rect.collidepoint(mouseLoc):
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        Start_Button.ButtonAction()
                if Quit_Button_1.rect.collidepoint(mouseLoc):
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        Quit_Button_1.ButtonAction()
            screen.fill('black')
            Start_Button.update()
            Quit_Button_1.update()
            pyg.display.update()
            

        while ui.Game_state[ui.Current_State] == ui.Game_state[1]:  ##Playing State
            ui.update_time(pyg.time.get_ticks())
            keys = pyg.key.get_pressed()
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
                if event.type == pyg.KEYDOWN:  ## Pause Game
                    if event.key == pyg.K_ESCAPE:
                        ui.Current_State=2 ## Pause Game
                    if DEBUG == True:
                        if event.key == pyg.K_F1:
                            #print("F1: Spawn Test baddie")
                            ui.debugTXT = f"Spawn Test Bad guy at: {player.pos[0]+600,player.pos[1]+600}"
                            ui.debugtimerbool = True
                            Testbadguy = Enemy(name= "Sold",  MinDist= 200, position=(player.pos[0]+600,player.pos[1]+600))
                        if event.key == pyg.K_F2:
                            #print("F2: Level up")
                            ui.debugTXT = f"granting 100xp"
                            ui.debugtimerbool = True
                            player.xp += 1000
                if event.type == pyg.KEYUP:
                    pass

            screen.fill('black')
            game_level.C_draw()
            background_group.update()
            all_sprites_group.update()
            ui.update()
            game_level.spawn_enemies()

            pyg.display.update()
            
            

        while ui.Game_state[ui.Current_State] == ui.Game_state[2]:  ##Paused State
            keys = pyg.key.get_pressed()
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        ui.Current_State=1 ## Unpause Game

        while ui.Game_state[ui.Current_State] == ui.Game_state[3]:  ##Game Over
            keys = pyg.key.get_pressed()
            mouseLoc = pyg.mouse.get_pos() 
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
                if Restart_Button.rect.collidepoint(mouseLoc):
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        Restart_Button.ButtonAction()
                if Quit_Button_2.rect.collidepoint(mouseLoc):
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        Quit_Button_2.ButtonAction()
                if Menu_Button_2.rect.collidepoint(mouseLoc):
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        Menu_Button_2.ButtonAction()

            Menu_Button_2.update()
            Restart_Button.update()
            Quit_Button_2.update()
            pyg.display.update()
        
        while ui.Game_state[ui.Current_State] == ui.Game_state[4]:  ##Level up State
            mouseLoc = pyg.mouse.get_pos()
            keys = pyg.key.get_pressed()
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        ui.Current_State=1 ## Unpause Game
            if Upgrade_1_Button.rect.collidepoint(mouseLoc):
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        Upgrade_1_Button.levelup(0)
                        if DEBUG == True : print("HP UP")
            if Upgrade_2_Button.rect.collidepoint(mouseLoc):
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        Upgrade_2_Button.levelup(1)
                        if DEBUG == True :print("DMG UP")
            if Upgrade_3_Button.rect.collidepoint(mouseLoc) and player.Base_CD >= 30:
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        if DEBUG == True :print(player.Base_CD)
                        Upgrade_3_Button.levelup(2)
                        if DEBUG == True :print("AS UP")
            Upgrade_1_Button.update()
            Upgrade_2_Button.update()
            if player.Base_CD >= 30:
                Upgrade_3_Button.update()
            pyg.display.update()

if __name__ == "__main__":
    main()