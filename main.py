#import
import pygame
import random
from pygame import mixer

#initialise python
pygame.init()

#screen
screen_width=400
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("AMOGUS")

#colours
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
cyan=(0,255,255)
green=(0,255,0)

#fps
clock=pygame.time.Clock()
fps=60

#game variables
screen_thresh=200
gravity=1
max_plat=10
scroll=0
bg_scroll=0
game_over=False
score=0

#music
pygame.mixer.music.load("images/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

#font
font_small=pygame.font.SysFont("Comic Sans",24)
font_big=pygame.font.SysFont("Lucida Sans",24)

#images
player_img=pygame.image.load("images/red.png")
bg_img=pygame.image.load("images/background.png")
plat_img=pygame.image.load("images/plat.png")

#text function
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))

#background 
def background(bg_scroll):
    screen.blit(bg_img,(0,0+bg_scroll))
    screen.blit(bg_img,(0,-600+bg_scroll))

#player movement
class Player():
    def __init__(self,x,y):
        self.image=pygame.transform.scale(player_img,(65,65))
        self.width=25
        self.height=55
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=(x,y)
        self.vel_y=0

        #flipping image
        self.flip=False
    
    def move(self):
        #limit (change in position)
        dx=0
        dy=0
        scroll=0

        #keyboard press
        key=pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx=-12
            self.flip=True
        if key[pygame.K_d]:
            dx=12
            self.flip=False
        
        #gravity
        self.vel_y+=gravity
        dy+=self.vel_y-1

        #boundaries
        if self.rect.left+dx<0:
            dx=-self.rect.left
        if self.rect.right+dx>screen_width:
            dx=screen_width-self.rect.right
        
        #platform collision
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                #check if player is above the platform
                if self.rect.bottom<platform.rect.centery:
                    if self.vel_y>0:
                        self.rect.bottom=platform.rect.top
                        dy=0
                        self.vel_y=-20
        
        #infinite screen
        if self.rect.top<=screen_thresh:
            if self.vel_y<0:
                scroll=-dy

        #updating position
        self.rect.x+=dx
        self.rect.y+=dy+scroll

        return scroll
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),(self.rect.x-20,self.rect.y-10))
        pygame.draw.rect(screen,white,self.rect,2)

#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)

        self.image=pygame.transform.scale(plat_img,(width+5,12))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    
    def update(self,scroll):
        #update the platform for infinity
        self.rect.y+=scroll

        #generating infinite platorms
        if self.rect.top>screen_height:
            self.kill()

player=Player(screen_width//2,screen_height-150)

#sprite group for platform
platform_group=pygame.sprite.Group()

#start platform
platform=Platform(screen_width//2 -30,screen_height-30,60)
platform_group.add(platform)


run=True
while run:
    #fps limiter
    clock.tick(fps)

    if game_over==False:
        #player movement
        scroll=player.move()

        #background
        bg_scroll+=scroll
        if bg_scroll>=600:
            bg_scroll=0
        background(bg_scroll)
        
        draw_text("score:"+str(score),font_small,red,0,0)
        #draw player
        player.draw()

        #generating platforms
        if len(platform_group)<max_plat:
            plat_width=random.randint(40,60)
            plat_x=random.randint(0,screen_width-plat_width-5)
            plat_y=platform.rect.y-random.randint(80,120)
            platform=Platform(plat_x,plat_y,plat_width)
            platform_group.add(platform)

        platform_group.update(scroll)

        #update score
        if scroll>0:
            score+=scroll

        #draw platform
        platform_group.draw(screen)

        #check if bird is below screen (game over)
        if player.rect.top>screen_height:
            game_over=True
    else:
        draw_text("GAME OVER",font_big,black,120,200)
        draw_text("SCORE:"+str(score),font_big,cyan,130,250)
        draw_text("PRESS SPACE TO PLAY AGAIN",font_small,green,25,300)
        draw_text("GG",font_big,white,160,350)

        key=pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            #resetting all variables
            game_over=False
            score=0
            scroll=0

            #repostion player to start
            player.rect.center=(screen_width//2,screen_height-150)
            #reset platforms
            platform_group.empty()
            platform=Platform(screen_width//2 -30,screen_height-40,60)
            platform_group.add(platform)

    #closing the game
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    
    #updating pygame
    pygame.display.update()

pygame.quit()

