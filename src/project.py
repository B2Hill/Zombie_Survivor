from typing import Iterable, Union
import pygame as pyg
from sys import exit
import math, json



from settings import *
from spritesheet import *

pyg.init()
#Create window
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Zombie Survior")
clock = pyg.time.Clock()

#loads images
background = pyg.transform.scale(pyg.image.load(rf'src/background/Dirt_Background.jpg').convert(), (WIDTH, HEIGHT)) #use rf'src/{folder_path}...' for local testing

#Group Initialization
all_sprites_group = pyg.sprite.Group()
bullet_group = pyg.sprite.Group()
enemy_group = pyg.sprite.Group()


#Character Class
class Player(pyg.sprite.Sprite):
    def __init__(self, Sprite_Location=rf'src\sprites\Player\Option_1\Zombie_Player.png', pos = (WIDTH // 2, HEIGHT //2)):
        super().__init__(all_sprites_group)
        self.zombiesheet = Spritesheet(Sprite_Location)
        #Init Vars
        self.currentFrame = 0
        self.actions = ["Idle","Walk","Attack","Hurt","Die"]
        self.currentAction = self.actions[0]
        self.currentActionState = 0

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

        #Attack Variables
        self.attack = False
        self.attack_cooldown = 0
        self.attack_offset = pyg.math.Vector2(ATTACK_OFFSET_X, ATTACK_OFFSET_Y)
        
        
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
        

    def DEBUG(self):
        print(self.pos)

    

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
            print(f"{self.currentAction} || {self.actions[self.currentActionState]}")
            self.currentFrame = 0
        #SKIP
                

    def user_input(self):
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

        if pyg.mouse.get_pressed() == (1,0, 0) or keys[pyg.K_SPACE]:
            self.attack = True
            self.idletick = 0
            #print(self.angle)
            self.is_attacking()
        else:
            self.attack = False


    def is_idle(self):
        if self.idletick < 500:
            self.idletick += 1
        else:
            self.update_action(0)
        #print(self.idletick)

    def update_action(self,ACTIONSTATE):
        if ACTIONSTATE != self.currentActionState:
            #print(f"ACTIONSTATE CHANGE: \n {self.actions[self.currentActionState]} to {self.actions[ACTIONSTATE]}")
            self.currentFrame = 0
            self.currentActionState = ACTIONSTATE
            self.currentAction = self.actions[ACTIONSTATE]

    def is_attacking(self):
        if self.attack_cooldown == 0:
            
            self.update_action(2)
            self.attack_cooldown = ATTACK_COOLDOWN
            spawn_bullet_pos = list(self.vec_pos)
            
            if self.flipped == False:
                spawn_bullet_pos[0] = self.vec_pos[0] + self.attack_offset[0]
                spawn_bullet_pos[1] = self.vec_pos[1] + self.attack_offset[1]
            else:
                spawn_bullet_pos[0] = self.vec_pos[0] - self.attack_offset[0]
                spawn_bullet_pos[1] = self.vec_pos[1] + self.attack_offset[1]
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)
            #print(spawn_bullet_pos)



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
            self.attack_cooldown -= 1


#Enemy Class
class Enemy(pyg.sprite.Sprite):
    def __init__(self,position=(500,500),Sprite_Location=rf'src\sprites\Player\Option_1\Zombie_Player.png', MinDist = 0):
        super().__init__(enemy_group, all_sprites_group)
        self.zombiesheet = Spritesheet(Sprite_Location)

        self.currentFrame = 0
        self.actions = ["Idle","Walk","Attack","Hurt","Die"]
        self.currentAction = self.actions[0]
        self.currentActionState = 0

        ### SPRITESHEET DATA ###
        self.idle = [pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-0.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-1.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-2.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-3.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-4.png').convert_alpha(), 0, PLAYER_SIZE), pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-5.png').convert_alpha(), 0, PLAYER_SIZE),
                      pyg.transform.rotozoom(self.zombiesheet.parse_sprite(f'Zombie_{self.actions[0]}-6.png').convert_alpha(), 0, PLAYER_SIZE)]
        
        #Image variables
        self.image = self.idle[0]
        

        #Hitbox Variables
        self.hitbox_rect = self.image.get_rect(center = position)
        self.rect = self.hitbox_rect.copy()
        self.flipped = False

        #idle Var
        self.idletick = 0

        #Enemy Stats
        self.health = 20
        self.movement_speed = ENEMY_SPEED
        self.position = pygame.math.Vector2(position)

        #Enemy Movement
        self.direction = pyg.math.Vector2()
        self.velocity = pyg.math.Vector2()
        self.min_distance = MinDist

    def hunt_player(self):
        player_vector = pyg.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pyg.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > self.min_distance:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pyg.math.Vector2(0,0)
        
        self.velocity = self.direction * self.movement_speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

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

    def is_idle(self):
        if self.idletick < 500:
            self.idletick += 1
        else:
            self.update_action(0)
        #print(self.idletick)

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
            print(f"{self.currentAction} || {self.actions[self.currentActionState]}")
            self.currentFrame = 0
        #SKIP
   
    def flip_image(self):
        if self.flipped == True:
            self.image = self.image = pyg.transform.flip(self.image, 1,0)
            #print("FLIP!")
        else:
            self.image = self.image

    def update(self):
        self.update_frame()
        self.is_idle()
        self.hunt_player()
        self.flip_image()



#Bullet Class
class Bullet(pyg.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image =pygame.image.load("src\sprites\FX\Preview\Smoke7.gif").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y 
        
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x_vel = math.cos(self.angle * (2 * math.pi/360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi/360)) * self.speed

        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pyg.time.get_ticks()
    
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
    
    def update(self):
        self.bullet_movement()


class Camera(pyg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pyg.math.Vector2(0,0)

    def C_draw(self):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        #Floor Draw
        self.floor_rect = background.get_rect(topleft = (0,0))
        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
            #print(f"DRAWING || {sprite}")

#Player Initilization
player = Player()
Testbadguy = Enemy(MinDist= 300)


def main():
    #TODO MAIN STATMENT
    #Set Player sprite
    camera = Camera()
    debug = False
   
    while True:
        keys = pyg.key.get_pressed()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_F1:
                    if debug == False:
                        debug = True
                        #print("DEBUG ON")
                    else:
                        debug = False
                        #print("DEBUG OFF")
            if event.type == pyg.KEYUP:
                pass

        #Set Game Background Image
        screen.fill('black')
        camera.C_draw()
        all_sprites_group.update()

        

        #Debug Hitrects
        if debug == True:
            pyg.draw.rect(screen, "red", player.hitbox_rect, width=2)
            pyg.draw.rect(screen, "yellow", player.rect, width=2)

        #Update Display
        pyg.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()