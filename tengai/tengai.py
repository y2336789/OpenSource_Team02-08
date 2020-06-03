import os
import pygame
import random
pygame.init()

WHITE = (255, 255, 255)
screen_width = 1024
screen_height = 512
screen = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Tengai")


clock = pygame.time.Clock()


current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")


battleship = pygame.image.load(os.path.join(image_path, "plane.png"))
battleship_size = battleship.get_rect().size
battleship_width = battleship_size[0]
battleship_height = battleship_size[1]
battleship_x_pos = 0
battleship_y_pos = (screen_height/2) - battleship_height

battleship_to_x = 0
battleship_to_y = 0

battleship_speed = 4
###################################################################
background = pygame.image.load(os.path.join(image_path, "background.png"))
background_width = 1024
background2 = background.copy()
background_x = 0
background2_x = background_width

###################################################################
bat = pygame.image.load(os.path.join(image_path,"bat.png"))
bat_size = bat.get_rect().size
bat_width = bat_size[0]
bat_height = bat_size[1]
bat_x = screen_width
bat_y = random.randrange(0,screen_height)

bat_speed = 7

###################################################################
dragon = pygame.image.load(os.path.join(image_path,"fireball.png"))
dragon_size = dragon.get_rect().size
dragon_width = dragon_size[0]
dragon_height = dragon_size[1]
dragon_x = screen_width - dragon_size[0]
dragon_y = random.randrange(0,screen_height - dragon_height)
dragon_speed = 5

###################################################################
bullet = pygame.image.load(os.path.join(image_path,"bullet.png"))

bullet_xy = []

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
                 running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                battleship_to_y -= battleship_speed
            elif event.key == pygame.K_DOWN:
                battleship_to_y += battleship_speed
            elif event.key == pygame.K_LEFT:
                battleship_to_x -= battleship_speed
            elif event.key == pygame.K_RIGHT:
                battleship_to_x += battleship_speed
            elif event.key == pygame.K_LSHIFT:
                battleship_to_x=0
                battleship_to_y=0
            elif event.key == pygame.K_SPACE:
                bullet_x = battleship_x_pos + battleship_width
                bullet_y = battleship_y_pos + bat_height/2
                bullet_xy.append([bullet_x, bullet_y])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                battleship_to_x = 0
            elif event.type == pygame.K_UP or event.type == pygame.K_DOWN:
                battleship_to_y = 0

    bat_x -= bat_speed
    if bat_x <= 0:
        bat_x = screen_width
        bat_y = random.randrange(0, screen_height - bat_height)

    dragon_x -= dragon_speed
    if dragon_x <= (screen_width / 4) * 3:
        dragon_x = (screen_width / 4)* 3
    
    '''if dragon_x == (screen_width / 4) * 3:
        if dragon_y < (screen_height /2):
            dragon_y -= dragon_speed
        elif dragon_y >= (screen_height /2):
            dragon_y += dragon_speed

        if dragon_y >= screen_height - dragon_height:
            dragon_y -= dragon_speed
    
        if dragon_y >= 0 + dragon_height:
            dragon_y += dragon_speed'''
    
    battleship_x_pos += battleship_to_x
    battleship_y_pos += battleship_to_y

    if battleship_x_pos < 0:
        battleship_x_pos = 0
    elif battleship_x_pos > screen_width - battleship_width:
        battleship_x_pos = screen_width - battleship_width
    elif battleship_y_pos < 0:
        battleship_y_pos = 0
    elif battleship_y_pos > screen_height - battleship_height:
        battleship_y_pos = screen_height - battleship_height

    background_x -= 2
    background2_x -= 2

    if background_x == -background_width:
        background_x = background_width

    if background2_x == -background_width:
        background2_x = background_width



    if len(bullet_xy) != 0:
        for i, bxy in enumerate(bullet_xy):
            bxy[0] += 15
            bullet_xy[i][0] = bxy[0]
            if bxy[0] >= screen_width:
                bullet_xy.remove(bxy)

    screen.blit(background, (background_x, 0))
    screen.blit(background2,(background2_x, 0))
    screen.blit(battleship, (battleship_x_pos, battleship_y_pos))
    screen.blit(bat, (bat_x, bat_y))
    screen.blit(dragon, (dragon_x, dragon_y))

    if len(bullet_xy) != 0:
        for bx, by in bullet_xy:
            screen.blit(bullet, (bx, by))
    
    pygame.display.update()
    

pygame.quit()

    
   
    
