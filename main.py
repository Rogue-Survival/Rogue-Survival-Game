import pygame
import random
import math
import numpy

# initializes the pygame library
pygame.init()

# creates the window and dimensions for the game
screen = pygame.display.set_mode((800, 800))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
transparentSurface = pygame.Surface((800,800), pygame.SRCALPHA)
# sets the window caption at the top
pygame.display.set_caption("Rogue Survival")

# creates variable to control game fps
clock = pygame.time.Clock()
x = pygame.time.get_ticks()

mc_img = pygame.image.load("./images/MAIN_CHARACTER.png").convert_alpha()
enemy1 = pygame.image.load("./images/slime.png").convert_alpha()
xp = []
xp_hit = []

class Map(pygame.sprite.Sprite):
    def __init__(self, mapX=-600, mapY=-800):
        pygame.sprite.Sprite.__init__(self)
        self.mapX = mapX
        self.mapY = mapY
        self.cameraX = 0
        self.cameraY = 0

    def get_mapX(self):
        # returns the x coordinate of the map
        return self.mapX

    def get_mapY(self):
        # returns the y coordinate of the map
        return self.mapY


class Player(pygame.sprite.Sprite):
    # Player class controls basic functions relating to the player
    def __init__(self, speed=5, health=50):
        # inherits from the pygame.sprite.Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = "./images/MAIN_CHARACTER.png"
        self.health = health
        self.rect = mc_img.get_rect().scale_by(2,2)
        self.rect.x = 400
        self.rect.y = 400

    def get_speed(self):
        # returns speed of player
        return self.speed

    def get_image(self):
        # returns image of player
        return self.image

    def move_west(self):
        # moves the player West
        if self.rect.x > 25:
            m.cameraX -= self.speed
            n = len(enemies)
            count = 0
            westCount = 0
            northCount = 0
            southCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.x += self.speed
                enemy.northRect.x = enemy.rect.x + enemy.northXVal
                enemy.eastRect.x = enemy.rect.x + enemy.eastXVal
                enemy.southRect.x = enemy.rect.x + enemy.southXVal
                enemy.westRect.x = enemy.rect.x - enemy.westXVal
            for x in xp:
                x.x += self.speed
                x.xp_stationary()

    def move_east(self):
        # moves the player East
        if self.rect.x < 800:
            m.cameraX += self.speed
            n = len(enemies)
            count = 0
            eastCount = 0
            northCount = 0
            southCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.x -= self.speed
                enemy.northRect.x = enemy.rect.x + enemy.northXVal
                enemy.eastRect.x = enemy.rect.x + enemy.eastXVal
                enemy.southRect.x = enemy.rect.x + enemy.southXVal
                enemy.westRect.x = enemy.rect.x - enemy.westXVal
            for x in xp:
                x.x -= self.speed
                x.xp_stationary()

    def move_north(self):
        # moves the player North
        if self.rect.y > 25:
            m.cameraY -= self.speed
            n = len(enemies)
            count = 0
            northCount = 0
            eastCount = 0
            westCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y += self.speed
                enemy.northRect.y = enemy.rect.y - enemy.northYVal
                enemy.eastRect.y = enemy.rect.y + enemy.eastYVal
                enemy.southRect.y = enemy.rect.y + enemy.southYVal
                enemy.westRect.y = enemy.rect.y + enemy.westYVal
            for x in xp:
                x.y += self.speed
                x.xp_stationary()

    def move_south(self):
        # moves the player South
        if self.rect.y < 800:
            m.cameraY += self.speed
            n = len(enemies)
            count = 0
            southCount = 0
            eastCount = 0
            westCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y -= self.speed
                enemy.northRect.y = enemy.rect.y - enemy.northYVal
                enemy.eastRect.y = enemy.rect.y + enemy.eastYVal
                enemy.southRect.y = enemy.rect.y + enemy.southYVal
                enemy.westRect.y = enemy.rect.y + enemy.westYVal
            for x in xp:
                x.y -= self.speed
                x.xp_stationary()

class Bullet(pygame.sprite.Sprite):
    # Bullet class allows the player to shoot bullets at enemies
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.draw.circle(screen, (255,255,255), (p.rect.x+18,p.rect.y+17), 10)
        self.image = False
        self.startingPoint = pygame.math.Vector2(0,0)
        self.mousePOS = pygame.mouse.get_pos()
        self.bulletValid = False
        self.bulletSpeed = 50/3
        self.bulletIncrement = .5
        self.counterX = 0
        self.counterY = 0
        self.bulletDistance = 20
        self.angle = 200
        self.positionReached = False

    def bullet(self):
        # bullet movement
        # self.mousePOS = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        playerVector = pygame.math.Vector2(self.startingPoint[0], self.startingPoint[1])
        mouseVector = pygame.math.Vector2(self.mousePOS[0], self.mousePOS[1])
        # print(f'playerVector: ({self.startingPoint[0]}, {self.startingPoint[1]}), mouseVector: ({self.mousePOS[0]}, {self.mousePOS[1]})')
        # self.angle = playerVector.angle_to(mouseVector)
        if self.mousePOS[0] > self.startingPoint[0] and self.mousePOS[1] < self.startingPoint[1]:
            # first quadrant
            newTriangle = pygame.math.Vector2(self.mousePOS[0] - self.startingPoint[0], self.mousePOS[1] - self.startingPoint[1])
            # print(newTriangle)
            # print(f'{newTriangle[1]}/{newTriangle[0]}')
            self.angle = -(numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        elif self.mousePOS[0] > self.startingPoint[0] and self.mousePOS[1] > self.startingPoint[1]:
            # fourth quadrant
            newTriangle = pygame.math.Vector2(self.mousePOS[0] - self.startingPoint[0], self.mousePOS[1] - self.startingPoint[1])
            # print(newTriangle)
            # print(f'{newTriangle[1]}/{newTriangle[0]}')
            self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        elif self.mousePOS[0] < self.startingPoint[0] and self.mousePOS[1] < self.startingPoint[1]:
            # second quadrant
            newTriangle = pygame.math.Vector2(self.startingPoint[0] - self.mousePOS[0], self.startingPoint[1] - self.mousePOS[1])
            # print(newTriangle)
            # print(f'{newTriangle[1]}/{newTriangle[0]}')
            self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        elif self.mousePOS[0] < self.startingPoint[0] and self.mousePOS[1] > self.startingPoint[1]:
            # second quadrant
            newTriangle = pygame.math.Vector2(self.startingPoint[0] - self.mousePOS[0], self.startingPoint[1] - self.mousePOS[1])
            # print(newTriangle)
            # print(f'{newTriangle[1]}/{newTriangle[0]}')
            self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        # print(self.angle)
        if self.counterX > self.bulletDistance or self.counterY > self.bulletDistance: #or ((self.rect.x - self.mousePOS[0] < 5 or self.mousePOS[0] - self.rect.x > 5) and (self.rect.y - self.mousePOS[1] < 5 or self.mousePOS[1] - self.rect.y > 5)):
            self.rect.x = p.rect.x
            self.rect.y = p.rect.y
            self.bulletValid = False
            self.positionReached = False
            self.counterX = 0
            self.counterY = 0
            bulletsNum = len(enemies)
            bulletCounter = 0
            for bullet in bullets:
                if bullet.rect.x == bullets[bulletCounter].rect.x and bullet.rect.y == bullets[bulletCounter].rect.y:
                    bullets.remove(bullet)
                    # print("BULLET REMOVED!!!")
                bulletCounter += 1
        else:
            self.bulletValid = True
            # print("**********************************************************************")
            # print(f'rect.x = {self.rect.x}, rect.y = {self.rect.x}')
            # print(f'mousePOS.x = {self.mousePOS[0]}, mousePOS.y = {self.mousePOS[1]}')
            # print("**********************************************************************")


            if (self.rect.x > self.startingPoint[0] and self.rect.y > self.startingPoint[1]) and self.positionReached:
                # fourth quadrant - continues traveling after reaching mouse position
                self.rect.y += math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print('-------------------')
                # print("fourth quadrant - CONTINUING JOURNEY")
                # print('-------------------')
            elif (self.rect.x < self.startingPoint[0] and self.rect.y > self.startingPoint[1]) and self.positionReached:
                # third quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print('-------------------')
                # print("third quadrant - CONTINUING JOURNEY")
                # print('-------------------')
            elif (self.rect.x < self.startingPoint[0] and self.rect.y < self.startingPoint[1]) and self.positionReached:
                # second quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print('-------------------')
                # print("second quadrant - CONTINUING JOURNEY")
                # print('-------------------')
            elif (self.rect.x > self.startingPoint[0] and self.rect.y < self.startingPoint[1]) and self.positionReached:
                # first quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print('-------------------')
                # print("first quadrant - CONTINUING JOURNEY")
                # print('-------------------')
            elif self.rect.x < self.mousePOS[0] and self.rect.y < self.mousePOS[1]:
                # fourth quadrant - travels to mouse position
                self.rect.y += math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                if self.mousePOS[1] - self.rect.y < 10 and self.mousePOS[0] - self.rect.x < 10:
                    self.positionReached = True
                # print('-------------------')
                # print("fourth quadrant")
                # print('-------------------')
            elif self.rect.x > self.mousePOS[0] and self.rect.y < self.mousePOS[1]:
                # third quadrant - travels to mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                if self.mousePOS[1] - self.rect.y <= 10 and self.rect.x - self.mousePOS[0] <= 10:
                    self.positionReached = True
                # print('-------------------')
                # print("third quadrant")
                # print('-------------------')
            elif self.rect.x > self.mousePOS[0] and self.rect.y > self.mousePOS[1]:
                # second quadrant - travels to mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                if self.rect.y - self.mousePOS[1] <= 10 and self.mousePOS[0] - self.rect.x <= 10:
                    self.positionReached = True
                # print('-------------------')
                # print("second quadrant")
                # print('-------------------')
            elif self.rect.x < self.mousePOS[0] and self.rect.y > self.mousePOS[1]:
                # first quadrant - travels to mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                if self.rect.y - self.mousePOS[1] <= 10 and self.mousePOS[0] - self.rect.x <= 10:
                    self.positionReached = True
                # print('-------------------')
                # print("first quadrant")
                # print('-------------------')
            else:
                if self.mousePOS[1] > self.startingPoint[1] and (abs(self.mousePOS[0]) - abs(self.startingPoint[0])) < 15:
                    self.rect.y += math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                elif self.mousePOS[1] < self.startingPoint[1] and (abs(self.mousePOS[0]) - abs(self.startingPoint[0])) < 15:
                    self.rect.y -= math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                    self.rect.y -= math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1

class Enemy(pygame.sprite.Sprite):
    # Enemy class controls basic functions relating to the enemy
    def __init__(self, enemy_x=50, enemy_y= 50, width=0, height=0, image="./images/slime.png"):
        pygame.sprite.Sprite.__init__(self)
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
        self.width = width
        self.height = height
        self.speed = random.uniform(1.3, 2.5)
        self.image = image
        self.rect = enemy1.get_rect().scale_by(2, 2)
        self.rect.x = random.randint(0, 600)
        self.rect.y = random.randint(0, 1000)
        self.inRange = False
        self.northRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.northRect.midtop = self.rect.midtop
        self.eastRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.eastRect.midright = self.rect.midright
        self.southRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.southRect.midbottom = self.rect.midbottom
        self.westRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.westRect.midleft = self.rect.midleft
        self.northXVal = 12
        self.northYVal = -5
        self.eastXVal = 17
        self.eastYVal = 10
        self.southXVal = 12
        self.southYVal = 17
        self.westXVal = -5
        self.westYVal = 10
        self.circleRect = pygame.draw.circle(transparentSurface, (0, 50, 0), (self.rect.x, self.rect.y), 10)
        self.midDotRect = pygame.draw.circle(transparentSurface, (0, 50, 0, 100), (self.rect.x+16, self.rect.y + 16), 1)
        self.health = 50
        self.bulletCollisions = []

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
        pass

    def travel_north(self):
        # enemy moves North
        self.rect.y -= self.speed
        self.northRect.y = self.rect.y - self.northYVal
        self.eastRect.y = self.rect.y + self.eastYVal
        self.southRect.y = self.rect.y + self.southYVal
        self.westRect.y = self.rect.y + self.westYVal

    def travel_east(self):
        # enemy moves East
        self.rect.x += self.speed
        self.northRect.x = self.rect.x + self.northXVal
        self.eastRect.x = self.rect.x + self.eastXVal
        self.southRect.x = self.rect.x + self.southXVal
        self.westRect.x = self.rect.x - self.westXVal

    def travel_south(self):
        # enemy moves South
        self.rect.y += self.speed
        self.northRect.y = self.rect.y - self.northYVal
        self.eastRect.y = self.rect.y + self.eastYVal
        self.southRect.y = self.rect.y + self.southYVal
        self.westRect.y = self.rect.y + self.westYVal

    def travel_west(self):
        # enemy moves West
        self.rect.x -= self.speed
        self.northRect.x = self.rect.x + self.northXVal
        self.eastRect.x = self.rect.x + self.eastXVal
        self.southRect.x = self.rect.x + self.southXVal
        self.westRect.x = self.rect.x - self.westXVal

    def follow_mc(self):
        # follows the main character around the map
        if self.rect.x < p.rect.x:
            # enemy moves East
            n = len(enemies)
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            for i in range(n):
                # iterate through each enemy
                if self.eastRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    pass
                else:
                    if not self.eastRect.colliderect(enemies[i].circleRect):
                        # enemy moves East if unobstructed
                        moveEast += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(enemies[i].circleRect) and not self.eastRect.colliderect(enemies[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0, 3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    moveNorth += 1
                                else:
                                    # enemy moves South
                                    moveSouth += 1
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.northRect.colliderect(enemies[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(enemies[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.westRect.colliderect(enemies[i].circleRect):
                                    # enemy moves West as a last resort
                                    moveWest += 1
            if moveEast == (len(enemies) - 1):
                self.travel_east()
            elif moveNorth == (len(enemies) - 1):
                self.travel_north()
            elif moveSouth == (len(enemies) - 1):
                self.travel_south()
            elif moveWest == (len(enemies) - 1):
                self.travel_west()

        if self.rect.x > p.rect.x:
            # enemy moves West
            n = len(enemies)
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            for i in range(n):
                # iterate through each enemy
                if self.westRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    pass
                else:
                    if not self.westRect.colliderect(enemies[i].circleRect):
                        # enemy moves West if unobstructed
                        moveWest += 1
                    else:
                        if (self.rect.x - p.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(enemies[i].circleRect) and not self.eastRect.colliderect(enemies[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0, 3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    moveNorth += 1
                                else:
                                    # enemy moves South
                                    moveSouth += 1
                            else:
                                # if North and Sout are not both an option, check which direct is an option
                                if not self.northRect.colliderect(enemies[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(enemies[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.eastRect.colliderect(enemies[i].circleRect):
                                    # enemy moves East as a last resort
                                    moveEast += 1
            if moveWest == (len(enemies) - 1):
                self.travel_west()
            elif moveNorth == (len(enemies) - 1):
                self.travel_north()
            elif moveSouth == (len(enemies) - 1):
                self.travel_south()
            elif moveEast == (len(enemies) - 1):
                self.travel_east()

        if self.rect.y < p.rect.y:
            # enemy moves South
            n = len(enemies)
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            for i in range(n):
                # iterate through each enemy
                if self.southRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    pass
                else:
                    if not self.southRect.colliderect(enemies[i].circleRect):
                        # enemy moves South if unobstructed
                        moveSouth += 1
                    else:
                        if (p.rect.y - self.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(enemies[i].circleRect) and not self.westRect.colliderect(enemies[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0,3)
                                if randomDirection <= 1:
                                    # enemy moves East
                                    moveEast += 1
                                else:
                                    # enemy moves West
                                    moveWest += 1
                            else:
                                # if East and West are not both an option, check which direct is an option
                                if not self.eastRect.colliderect(enemies[i].circleRect):
                                    moveEast += 1
                                elif not self.westRect.colliderect(enemies[i].circleRect):
                                    moveWest += 1
                                elif not self.northRect.colliderect(enemies[i].circleRect):
                                    # enemy moves North as a last resort
                                    moveNorth += 1
            if moveSouth == (len(enemies) - 1):
                self.travel_south()
            elif moveEast == (len(enemies) - 1):
                self.travel_east()
            elif moveWest == (len(enemies) - 1):
                self.travel_west()
            elif moveNorth == (len(enemies) - 1):
                self.travel_north()

        if self.rect.y > p.rect.y:
            # enemy moves North
            n = len(enemies)
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            for i in range(n):
                # iterate through each enemy
                if self.northRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == enemies[i].rect.x and self.rect.y == enemies[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    pass
                else:
                    if not self.northRect.colliderect(enemies[i].circleRect):
                        # enemy moves North if unobstructed
                        moveNorth += 1
                    else:
                        if (self.rect.y - p.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(enemies[i].circleRect) and not self.westRect.colliderect(enemies[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0, 3)
                                if randomDirection <= 1:
                                    # enemy moves East
                                    moveEast += 1
                                else:
                                    # enemy moves West
                                    moveWest += 1
                            else:
                                # if East and West are not both an option, check which direct is an option
                                if not self.eastRect.colliderect(enemies[i].circleRect):
                                    # enemy moves east
                                    moveEast += 1
                                elif not self.westRect.colliderect(enemies[i].circleRect):
                                    # enemy moves west
                                    moveWest += 1
                                elif not self.southRect.colliderect(enemies[i].circleRect):
                                    # enemy moves South as a last resort
                                    moveSouth += 1
            if moveNorth == (len(enemies) - 1):
                self.travel_north()
            elif moveEast == (len(enemies) - 1):
                self.travel_east()
            elif moveWest == (len(enemies) - 1):
                self.travel_west()
            elif moveSouth == (len(enemies) - 1):
                self.travel_south()

    def attack_mc(self):
        pass


class XP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = pygame.draw.circle(screen, (0,255,0), (x, y), 5)
        self.hitBoxRect = pygame.draw.circle(transparentSurface, (0,255,35), (x, y), 50)



    def xp_stationary(self):
        self.rect = pygame.draw.circle(screen, (0,255,0), (self.x, self.y), 5)
        self.hitBoxRect = pygame.draw.circle(transparentSurface, (0,255,35), (self.x, self.y), 50)

class XP_Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xpBarBorderRect = None
        self.xpBarRect = None
        self.xpBarEmptyRect = None
        self.xp = 0
        self.level = 1
        self.total_length = 600
        self.level_xp_requirement = 10
        self.length = 0
        self.connector = None
        self.top = None
        self.right = None
        self.bottom = None
        self.left = None
        self.level_background = None
        self.level_font = pygame.font.SysFont('futura', 42)
        self.offset = 35
        self.leftover = 0
        self.leftoverSize = 0


    def show_xp_bar(self):
        self.xpBarBorderRect = pygame.draw.line(screen, (0,0,0), (90-self.offset,770), (710-self.offset, 770), 45)
        if self.xp:
            self.length = self.xp / self.level_xp_requirement
            if self.length >= 1 or self.length+self.leftover >= 1:
                self.leftover = self.xp - self.level_xp_requirement
                self.level += 1
                self.xp = 0
                self.level_xp_requirement *= 1.25
                self.length = self.xp / self.level_xp_requirement
                if self.leftover:
                    self.leftoverSize = (((1 / self.level_xp_requirement)*self.total_length)*self.leftover)
                    self.xpBarRect = pygame.draw.line(screen, (28,36,192), (100-self.offset,770), (self.leftoverSize+100-self.offset, 770), 25)
                    print(self.leftover)
                    self.leftover = 0
            else:
                self.xpBarRect = pygame.draw.line(screen, (28,36,192), (100-self.offset,770), ((self.total_length*self.length)+self.leftoverSize+100-self.offset, 770), 25)
                # self.xpBarEmptyRect = pygame.draw.line(screen, (255,255,255), ((self.total_length*self.length)+100-self.offset,770), (700-self.offset, 770), 25)
        else:
            self.xpBarRect = pygame.draw.line(screen, (28,36,192), (100-self.offset,770), (self.leftoverSize+100-self.offset, 770), 25)
            # self.xpBarEmptyRect = pygame.draw.line(screen, (255,255,255), (100-self.offset,770), (700-self.offset, 770), 25)
        self.connector = pygame.draw.line(screen, (0,0,0), (710-self.offset,770), (740-self.offset, 770), 5)
        self.left = pygame.draw.line(screen, (0,0,0), (740-self.offset,790), (740-self.offset, 750), 6)
        self.top = pygame.draw.line(screen, (0,0,0), (738-self.offset,750), (785-self.offset, 750), 6)
        self.bottom = pygame.draw.line(screen, (0,0,0), (738-self.offset,790), (785-self.offset, 790), 6)
        self.right = pygame.draw.line(screen, (0,0,0), (785-self.offset,793), (785-self.offset, 748), 6)
        self.level_background = pygame.draw.line(screen, (255,255,255), (744-self.offset,770), (782-self.offset, 770), 33)
        levelRender = self.level_font.render(str(self.level), True, (0, 0, 0))
        if self.level < 10:
            screen.blit(levelRender, (756-self.offset, 758))
        else:
            screen.blit(levelRender, (747-self.offset, 758))


# initializes the Player and Enemy classes
p = Player()
m = Map()
b = Bullet()
xpB = XP_Bar()
enemies = [Enemy(500, 100, 80, 40) for _ in range(25)]
bullets = [Bullet() for _ in range(1)]

# adds ability for text to be on screen
def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

# adding the ability to implement buttons
def button(msg,x,y,w,h,ic,ac, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h), border_radius=20)
        if click[0] == 1 and action != None:
            if action == "Settings":
                settingsMenu()
            elif action == "Fullscreen Toggle":
                 fullscreenToggle()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h), border_radius=20)

    smallText = pygame.font.SysFont("monospace", 20, bold=True)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)


# loads images
bg_img = pygame.image.load('./images/island.png').convert_alpha()
speedI = pygame.image.load("./images/Noodle.png").convert_alpha()


speed_item_visible = True
game = True
gameTimerOn = False


timerFont = pygame.font.SysFont('futura', 64)
fpsFont = pygame.font.SysFont('futura', 28)

gameTimeStr = 0
minutes = 0
seconds = 0


def start_game_time():
    gameTime = pygame.time.get_ticks()
    global gameTimeStr
    gameTimeStr = int(gameTime/1000)
    if gameTimeStr < 60:
        gameTimeStr = str(int(gameTime/1000))
        global seconds
        seconds = int(gameTimeStr) % 60
    elif gameTimeStr >= 60:
        global minutes
        # global seconds
        minutes = gameTimeStr / 60
        seconds = gameTimeStr % 60
        if minutes < 10 and seconds < 10:
            gameTimeStr = f'0{int(minutes)}:0{int(seconds)}'
        elif minutes < 10 and seconds >= 10:
            gameTimeStr = f'0{int(minutes)}:{int(seconds)}'
        elif minutes > 10 and seconds < 10:
            gameTimeStr = f'{int(minutes)}:0{int(seconds)}'
        elif minutes > 10 and seconds > 10:
            gameTimeStr = f'{int(minutes)}:{int(seconds)}'
    if minutes < 1 and seconds < 10:
        gameTimeStr = f'00:0{int(seconds)}'
    elif minutes < 1 and seconds >= 10:
        gameTimeStr = f'00:{int(seconds)}'


def display_timer(text, font, textColor):
    gameTimer = font.render(text, True, textColor).convert_alpha()
    screen.blit(gameTimer, (675, 15))
    # timerRect = gameTimer.get_rect()
    # screen.blit(gameTimer, (675, 15), timerRect)


def display_fps(text, font, textColor):
    text = str(int(text))
    # print(text)
    fpsDisplay = font.render(text, True, textColor).convert_alpha()
    # print(fpsDisplay)
    screen.blit(fpsDisplay, (0, 0))

# adds the ability to fullscreen the game
def fullscreenToggle():
    # info = pygame.display.Info()  # get the size of the current screen
    # screen_width, screen_height = info.current_w, info.current_h
    # window_width, window_height = screen_width - 10, screen_height - 50
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.update()


def pauseGame():
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    pause = True

    while pause:
        if pygame.key.get_pressed()[pygame.K_1]:
            pause = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        screen.fill((255, 255, 255))
        # surf = transparentSurface
        # screen.blit(surf, (0, 0))

        largeText = pygame.font.SysFont('monospace', 115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((400), (200))
        button("Settings", ((screen_width/8)*3), ((screen_height/4)*3), (screen_width/4), (screen_height/8), (202, 186, 227), (227, 186, 186), "Settings")
        screen.blit(TextSurf, TextRect)

        # key_presses = pygame.key.get_pressed()
        pygame.display.update()
        clock.tick(15)

def settingsMenu():
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    pause = True

    while pause:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        screen.fill((255, 255, 255))
        largeText = pygame.font.SysFont('monospace', 115)
        TextSurf, TextRect = text_objects("Settings", largeText)
        TextRect.center = ((400), (200))
        button("Fullscreen", ((screen_width/8)*3), ((screen_height/4)*2), (screen_width/4), (screen_height/8), (202, 186, 227), (227, 186, 186), "Fullscreen Toggle")
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)

# unpausing func for the buttons
def unPause():
    pause = False

# def to store all the keypress functions
def keypressed():
    key_presses = pygame.key.get_pressed()
    # stores the keys that are pressed

    if key_presses[pygame.K_a]:
        # if 'a' is pressed, move left
        p.move_west()
    elif key_presses[pygame.K_LEFT]:
        # if left arrow is pressed, move left
        p.move_west()
        # p.rect.x -= 45

    if key_presses[pygame.K_d]:
        # if 'd' is pressed, move right
        p.move_east()

    elif key_presses[pygame.K_RIGHT]:
        # if right arrow is pressed, move right
        p.move_east()
        # p.rect.x += 45

    if key_presses[pygame.K_w]:
        # if 'w' is pressed, move up
        p.move_north()
    elif key_presses[pygame.K_UP]:
        # if up arrow is pressed, move up
        p.move_north()
        # p.rect.y -= 45

    if key_presses[pygame.K_s]:
        # if 's' is pressed, move down
        p.move_south()
    elif key_presses[pygame.K_DOWN]:
        # if down arrow is pressed, move down
        p.move_south()
        # p.rect.y += 45

    # if key_presses[pygame.K_q]:
    #     # if 'q' is pressed, fire bullet
    #     mousePOS = pygame.mouse.get_pos()
    #     b.mousePOS = (pygame.math.Vector2(mousePOS[0], mousePOS[1]))
    #     b.startingPoint = pygame.math.Vector2(p.rect.x, p.rect.y)
    #     b.bullet()

    if key_presses[pygame.K_ESCAPE]:
        # if ESC key is pressed, pause game
        pauseGame()

activateBullet = True
bulletTimer1 = 2
bulletTimer2 = 0

while game:
    # the core game loop
    start_game_time()


    fps = clock.get_fps()

    clock.tick(60)
    # sets the fps to 60

    # pygame.time.delay(5)
    # adds a very small delay to make it feel more like a game

    # Introducing a pause function for the buttons and game pause functionality
    pause = False
    # making sure the X button still closes the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the x in the top right corner of game is clicked, the program will close.
            game = False

    # cycling through the possible key presses
    keypressed()

    # makes the map visible
    screen.blit(pygame.transform.scale(bg_img, (2250, 2250)), (-800 - m.cameraX, -800 - m.cameraY))

    # makes the main character visible
    screen.blit(pygame.transform.scale(mc_img, (35, 30)), (p.rect.x, p.rect.y))

    bulletTimer2 = (pygame.time.get_ticks() / 1000)
    # if bulletTimer1
    if seconds % b.bulletIncrement == 0:
        activateBullet = True
    if bulletTimer2 > bulletTimer1:
        # controls the speed of shooting the bullets
        bullets.append(Bullet())
        for bullet in bullets:
            bullet.mousePOS = pygame.mouse.get_pos()
            bullet.mousePOS = (pygame.math.Vector2(bullet.mousePOS[0], bullet.mousePOS[1]))
            bullet.startingPoint = pygame.math.Vector2(p.rect.x, p.rect.y)
            bullet.bullet()
        bulletTimer1 += b.bulletIncrement
        activateBullet = False
        # print(activateBullet)
    for bullet in bullets:
        if bullet.bulletValid:
            # if bullet ability has been activated
            pygame.draw.circle(screen, (255, 255, 255), (bullet.rect.x+18, bullet.rect.y+17), 10)
            bullet.bullet()

    for enemy in enemies:
        # for every enemy
        screen.blit(pygame.transform.scale(enemy1, (35, 30)), (enemy.rect.x, enemy.rect.y))
        enemy.generate_enemy()
        enemy.follow_mc()
        # pygame.draw.rect(screen, (255,0,0), enemy.rect)
        # pygame.draw.rect(screen, (128,0,128), enemy.northRect)
        # pygame.draw.rect(screen, (128,0,128), enemy.eastRect)
        # pygame.draw.rect(screen, (128,0,128), enemy.southRect)
        # pygame.draw.rect(screen, (128,0,128), enemy.westRect)
        enemy.circleRect = pygame.draw.circle(transparentSurface, (0, 50, 0, 100), (enemy.rect.x+18, enemy.rect.y + 17), 10)
        enemy.midDotRect = pygame.draw.circle(transparentSurface, (0, 50, 0, 100), (enemy.rect.x + 16, enemy.rect.y + 16), 1)
        for bullet in bullets:
            if enemy.rect.colliderect(bullet.rect):
                if not enemy.bulletCollisions:
                    # if the enemy has encountered it's first bullet, add to the list and take damage
                    enemy.bulletCollisions.append(bullet)
                    enemy.health -= 100
                elif enemy.bulletCollisions:
                    # if the list of bullets the enemy has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                    i = 0
                    for l in enemy.bulletCollisions:
                        if bullet.rect.x == enemy.bulletCollisions[i].rect.x and bullet.rect.y == enemy.bulletCollisions[i].rect.y:
                            pass
                        elif bullet not in enemy.bulletCollisions:
                            enemy.bulletCollisions.append(bullet)
                            enemy.health -= 100
                        i += 1

                if enemy.health <= 0:
                    # despawns the enemy if their health is 0 or below
                    xp.append(XP(enemy.rect.x+18, enemy.rect.y+17))
                    enemies.remove(enemy)

                    # self.rect = pygame.draw.circle(screen, (255,255,255), (p.rect.x+18,p.rect.y+17), 10)
                    break
        if enemy.rect.colliderect(p.rect) or enemy.northRect.colliderect(p.rect) or enemy.eastRect.colliderect(p.rect) or enemy.southRect.colliderect(p.rect) or enemy.westRect.colliderect(p.rect):
            # print("COLLIDE!!!")
            p.health -= 1

    for x in xp:
        x.xp_stationary()
        if x.hitBoxRect.colliderect(p.rect):
            xp_hit.append(x)
            x.xp_stationary()

    for x in xp_hit:
        if abs(x.rect.x - p.rect.x) < 25 and abs(x.rect.y - p.rect.y) < 25:
            # print(f'({x.x,x.y}), ({p.rect.x,p.rect.y})')
            if x in xp:
                xp.remove(x)
                xpB.xp += 1
            if x in xp_hit:
                xp_hit.remove(x)
        else:
            if x.rect.x+18 < p.rect.x:
                x.x += p.speed
            if x.rect.x+18 > p.rect.x:
                x.x -= p.speed
            if x.rect.y+18 < p.rect.y:
                x.y += p.speed
            if x.rect.y+18 > p.rect.y:
                x.y -= p.speed


    for bullet in bullets:
        # check if any of the bullets are actually still colliding with enemies, if not, remove the bullet from the enemies' collision list
        counter = 0
        enemiesHit = []
        enemiesNotHit = []
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                counter += 1
                enemiesHit.append(enemy)
            else:
                enemiesNotHit.append(enemy)
        if not counter:
            for l in enemiesNotHit:
                if bullet in l.bulletCollisions:
                    l.bulletCollisions.remove(bullet)


    if len(enemies) < 15:
        enemies.append(Enemy())

    display_timer(gameTimeStr, timerFont, (0, 0, 0))
    display_fps(fps, fpsFont, (0,255,0))
    xpB.show_xp_bar()
    index = 0
    numOfEnemies = len(enemies)
    pygame.display.flip()
    # print(p.health)
    pygame.display.update()

pygame.quit()


"""

The reason why the enemy physics goes insane after 2 spawned enemies is because we are iterating
through each enemy and adjusting movements per each enemy.

Possible fix: Iterate through each enemy like we have been, however, instead of actually moving
the enemy for each iteration, just have specific variables such as northOpen or northClosed. After
iterating through each enemy and ascertaining the available directions, whatever direction variables
are true, then execute the movement code.




The reason why the enemies can stack on top of one another instead of going around the enemy to the
player is because of the > than 50 line of code. If changed to > 25, then the direction of the
enemy will be randomly picked, however, the direction is continually randomly picked, due to this,
if the options were either east or west and it picked east, it would go east for that one loop,
however, immediately after it could also pick west, so it keeps going back and forth looking like it
is shaking. Ideally, have it pick one random direction, then have that direction saved for a couple
seconds so that it will keep going in that direction. As a "band-aid" solution, we could just have
enemy default to one of the two directions if both are available.

Perhaps, if Player has no enemies on specific side, tell enemies to go in that direction to better
surround the Player.



"""
