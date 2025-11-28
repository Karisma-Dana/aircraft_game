import pygame
import math
import time
from utils import scale_image, blit_rotate_center


# import asset
BACKGROUND = scale_image(pygame.image.load("imgs/angkasa.png"), 0.8)
PLANE_1 = pygame.image.load("imgs/jet_1.png")
PLANE_2 = scale_image(pygame.image.load("imgs/jet_2.png"), 0.2)
MASK_PLANE_2 = pygame.mask.from_surface(PLANE_2)
BULLET = scale_image(pygame.image.load("imgs/bullet.png"), 0.1)
MASK_BULLET = pygame.mask.from_surface(BULLET)
ALIEN_1 = scale_image(pygame.image.load("imgs/alien(1).png"),0.15)


# MAKE A wincow for game
WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("aircraf war")
FPS = 60

pygame.mixer.init()


# load music :
pygame.mixer.music.load("music/basic_gun.mp3")


# chanel music 
basic_gun_music = pygame.mixer.Channel(0)





class aircraft:
    def __init__(self, max_vel):
        self.img = self.IMG
        self.vel = 0
        self.max_vel = max_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, dx, dy):
        print(self.x, self.y)

        self.x += dx
        self.y += dy

        # aircraft cant be out of window
        if self.x < 0:
            self.x = 0
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height


class player_aircraft(aircraft):
    IMG = PLANE_2
    START_POS = (350, 630)







class bullet:
    def __init__(self,win, player, bullet):
        self.bullets = []
        self.win = win
        self.player = player
        self.bullet_img = bullet
    
    def spawn_bullet(self,player):
        x = self.player.x + self.player.width / 2 - self.bullet_img.get_width() / 2
        y = self.player.y
        self.bullets.append([x, y])
        basic_gun_music.play(pygame.mixer.Sound("music/basic_gun.mp3"), loops= 0)


    def update_bullets(self):
        for b in self.bullets:
            b[1] -= 10

        self.bullets[:] = [b for b in self.bullets if b[1] > -50]


    def draw_bullets(self,):
        for x, y in self.bullets:
            self.win.blit(BULLET, (x, y))


    def bullet_hit(self,hit):
        self.bullets.remove(hit)





class Alien:
    def __init__(self,img,vel,position):
        self.vel = 0
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.position = position


    def draw (self,win):
        for x,y in self.position:
            win.blit(self.img,(x,y))





    def collide(self,mask, x = 0, y = 0):
        alien_mask = pygame.mask.from_surface(self.img)

        for alien_x, alien_y in self.position:
            offset = (int(alien_x - x), int(alien_y - y))
            poi = mask.overlap(alien_mask,offset)

            if poi :
                return(poi)
        return None
      


def draw(win, images, player_aircraft):
    for img, pos in images:
        win.blit(img, pos)

    player_aircraft.draw(WIN)
    player_bullet.draw_bullets()
    alien.draw(WIN)
    pygame.display.update()

def move (player,last_bullet_time,bullet_delay):
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.move(-player.max_vel, 0)
    if keys[pygame.K_d]:
        player.move(player.max_vel, 0)
    if keys[pygame.K_w]:
        player.move(0, -player.max_vel)
    if keys[pygame.K_s]:
        player.move(0, player.max_vel)
    if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_delay:
        player_bullet.spawn_bullet(player)
        last_bullet_time = current_time

    return last_bullet_time



run = True
clock = pygame.time.Clock()

images = [
    (BACKGROUND, (0, 0))
]

alien_pos = [
    [50,50],
    [120,200]
]


player = player_aircraft(6)
alien = Alien(ALIEN_1,0,alien_pos)
player_bullet = bullet(WIN,player,BULLET)

last_bullet_time = 0
bullet_delay = 100

while run:
  
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    draw(WIN, images, player)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    
    last_bullet_time = move(player,last_bullet_time,bullet_delay)
    player_bullet.update_bullets()


    
    for bx, by in player_bullet.bullets:
        if alien.collide(MASK_BULLET, bx, by) :
            print("kena nih")
            remove = [bx,by]
            player_bullet.bullet_hit(remove)
            
    if alien.collide(MASK_PLANE_2,player.x,player.y):
        print("kena nih")

pygame.quit()
