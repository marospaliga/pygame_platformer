import pygame, time
import sys
import random


pygame.display.set_caption("Name of Game")

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((700, 500))


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30 , 30))
        self.image.fill((255, 0, 50))

        self.rect = self.image.get_rect()
        self.hero_velocity = [0, 0]

        self.is_jumping= False
        self.is_falling= False
        self.is_grounded = False

        self.jump_max = 12
        self.jump_current = 0

    def moving(self, dt):
       pass

    def gravity(self, dt):
        if self.rect.centery < 480 and self.is_jumping == False and self.is_grounded == False:
            self.is_falling = True
            self.jump_current = 0
            self.hero_velocity[1] += 600 * dt
        else: 
            self.is_falling = False
            
    
    def jump(self, dt):
        if self.is_falling == False and self.jump_current < self.jump_max:
            self.hero_velocity[1] -= 600 * dt
            self.jump_current += 50 * dt
            self.is_jumping = True  
            self.is_grounded = False  
        elif self.jump_current >= self.jump_max:
            self.is_jumping = False
            self.jump_current = 0

    def handle_collisions(self, objects):
        self.is_grounded = False  # Reset at start
        
        for object in objects:
            if self.rect.colliderect(object.rect):
                            
                if self.rect.bottom > object.rect.bottom:
                    self.rect.top = object.rect.bottom + 5
                    self.is_falling = True
                    self.is_jumping = False

                    self.jump_current = self.jump_max


                elif self.rect.top < object.rect.top :
                    self.rect.bottom = object.rect.top + 1
                    self.is_grounded = True
                    self.is_falling = False   

            
                break  
 

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

        self.plat_coor_x= x
        self.plat_coor_y= y

        self.image = pygame.Surface((width , height))
        self.image.fill((0, 255, 50))

    def move(self, dt):
        self.rect.x -= 100 * dt

class GameMechanics(object):
    def __init__(self):
        self.plat_spawn_time = 3
        self.plat_current_time = 0
    def spawn(self):
        plat = Platform(650, random.randint(100, 500), 200, 20)
        platforms.add(plat)
        platforms_list.append(plat)


previous_time = time.time()    
dt = 0


hero = Hero(100, 400)
#plat1 = Platform(200, 400, 200, 20)
#plat2 = Platform(400, 300, 200, 20)
platforms_list = []
platforms = pygame.sprite.Group()
game_mechanics = GameMechanics()
game_mechanics.spawn()
game_mechanics.spawn()
game_mechanics.spawn()
game_mechanics.spawn()
game_mechanics.spawn()


while True:


    now = time.time()
    dt = now - previous_time
    previous_time = now

   
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
            sys.exit()
    


    hero.is_jumping = False
    

    key_state = pygame.key.get_pressed()
    
    if key_state[pygame.K_SPACE] == True:
        hero.jump(dt)
            
    if key_state[pygame.K_a] == True:
        #hero.rect.centerx += - 1* hero.hero_velocity * dt
        hero.hero_velocity[0] -= 500 * dt

    if key_state[pygame.K_d] == True:
        #hero.rect.centerx +=  + 1* hero.hero_velocity  * dt
         hero.hero_velocity[0] += 500 * dt

    if game_mechanics.plat_current_time < game_mechanics.plat_spawn_time:
        game_mechanics.plat_current_time += 1.3 * dt

        
    else:
        
        game_mechanics.plat_current_time = 0
        game_mechanics.spawn()
        platforms_list[0].kill()
        platforms_list.pop(0)
        print(platforms_list,"/", platforms)

    hero.gravity(dt)
    hero.handle_collisions(platforms)

    for platform in platforms:
        platform.move(dt)


    hero.moving(dt)
    
    hero.hero_velocity = [0, 0]
    screen.fill(0)
    
    screen.blit(hero.image, hero.rect.topleft)

    for platform in platforms:
        screen.blit(platform.image, platform.rect.topleft)
        
   
    pygame.display.update()
    clock.tick(60)
