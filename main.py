import pygame
import random

# initializes the pygame library
pygame.init()

# creates the window and dimensions for the game
screen = pygame.display.set_mode((800, 800))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# sets the window caption at the top
pygame.display.set_caption("Rogue Survival")

# creates variable to control game fps
clock = pygame.time.Clock()
x = pygame.time.get_ticks()


mc_img = pygame.image.load("./images/MAIN_CHARACTER.png").convert_alpha()
enemy1 = pygame.image.load("./images/slime.png").convert_alpha()

mapX = -675
mapY = -800

class Map(pygame.sprite.Sprite):
    def __init__(self, mapX=-600, mapY=-800):
        pygame.sprite.Sprite.__init__(self)
        self.mapX = mapX
        self.mapY = mapY

    def get_mapX(self):
        # returns the x coordinate of the map
        return self.mapX

    def get_mapY(self):
        # returns the y coordinate of the map
        return self.mapY





class Player(pygame.sprite.Sprite):
    # Player class controls basic functions relating to the player
    def __init__(self, mc_x=350, mc_y=580, width=0, height=0, speed=5, image="./images/MAIN_CHARACTER.png", health=50):
        # inherits from the pygame.sprite.Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.mc_x = mc_x
        self.mc_y = mc_y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = image
        self.health = health
        self.rect = mc_img.get_rect()
        self.rect.x = 500
        self.rect.y = 600

    def render(self):
        pass

    def get_mc_x(self):
        # returns x position of player
        return self.mc_x

    def get_mc_y(self):
        # returns y position of player
        return self.mc_y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_speed(self):
        # returns speed of player
        return self.speed

    def get_image(self):
        # returns image of player
        return self.image

    def move_left(self):
        # moves the player left
        # if not self.mc_x < 370:
        self.rect.x -= self.speed

    def move_right(self):
        # moves the player right
        # if not self.mc_x > 1120:
        self.rect.x += self.speed

    def move_up(self):
        # moves the player up
        # if not self.mc_y < 550:
        self.rect.y -= self.speed

    def move_down(self):
        # moves the player down
        # if not self.mc_y > 1350:
        self.rect.y += self.speed


class Enemy(pygame.sprite.Sprite):
    # Enemy class controls basic functions relating to the enemy
    def __init__(self, enemy_x=50, enemy_y= 50, width=0, height=0, speed=2.5, image="./images/slime.png"):
        pygame.sprite.Sprite.__init__(self)
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = image
        self.rect = enemy1.get_rect()
        self.rect.x = random.randint(0, 600)
        self.rect.y = random.randint(0, 1000)
        self.inRange = False
        self.startTimer = 0
        self.northRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.northRect.midbottom = self.rect.midbottom
        self.eastRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.eastRect.midbottom = self.rect.midbottom
        self.southRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.southRect.midbottom = self.rect.midbottom
        self.westRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.westRect.midbottom = self.rect.midbottom


    def render(self):
        pass

    def get_enemy_x(self):
        # returns x position of player
        return self.enemy_x

    def get_enemy_y(self):
        # returns y position of player
        return self.enemy_y

    def get_width(self):
        # returns the width of the enemy
        return self.width

    def get_height(self):
        # returns the height of the enemy
        return self.height

    def get_speed(self):
        # returns speed of player
        return self.speed

    def get_image(self):
        # returns image of player
        return self.image

    def generate_enemy(self):
        # screen.blit(pygame.transform.scale(enemy1, (60, 60)), (self.enemy_x, self.enemy_y))
        # screen.blit(enemy1, (self.rect.x, self.rect.y))
        pass

    def follow_mc(self):
        # follows the main character around the map
        if self.rect.x < p.rect.x:
            n = len(enemies)
            self.rect.x += self.speed
            self.northRect.x = self.rect.x + 3
            self.eastRect.x = self.rect.x + 8
            self.southRect.x = self.rect.x + 3
            self.westRect.x = self.rect.x - 3
            for i in range(n):
                if self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    pass
                else:
                    if self.northRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.eastRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.southRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.westRect.colliderect(enemies[i].rect):
                        print("WORKING")


        if self.rect.x > p.rect.x:
            n = len(enemies)
            self.rect.x -= self.speed
            self.northRect.x = self.rect.x + 3
            self.eastRect.x = self.rect.x + 8
            self.southRect.x = self.rect.x + 3
            self.westRect.x = self.rect.x - 3
            for i in range(n):
                if self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    pass
                else:
                    if self.northRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.eastRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.southRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.westRect.colliderect(enemies[i].rect):
                        print("WORKING")


            # for enemy in enemies:
            #     if self.rect.colliderect(enemies[n]):
            #         self.rect.x+= self.speed
        if self.rect.y < p.rect.y:
            n = len(enemies)
            self.rect.y += self.speed
            self.northRect.y = self.rect.y - 3
            self.eastRect.y = self.rect.y + 3
            self.southRect.y = self.rect.y + 10
            self.westRect.y = self.rect.y + 3
            for i in range(n):
                if self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    pass
                else:
                    if self.northRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.eastRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.southRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.westRect.colliderect(enemies[i].rect):
                        print("WORKING")


            # for enemy in enemies:
            #     if self.rect.colliderect(enemies[n]):
            #         self.rect.y-= self.speed
        if self.rect.y > p.rect.y:
            n = len(enemies)
            self.rect.y -= self.speed
            self.northRect.y = self.rect.y - 3
            self.eastRect.y = self.rect.y + 3
            self.southRect.y = self.rect.y + 10
            self.westRect.y = self.rect.y + 3
            for i in range(n):
                if self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    pass
                else:
                    if self.northRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.eastRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.southRect.colliderect(enemies[i].rect):
                        print("WORKING")
                    if self.westRect.colliderect(enemies[i].rect):
                        print("WORKING")


            # for enemy in enemies:
            #     if self.rect.colliderect(enemies[n]):
            #         self.rect.y+= self.speed

    def attack_mc(self):
        if self.rect.colliderect(p.rect):
            if self.inRange == False:
                self.startTimer=pygame.time.get_ticks()
            self.inRange = True
            if self.startTimer > 3000:
                # print("TESTING)
                pass
            print(self.startTimer)



# while mainloop: # mainloop
#



# initializes the Player and Enemy classes
p = Player()
m = Map()
enemies = [Enemy(500,100,80,40) for _ in range(2)]
enemies2 = enemies.copy()



# loads images
bg_img = pygame.image.load('./images/island.png').convert_alpha()
speedI = pygame.image.load("./images/Noodle.png").convert_alpha()


speed_item_visible = True
game = True

while game:
    fps= clock.get_fps()
    # print(fps)

    # the core game loop
    clock.tick(60)
    # sets the fps to 60
    pygame.time.delay(5)
    # adds a very small delay to make it feel more like a game




    key_presses = pygame.key.get_pressed()
    # stores the keys that are pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the x in the top right corner of game is clicked, the program will close.
            game = False

    if key_presses[pygame.K_a]:
        # if 'a' is pressed, move left
        p.move_left()
    elif key_presses[pygame.K_LEFT]:
        # if left arrow is pressed, move left
        p.move_left()

    if key_presses[pygame.K_d]:
        # if 'd' is pressed, move right
        p.move_right()

    elif key_presses[pygame.K_RIGHT]:
        # if right arrow is pressed, move right
        p.move_right()

    if key_presses[pygame.K_w]:
        # if 'w' is pressed, move up
        p.move_up()
    elif key_presses[pygame.K_UP]:
        # if up arrow is pressed, move up
        p.move_up()

    if key_presses[pygame.K_s]:
        # if 's' is pressed, move down
        p.move_down()
    elif key_presses[pygame.K_DOWN]:
        # if down arrow is pressed, move down
        p.move_down()

    # makes the map visible
    screen.blit(pygame.transform.scale(bg_img, (2250, 2250)), (mapX, mapY))

    # makes the main character visible
    # the first tuple dictates the size (45,45)
    # the second tuple dictates the starting coordinates (p.mc_x, p.mc_y)
    # the coordinates start at the top left of the screen, which is (0,0) instead of the center
    # screen.blit(pygame.transform.scale(mc_img, (45, 45)), (p.mc_x,p.mc_y))
    screen.blit(mc_img,p.rect)

    if speed_item_visible:
        # shows a visible object on the map if it has not been taken yet
        screen.blit(pygame.transform.scale(speedI, (30, 30)), (400, 285))

    if (380 <= p.rect.x <= 420) and (265 <= p.rect.y <= 305):
        # if the player is in the vacinity of the item, give the player the powerup from the item
        # and no longer show the powerup
        if speed_item_visible:
            p.speed += 10
            speed_item_visible = False

    for enemy in enemies:
        screen.blit(enemy1, (enemy.rect.x, enemy.rect.y))
        enemy.generate_enemy()

        enemy.follow_mc()
        pygame.draw.rect(screen, (255,0,0), enemy.rect)
        pygame.draw.rect(screen, (128,0,128), enemy.northRect)
        pygame.draw.rect(screen, (128,0,128), enemy.eastRect)
        pygame.draw.rect(screen, (128,0,128), enemy.southRect)
        pygame.draw.rect(screen, (128,0,128), enemy.westRect)
        if enemy.rect.colliderect(p.rect):
            print("COLLISION DETECTED!!!")
            p.health -= 1
    index = 0
    numOfEnemies = len(enemies)
    # for enemy in enemies:
    #     for index in enemies:
    #         if enemy.rect.colliderect(enemies[0].rect):
    #             pass
    #
    #
    #     # index +=1
    #
    #
    #     if enemy.rect.colliderect(enemies[2]):
    #         pass
    #     else:
    #         enemy.follow_mc()


    # lol = (p.rect.y)
    # p.rect.y += 5




    pygame.draw.rect(screen, (0,255,0), p.rect)

    print(p.health)
    pygame.display.update()

pygame.quit()








# when enemy reaches player collision, initiate attack animation/wind up attack, if player still in collision (plus add offset due to weapon they might have) then the player will take damage.




















"""

0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0
0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0
0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0
0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0
0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0

"""
"""
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

"""
