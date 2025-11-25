import pygame
import math
import time
from utils import scale_image, blit_rotate_center


# import asset
BACKGROUND = scale_image(pygame.image.load("imgs/angkasa.png"), 0.8)
PLANE_1 = pygame.image.load("imgs/jet_1.png")
PLANE_2 = scale_image(pygame.image.load("imgs/jet_2.png"), 0.2)
BULLET = scale_image(pygame.image.load("imgs/bullet.png"), 0.1)

# MAKE A wincow for game
WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("aircraf war")
FPS = 60


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


    def update_bullets(self):
        for b in self.bullets:
            b[1] -= 10

        self.bullets[:] = [b for b in self.bullets if b[1] > -50]


    def draw_bullets(self,):
        for x, y in self.bullets:
            self.win.blit(BULLET, (x, y))



    

# def spawn_bullet(player):
#     x = player.x + player.width / 2 - BULLET.get_width() / 2
#     y = player.y
#     bullets.append([x, y])


# def update_bullets():
#     for b in bullets:
#         b[1] -= 10

#     bullets[:] = [b for b in bullets if b[1] > -50]


# def draw_bullets(win):
#     for x, y in bullets:
#         win.blit(BULLET, (x, y))


def draw(win, images, player_aircraft):
    for img, pos in images:
        win.blit(img, pos)

    player_aircraft.draw(WIN)
    player_bullet.draw_bullets()
    pygame.display.update()



run = True
clock = pygame.time.Clock()

images = [
    (BACKGROUND, (0, 0)),
]
player = player_aircraft(6)
last_bullet_time = 0
bullet_delay = 200
player_bullet = bullet(WIN,player,BULLET)
while run:
  
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    draw(WIN, images, player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

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


    player_bullet.update_bullets()


pygame.quit()
