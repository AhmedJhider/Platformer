import csv
import pygame

class Level():
    def __init__(self,player,x,y,foreground,background):
        self.foreground = Layer(foreground)
        self.background = Layer(background)
        self.player_x = x 
        self.player_y = y
    def reset_player(self,player):
        player.setxY(self.player_x,self.player_y)
    def draw(self,screen,player):
        self.background.draw(screen)
        self.foreground.draw(screen)
        player.update(screen,self.foreground)
    def trigger(self,player):
        for tile in self.foreground.trigger_list:
            if tile[1].colliderect(player.rect.x, player.rect.y, player.width,player.height):
                return True

class Layer():
    def __init__(self,file):
        self.tile_list=[]
        self.trigger_list=[]
        with open(file) as file:
            csvreader = csv.reader(file)
            row_count = 0
            for row in csvreader:
                col_count = 0
                for tile in row:
                    if tile != "-1":
                        tile_index = lambda tile:str(int(tile)+1) if len(tile)>1 else "0"+str(int(tile)+1)
                        img = pygame.image.load("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/desert-ruins/l0_tilemap"+ tile_index(tile) +".png")
                        img = pygame.transform.scale(img,(32,32))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * 32
                        img_rect.y = row_count * 32
                        sprite =(img,img_rect)
                        if tile in {"30","31","37","38"}:
                            self.trigger_list.append(sprite)
                        else:
                            self.tile_list.append(sprite)
                    col_count+=1
                row_count+=1
    def draw(self,screen):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
        for tile in self.trigger_list:
            screen.blit(tile[0],tile[1])

class Player():
    def __init__(self):
        sheet_right = pygame.transform.scale(pygame.image.load("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/player.png"),(32,64))
        sheet_upright = pygame.transform.scale(pygame.image.load("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/player_jump.png"),(32,64))
        sheet_left = pygame.transform.scale(pygame.image.load("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/player_left.png"),(32,64))
        sheet_upleft = pygame.transform.scale(pygame.image.load("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/player_jump_left.png"),(32,64))
        sheet_right_1 = pygame.transform.scale(pygame.image.load("C:/Users/jhide/Documents/_PROJECTS/pygame/platformer/assets/player.png"),(32,64))
        self.sheet = [sheet_left,sheet_right,sheet_upright,sheet_upleft]
        self.image = self.sheet[1]
        self.rect = self.image.get_rect()
        self.rect.x = -1
        self.rect.y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.alive = True
        self.direction = [0,0]
    def isalive(self):
        return self.alive
    def setalive(self):
        self.alive = True
    def kill(self):
        self.alive = False
    def setxY(self,x,y):
        self.rect.x = x
        self.rect.y = y
    def update(self,screen,foreground):
        dx = 0
        dy = 0

        #input handler
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
            self.direction[1] = 1
        if key[pygame.K_LEFT]:
            dx -= 3 
            self.direction[0] = 0
        if key[pygame.K_RIGHT]:
            dx += 3
            self.direction[0] = 1
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y    
        
        #collision handler
        for tile in foreground.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,self.height):
                if dx > 0:
                    dx = tile[1].x - self.rect.right
                elif dx < 0:
                    dx = tile[1].right - self.rect.x 
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,self.height):
                if self.vel_y < 0:
                    dy= tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.jumped = False
                    self.direction[1] = 0
                    self.vel_y = 0

        #animation handler
        if self.direction[1]==1:
            if self.direction[0]==1:
                self.image = self.sheet[2]
            else:
                self.image = self.sheet[3]
        else:
            if self.direction[0]==1:
                self.image = self.sheet[1]
            else:
                self.image = self.sheet[0]
        print(self.direction)
        #dump
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 520 and self.alive == True:
            self.kill()
        elif self.rect.top <= 0:
            self.rect.y = 0
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= 640:
            self.rect.right = 640
        
        screen.blit(self.image,self.rect)

