#import pygame module
import pygame
import random
import time
import sys

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)
#setup for sounds
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load("continious.mp3")
pygame.mixer.music.play(-1)
move_up_sound = pygame.mixer.Sound("beep.wav")
move_down_sound = pygame.mixer.Sound("beep.wav")
move_front_sound = pygame.mixer.Sound("beep.wav")
move_back_sound = pygame.mixer.Sound("beep.wav")

collision_sound = pygame.mixer.Sound("collision.wav")
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player,self).__init__()
        self.surf = pygame.image.load("jett.png").convert()
        self.surf.set_colorkey((255, 255, 255),RLEACCEL)

        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            move_back_sound.play()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            move_front_sound.play()
        #keep player inside the SCREEN
        if self.rect.left<0:
            self.rect.left = 0
        if self.rect.right>SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top<=0:
            self.rect.top = 0
        if self.rect.bottom>=SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
#defining enemy class


class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(enemy,self).__init__()

        self.surf = pygame.Surface((20,10))
        self.surf = pygame.image.load("misile.png").convert()
        self.surf.set_colorkey((255, 255, 255),RLEACCEL)
        #self.surf.fill((0,0,255))
        self.rect = self.surf.get_rect(
        center = (
        random.randint(SCREEN_WIDTH+10,SCREEN_WIDTH+100),
        random.randint(0,SCREEN_HEIGHT),
        )
        )
        self.speed = random.randint(5,20)

    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.left<0:
            self.kill()

class cloude(pygame.sprite.Sprite):
    def __init__(self):
        super(cloude,self).__init__()
        self.surf = pygame.image.load("images.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
    #    self.surf = pygame.Surface((30,30))
    #    self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(
        center = (
        random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
        random.randint(0,SCREEN_HEIGHT),
        )
        )

    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.left < 0:
            self.kill()



screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Animesh")
#create a user event
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUDE = pygame.USEREVENT+2
pygame.time.set_timer(ADDCLOUDE,500)
myfont = pygame.font.SysFont("monospace", 16)
score = 0
#creating object for class player

player = player()

#create groups to hold enemy sprite and all sprites
#enemies is used for collision detection and position update
#all sprite is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#set the game speed

clock = pygame.time.Clock()
aa = 30
running = True
start_time = time.time()

while running:
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
    # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud?
        elif event.type == ADDCLOUDE:
            new_cloud = cloude()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    screen.fill((135, 206, 250))
    #screen.blit(player.surf,player.rect)
    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    if pygame.sprite.spritecollideany(player, enemies):
    # If so, then remove the player and stop the loop
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        move_back_sound.stop()
        move_front_sound.stop()
        pygame.mixer.music.stop()
        collision_sound.play()
        time.sleep(3)
        pygame.quit()
        #running = False

    scoretext = myfont.render("Your Score : {0}".format(score), 1, (0,0,50))
    screen.blit(scoretext, (5, 10))
    score += 1

    pygame.display.flip()
    #ensure the program makes 30 frames per seconds
    clock.tick(aa)
    aa = aa+.03

pygame.mixer.quit()

