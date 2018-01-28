import pygame

from datetime import datetime
import time

from random import randint

from NId3.Player import Player
from NId3.Hitbox import Hitbox
from NId3.Projectile import projectile
from NId3.Platform import platform

def process_player_inputs(p1 : Player, p2 : Player):
    keys = pygame.key.get_pressed()  # checking pressed keys
    p1down, p2down = False, False

    #Player 1 inputs
    if keys[pygame.K_c]:
        backgroundColor = (randint(0, 255), randint(0, 255), randint(0, 255))

    if keys[pygame.K_UP]:
        if (datetime.now() - last_press["UP"]).total_seconds() * 1000 >= 350:
            p1.move_in_y(0)

            last_press["UP"] = datetime.now()

    if keys[pygame.K_RIGHT]:
        p1.move_in_x(0)

    if keys[pygame.K_LEFT]:
        p1.move_in_x(1)

    if keys[pygame.K_DOWN]:
        p1down = True
    else:
        p1down = False

    if keys[pygame.K_PERIOD]:
        #allow the shoot every 1000 milliseconds aka 1 second
        if (datetime.now() - last_press["."]).total_seconds() * 1000 >= 700:
            p = projectile(p1.x - proj_size[0], p1.y + p1.dimensions[1]/2 - proj_size[1]/2,
                           WHITE, (0, 0, size[0], size[1]), proj_size, -5, p1, p1down)
            hit_boxes.append(p)

            last_press["."] = datetime.now()

    if keys[pygame.K_SLASH]:
        #allow the shoot every 1000 milliseconds aka 1 second
        if (datetime.now() - last_press["/"]).total_seconds() * 1000 >= 700:
            p = projectile(p1.x + proj_size[0], p1.y + p1.dimensions[1]/2 - proj_size[1]/2,
                           WHITE, (0, 0, size[0], size[1]), proj_size, 5, p1, p1down)
            hit_boxes.append(p)

            last_press["/"] = datetime.now()





    #Player 2 inputs
    if keys[pygame.K_w]:
        if (datetime.now() - last_press["w"]).total_seconds() * 1000 >= 350:
            p2.move_in_y(0)

            last_press["w"] = datetime.now()

    if keys[pygame.K_d]:
        p2.move_in_x(0)

    if keys[pygame.K_a]:
        p2.move_in_x(1)

    if keys[pygame.K_s]:
        p2down = True
    else:
        p2down = False

    if keys[pygame.K_q]:
        #allow the shoot every 1000 milliseconds aka 1 second
        if (datetime.now() - last_press["q"]).total_seconds() * 1000 >= 700:
            p = projectile(p2.x - proj_size[0], p2.y + p2.dimensions[1]/2 - proj_size[1]/2,
                           GREEN, (0, 0, size[0], size[1]), proj_size, -5, p2, p2down)
            hit_boxes.append(p)

            last_press["q"] = datetime.now()

    if keys[pygame.K_e]:
        #allow the shoot every 1000 milliseconds aka 1 second
        if (datetime.now() - last_press["e"]).total_seconds() * 1000 >= 700:
            p = projectile(p2.x + proj_size[0], p2.y + p2.dimensions[1]/2 - proj_size[1]/2,
                           GREEN, (0, 0, size[0], size[1]), proj_size, 5, p2, p2down)
            hit_boxes.append(p)

            last_press["e"] = datetime.now()




#var set
pygame.init()
pygame.font.init()
pygame.mixer.init()

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   1)
BLUE     = (   0,   0, 255)
GREY     = ( 169, 169, 169)
COLORS   = (BLACK,WHITE,GREEN,RED,BLUE)
backgroundColor = (0, 122, 255)

proj_size = (16,16)

size = (1200,800)

done = False

clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 30)



last_press = {"q" : datetime.now(), "e" : datetime.now(), "/" : datetime.now(), "." : datetime.now()
              , "w" : datetime.now(), "UP" : datetime.now()}

#Game initialze

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Nid III")

#initalize game objects
p1 = Player(0, 0, BLACK, (20, 40), (0, 0, 1200, 800))
p2 = Player(1180, 0, RED, (20, 40), (0, 0, 1200, 800))

wall = Hitbox(400, 745, GREY, (400, 55))

platform1 = platform(0, 600, GREY, (100, 5), 2, 0, (300, 0))
platform2 = platform(1100, 600, GREY, (100, 5), 2, 0, (-300, 0))
platform3 = platform(140, 350, GREY, (60, 5), 0, -2, (0, -200))
platform4 = platform(1000, 350, GREY, (60, 5), 0, -2, (0, -200))

ledge1 = Hitbox(400, 475, GREY, (400, 15))
ledge2 = Hitbox(400, 400, GREY, (150, 10))
ledge3 = Hitbox(650, 400, GREY, (150, 10))



#hitbox setup
hit_boxes = [p1, p2, wall, platform1, platform2, platform3, platform4, ledge1, ledge2, ledge3]

#music
pygame.mixer.music.load("bit_rush.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0)
#msuic

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())

    #movement
    process_player_inputs(p2, p1)

    for hitbox in hit_boxes:
        hitbox.move(hit_boxes)
    #movement

    #DRAWING
    screen.fill(backgroundColor)

    for hitbox in reversed(hit_boxes):
        hitbox.draw(screen)

    p1score = font.render(str(p2.deaths), True, p1.color)
    p2score = font.render(str(p1.deaths), True, p2.color)

    screen.blit(p1score, (300, 30))
    screen.blit(p2score, (900, 30))
    #DRAWING

    #END CONIDITON
    if p1.deaths == 10:
        p2win = font.render("WINNER", True, p2.color)
        screen.blit(p2win, (550, 30))
        done = True

        #win effect
        pygame.mixer.music.load("victory.mp3")
        pygame.mixer.music.play(0, 0.0)

    elif p2.deaths == 10:
        p1win = font.render("WINNER", True, p1.color)
        screen.blit(p1win, (550, 30))
        done = True

        #win effect
        pygame.mixer.music.load("victory.mp3")
        pygame.mixer.music.play(0, 0.0)

    pygame.display.flip()
    clock.tick(120)

time.sleep(6)
pygame.quit() #GG