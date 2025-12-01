import pygame
import math
import time
import random
from utils import scale_image, blit_rotate_center


# import asset
BACKGROUND = scale_image(pygame.image.load("imgs/angkasa.png"), 0.8)
PLANE_1 = pygame.image.load("imgs/jet_1.png")
PLANE_2 = scale_image(pygame.image.load("imgs/jet_2.png"), 0.2)
BULLET = scale_image(pygame.image.load("imgs/bullet.png"), 0.1)
MASK_BULLET = pygame.mask.from_surface(BULLET)
MASK_PLANE_2 = pygame.mask.from_surface(PLANE_2)
ALIEN_1 = scale_image(pygame.image.load("imgs/alien(1).png"),0.15)


# MAKE A wincow for game
WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
print(WIDTH,HEIGHT)
pygame.display.set_caption("aircraf war")
FPS = 60

pygame.mixer.init()
pygame.font.init()


# load music :
pygame.mixer.music.load("music/basic_gun.mp3")
pygame.mixer.music.load("music/bullet_hit.mp3")


# chanel music 
basic_gun_music = pygame.mixer.Channel(0)
bullet_hit_music = pygame.mixer.Channel(1)


# define color 
GREEN_NEON = (0, 255, 156)
BLACK = (0,0,0)
BLUE = (0,0,128)

TEXT_DICT = {
    "hp" : (WIDTH //2, HEIGHT -30),
    "bullet" : (WIDTH //3, HEIGHT -30),
    "level" : ((WIDTH // 3) * 2,HEIGHT - 30)
}




class aircraft:
    def __init__(self, max_vel):
        self.img = self.IMG
        self.vel = 0
        self.max_vel = max_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hp = 7

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, dx, dy):

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

    def get_hit(self, damage):

        self.hp -= damage
        if self.hp <= 0 :
            return ("end")
        
    def collide(self,mask,x,y):
        MASK_PLANE_2 = pygame.mask.from_surface(self.img)
        offset = (self.x - x, self.y - y) 
        poi = mask.overlap(MASK_PLANE_2,offset)

        if poi :
            return("kena bullet ni")
        
        return None






class player_aircraft(aircraft):
    IMG = PLANE_2
    START_POS = (350, 630)


class bullet:
    def __init__(self,win, player, bullet, damage = 1):
        self.bullets = []
        self.win = win
        self.player = player
        self.bullet_img = bullet
        self.damage = damage
    
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
        bullet_hit_music.play(pygame.mixer.Sound("music/bullet_hit.mp3"),loops=0)

class Alien:
    def __init__(self,img,vel,alien_count):
        self.vel = vel
        self.img = img
        self.alien_count = alien_count
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.position = self.alien_position(alien_count)
        print(f"alien position varibale {self.position}")
        self.hp = [3 for _ in range(self.alien_count)]

    def move(self):
        for y in self.position:
            y[1] += self.vel
        
        self.position[:] = [pos for pos in self.position if pos[1] < HEIGHT]


    def draw (self,win):
        for x,y in self.position:
            win.blit(self.img,(x,y))

    def alien_position(self,alien_number):
        alien_pos = []
        for i in range(alien_number):
            y_pos = (0 - self.height)
            x_random = random.randint(int(0+self.width),int(819-self.width))
            y_random = random.randint(int(-1000),int(0 - self.height))

            alien_pos.append([x_random,y_random])

        return alien_pos

    def collide(self,mask, x = 0, y = 0):
        alien_mask = pygame.mask.from_surface(self.img)

        for index, (alien_x, alien_y) in enumerate(self.position):
            offset = (int(alien_x - x), int(alien_y - y))
            poi = mask.overlap(alien_mask,offset)
            alien_hit_pos = [alien_x,alien_y]

            if poi :
                return([poi,alien_hit_pos,index])
        return None
    

    def get_hit(self, damage, alien_collide):
        position_hit = alien_collide[1]
        alien_hit_pos = alien_collide[2]

        # if self.hp[alien_hit_pos] == 0:
        #     self.hp.pop(alien_hit_pos)
        #     self.position.remove(position_hit)

        
        self.hp[alien_hit_pos] -= damage
        if self.hp[alien_hit_pos] <= 0 :
            self.hp.pop(alien_hit_pos)
            self.position.remove(position_hit)


class bulletAlien:
    def __init__(self,win,bulletAlien_img,alien,vel = 3,):
        
        self.win = win
        self.damage = 1
        self.img = bulletAlien_img
        self.vel = vel
        self.alien = alien
        self.bullets = [[] for _ in range(len(self.alien.position))]



    def spawn_bullet(self,player):
        for index, (x,y) in enumerate(self.alien.position):
            if 0 <= y <= HEIGHT:

                alien_center_x = x + self.alien.width / 2
                alien_center_y = y + self.alien.height / 2


                player_center_x = player.x + player.width/2
                player_center_y = player.y + player.height/2

                dx = player_center_x - alien_center_x
                dy = player_center_y - alien_center_y

                angle = math.atan2(dy,dx)

                vx = math.cos(angle) * self.vel
                vy = math.sin(angle) * self.vel

                self.bullets[index].append([alien_center_x,alien_center_y,vx,vy,angle])


    def update_bullet(self):
        for bullet_list in self.bullets:
            for b in bullet_list:
                b[0] += b[2] 
                b[1] += b[3]

        for i in range(len(self.bullets)):
            self.bullets[i] = [b for b in self.bullets[i] if b[1] < HEIGHT and 0 <= b[0] <= WIDTH ]



    def draw_bullets(self):
        for bullest_list in self.bullets:
            for x,y,vx,vy,angle in bullest_list:
                blit_rotate_center(self.win,self.img,(x,y),angle)

    def bullet_hit (self,arry_1,arry_2):
        del self.bullets[arry_1][arry_2]
        bullet_hit_music.play(pygame.mixer.Sound("music/bullet_hit.mp3"),loops=0)
        

                    

def draw(win, images, player_aircraft,alien):
    for img, pos in images:
        win.blit(img, pos)

    player_aircraft.draw(WIN)
    player_bullet.draw_bullets()
    alien.draw(WIN)
    alien_bullet.draw_bullets()
    info_text(TEXT_DICT,alien,player,player_bullet)
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

def info_text(position_dict,alien = None ,aircraft = None,bullet = None,):
    font = pygame.font.Font('font/ARCADECLASSIC.TTF', 30)
    if aircraft :
        # for hp aircraft / hp player
        hp_aircraft_text = f"HP  {aircraft.hp}"
        hp_render = font.render(hp_aircraft_text,True,GREEN_NEON,BLUE)
        text_hp_rect = hp_render.get_rect()
        text_hp_rect.center = position_dict["hp"]
        WIN.blit(hp_render,text_hp_rect)
    if bullet:
        # for damage level bullet 
        damage_bullet_text = f"DAMAGE  {bullet.damage}"
        damage_bullet_render = font.render(damage_bullet_text,True,GREEN_NEON,BLUE)
        text_damage_rect = damage_bullet_render.get_rect()
        text_damage_rect.center = position_dict["bullet"]
        WIN.blit(damage_bullet_render,text_damage_rect)

    if alien:

        level_text = f"LEVEL {"1"}"
        level_render = font.render(level_text,True,GREEN_NEON,BLUE)
        level_rect = level_render.get_rect()
        level_rect.center = position_dict["level"]
        WIN.blit(level_render,level_rect)



    



run = True
clock = pygame.time.Clock()

images = [
    (BACKGROUND, (0, 0))
]



player = player_aircraft(6)
alien = Alien(ALIEN_1,1,5)
player_bullet = bullet(WIN,player,BULLET)
alien_bullet = bulletAlien(WIN,BULLET,alien,2)

last_bullet_time = 0
last_bullet_alien = 0
bullet_delay_alien = 2500
bullet_delay = 100
level = 0

while run:
  
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    draw(WIN, images, player,alien)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    
    last_bullet_time = move(player,last_bullet_time,bullet_delay)
    player_bullet.update_bullets()
    alien.move()

    if current_time - last_bullet_alien > bullet_delay_alien:
        alien_bullet.spawn_bullet(player)
        last_bullet_alien = current_time
    alien_bullet.update_bullet()



    
    for bx, by in player_bullet.bullets:
        alien_collide_bullet = alien.collide(MASK_BULLET,bx, by)
        
        if alien_collide_bullet :
            remove = [bx,by]     
            player_bullet.bullet_hit(remove)
            alien.get_hit(player_bullet.damage,alien_collide_bullet)

    alien_collide_aircraft = alien.collide(MASK_PLANE_2,player.x,player.y)
    if alien_collide_aircraft:
        aircraft_current_hp = player.hp
        alien_hit_hp = alien.hp[alien_collide_aircraft[2]]
        player_status = player.get_hit(alien_hit_hp)
        alien.get_hit(aircraft_current_hp,alien_collide_aircraft)
        if player_status == "end":
            run = False

    for index1,(bullet_list) in enumerate(alien_bullet.bullets):
        for index2,(x, y, vx, vy, angle) in enumerate(bullet_list):
            bullet_alien_colide_aircraft = player.collide(MASK_BULLET,x,y)
            if bullet_alien_colide_aircraft:
                alien_bullet.bullet_hit(index1,index2)
                player.get_hit(alien_bullet.damagedd)
                


    


pygame.quit()
