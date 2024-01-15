import pygame
from sys import exit
from gameobjects import *
import time

#init
pygame.init()
big_font = pygame.font.Font("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/alagard.ttf",40)
small_font = pygame.font.Font("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/alagard.ttf",20)
screen = pygame.display.set_mode((640,480))

player=Player()
level_1 = Level(player,0,192,"C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level1/tilemap_foreground.csv","C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level1/tilemap_background.csv")
level_2 = Level(player,600,0,"C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level2/tilemap_foreground.csv","C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level2/tilemap_background.csv")
level_3 = Level(player,0,180,"C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level3/tilemap_foreground.csv","C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level3/tilemap_background.csv")
level_4 = Level(player,0,180,"C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level4/tilemap_foreground.csv","C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/level4/tilemap_background.csv")
level_list = [level_1,level_2,level_3,level_4]
crnt_level = 0
level_list[crnt_level].reset_player(player)
level_complete=False

pygame.display.set_caption("game")
clock = pygame.time.Clock()

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space key pressed")
    if level_complete:
        screen.fill('Black')
        level_text = big_font.render("",False,'White')
        gameover_text = big_font.render("YOU HAVE ESCAPED!!",False,'White')
        screen.blit(gameover_text,((640-gameover_text.get_width())//2,180))    
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     crnt_level = 0
        #     level_complete=False
        #     level_list[crnt_level].reset_player(player)
        #     player.setalive()
    if player.isalive() and not(level_complete):
        level_list[crnt_level].draw(screen,player)
        level_text = big_font.render(f"LEVEL {crnt_level+1}",False,'White')
        screen.blit(level_text,(0,0))
        if level_list[crnt_level].trigger(player):
            level_text = big_font.render("press ENTER to continue",False,'White')
            screen.blit(level_text,((640-level_text.get_width())//2,400))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and crnt_level < 3:
                crnt_level += 1
                level_list[crnt_level].reset_player(player)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("?")
                level_complete=True
                player.kill()
    elif not(player.isalive()) and not(level_complete):
        screen.fill('Black')
        level_text = big_font.render("",False,'White')
        gameover_text = big_font.render("YOU HAVE PERISHED",False,'White')
        retry_text = small_font.render("PRESS ENTER TO RETRY",False,"White")
        screen.blit(gameover_text,((640-gameover_text.get_width())//2,180))    
        screen.blit(retry_text,((640-retry_text.get_width())//2,240))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            crnt_level = 0
            level_list[crnt_level].reset_player(player)
            player.setalive()
    pygame.display.update()
    clock.tick(60)

