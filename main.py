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
        self.bulletRect = pygame.draw.circle(screen, (255,255,255), (self.rect.x+18,self.rect.y+17), 10)
        self.startingPoint = pygame.math.Vector2(0,0)
        self.mousePOS = pygame.mouse.get_pos()
        self.bulletValid = False
        self.bulletSpeed = 50/3
        self.counterX = 0
        self.counterY = 0
        self.bulletDistance = 20
        self.angle = 200

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

            # pygame.display.update()
            # pygame.display.flip()
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

        # pygame.display.update()
        # pygame.display.flip()

    def move_east(self):
        # moves the player East
        if self.rect.x < 800:

            m.cameraX += self.speed

            # pygame.display.update()
            # pygame.display.flip()
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
        # pygame.display.update()
        # pygame.display.flip()

    def move_north(self):
        # moves the player North
        if self.rect.y > 25:

            m.cameraY -= self.speed

            # pygame.display.update()
            # pygame.display.flip()
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
        # pygame.display.update()
        # pygame.display.flip()

    def move_south(self):
        # moves the player South
        if self.rect.y < 800:

            m.cameraY += self.speed

            # pygame.display.update()
            # pygame.display.flip()
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
        # pygame.display.update()
        # pygame.display.flip()

    def bullet(self):
        # bullet movement
        self.mousePOS = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        playerVector = pygame.math.Vector2(self.startingPoint[0], self.startingPoint[1])
        mouseVector = pygame.math.Vector2(self.mousePOS[0], self.mousePOS[1])
        print(f'playerVector: ({self.startingPoint[0]}, {self.startingPoint[1]}), mouseVector: ({self.mousePOS[0]}, {self.mousePOS[1]})')
        # self.angle = playerVector.angle_to(mouseVector)
        if self.mousePOS[0] > self.startingPoint[0] and self.mousePOS[1] < self.startingPoint[1]:
            # first quadrant
            newTriangle = pygame.math.Vector2(self.mousePOS[0] - self.startingPoint[0], self.mousePOS[1] - self.startingPoint[1])
            print(newTriangle)
            print(f'{newTriangle[1]}/{newTriangle[0]}')
            self.angle = -(numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        elif self.mousePOS[0] > self.startingPoint[0] and self.mousePOS[1] > self.startingPoint[1]:
            # fourth quadrant
            newTriangle = pygame.math.Vector2(self.mousePOS[0] - self.startingPoint[0], self.mousePOS[1] - self.startingPoint[1])
            print(newTriangle)
            print(f'{newTriangle[1]}/{newTriangle[0]}')
            print('=============================================================')
            self.angle = -(numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        elif self.mousePOS[0] < self.startingPoint[0] and self.mousePOS[1] < self.startingPoint[1]:
            # second quadrant
            newTriangle = pygame.math.Vector2(self.startingPoint[0] - self.mousePOS[0], self.startingPoint[1] - self.mousePOS[1])
            print(newTriangle)
            print(f'{newTriangle[1]}/{newTriangle[0]}')
            self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        elif self.mousePOS[0] < self.startingPoint[0] and self.mousePOS[1] > self.startingPoint[1]:
            # second quadrant
            newTriangle = pygame.math.Vector2(self.startingPoint[0] - self.mousePOS[0], self.startingPoint[1] - self.mousePOS[1])
            print(newTriangle)
            print(f'{newTriangle[1]}/{newTriangle[0]}')
            self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
        print(self.angle)
        if (self.counterX > self.bulletDistance or self.counterY > self.bulletDistance) or ((self.bulletRect.x - self.mousePOS[0] < 5 or self.mousePOS[0] - self.bulletRect.x > 5) and (self.bulletRect.y - self.mousePOS[1] < 5 or self.mousePOS[1] - self.bulletRect.y > 5)):
            self.bulletRect.x = self.rect.x
            self.bulletRect.y = self.rect.y
            self.bulletValid = False
            self.counterX = 0
            self.counterY = 0
        # elif self.counterX > self.bulletDistance or self.counterY > self.bulletDistance:
        #     self.bulletRect.x = self.rect.x
        #     self.bulletRect.y = self.rect.y
        #     self.bulletValid = False
        #     self.counterX = 0
        #     self.counterY = 0
        else:
            self.bulletValid = True
        # if self.bulletRect.x == self.mousePOS[0]:
        #     pass
        # else:
        #     # if (self.bulletRect.x < self.mousePOS[0] and self.bulletRect.y < self.mousePOS[1]):
        #     #     # fourth quadrant
        #     #     self.bulletRect.y += math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
        #     #     self.bulletRect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
        #     #     self.counterY += 1
        #         # fourth quadrant
        #         self.bulletRect.y += math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
        #         self.counterY += 1
        #         print('HEHEHE')
        #     if self.bulletRect.x < self.mousePOS[0]:
        #         # first and fourth quadrant
        #         self.bulletRect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
        #         self.counterX += 1
        #     elif self.bulletRect.x > self.mousePOS[0]:
        #         # second and third quadrant
        #         self.bulletRect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
        #         self.counterX += 1
        # if self.bulletRect.y == self.mousePOS[1]:
        #     pass
        # else:
        #     if self.bulletRect.y < self.mousePOS[1]:
        #         # third and fourth quadrant
        #         self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
        #         self.counterY += 1
        #     elif self.bulletRect.y > self.mousePOS[1]:
        #         # first and second quadrant
        #         self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
        #         self.counterY += 1

        if self.bulletRect.x < self.mousePOS[0] and self.bulletRect.y < self.mousePOS[1]:
            # fourth quadrant
            self.bulletRect.y += math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
            self.bulletRect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
            self.counterX += 1
            self.counterY += 1
        if self.bulletRect.x > self.mousePOS[0] and self.bulletRect.y < self.mousePOS[1]:
            # third quadrant
            self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
            self.bulletRect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
            self.counterX += 1
            self.counterY += 1
        if self.bulletRect.x > self.mousePOS[0] and self.bulletRect.y > self.mousePOS[1]:
            # second quadrant
            self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
            self.bulletRect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
            self.counterX += 1
            self.counterY += 1
        if self.bulletRect.x < self.mousePOS[0] and self.bulletRect.y > self.mousePOS[1]:
            # first quadrant
            self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
            self.bulletRect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
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
        self.midDotRect = pygame.draw.circle(screen, (0, 50, 0, 100), (self.rect.x+16, self.rect.y + 16), 1)
        self.health = 50

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


# initializes the Player and Enemy classes
p = Player()
m = Map()
enemies = [Enemy(500, 100, 80, 40) for _ in range(25)]

# loads images
bg_img = pygame.image.load('./images/island.png').convert_alpha()
speedI = pygame.image.load("./images/Noodle.png").convert_alpha()

speed_item_visible = True
game = True
n = 0
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
    # screen.blit(gameTimer, (675,15))
    timerRect = gameTimer.get_rect()
    screen.blit(gameTimer, (675, 15), timerRect)


def display_fps(text, font, textColor):
    text = str(int(text))
    fpsDisplay = font.render(text, True, textColor).convert_alpha()
    screen.blit(fpsDisplay, (0,0))


while game:
    # the core game loop
    start_game_time()
    display_timer(gameTimeStr, timerFont, (0, 0, 0))
    pygame.display.update()

    fps = clock.get_fps()
    clock.tick(60)
    display_fps(fps, fpsFont, (0, 255, 0))
    pygame.display.update()
    # print(fps)
    # sets the fps to 60
    pygame.time.delay(5)
    # adds a very small delay to make it feel more like a game

    key_presses = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the x in the top right corner of game is clicked, the program will close.
            game = False

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

    n += 1
    if key_presses[pygame.K_q]:
        # if 'q' is pressed, fire bullet
        p.mousePOS = pygame.mouse.get_pos()
        p.startingPoint = pygame.math.Vector2(p.rect.x, p.rect.y)
        p.bullet()

    # makes the map visible
    # the first tuple dictates the size (2250, 2250)
    # the second tuple dictates the starting coordinates (m.mapX, m.mapY)
    # the coordinates start at the top left of the game, which is (0,0) instead of the center
    screen.blit(pygame.transform.scale(bg_img, (2250, 2250)), (-800 - m.cameraX, -800 - m.cameraY))

    # makes the main character visible

    # screen.blit(pygame.transform.scale(mc_img, (45, 45)), (p.mc_x,p.mc_y))
    # screen.blit(mc_img,p.rect)

    screen.blit(pygame.transform.scale(mc_img, (35, 30)), (p.rect.x, p.rect.y))
    """
    # speed item
    if speed_item_visible:
        # shows a visible object on the map if it has not been taken yet
        screen.blit(pygame.transform.scale(speedI, (30, 30)), (400, 285))

    if (380 <= p.rect.x <= 420) and (265 <= p.rect.y <= 305):
        # if the player is in the vacinity of the item, give the player the powerup from the item
        # and no longer show the powerup
        if speed_item_visible:
            p.speed += 10
            speed_item_visible = False
    """

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
        enemy.midDotRect = pygame.draw.circle(screen, (0, 50, 0, 100), (enemy.rect.x + 16, enemy.rect.y + 16), 1)
        if enemy.rect.colliderect(p.bulletRect) and not enemy.rect.colliderect(p.rect):
            # if bullet hits enemy, reduce enemy health
            enemy.health -= 5
            # print(enemy.health)
            if enemy.health <= 0:
                enemies.remove(enemy)
        if enemy.rect.colliderect(p.rect) or enemy.northRect.colliderect(p.rect) or enemy.eastRect.colliderect(p.rect) or enemy.southRect.colliderect(p.rect) or enemy.westRect.colliderect(p.rect):
            # print("COLLIDE!!!")
            p.health -= 1

    if p.bulletValid:
        # if bullet ability has been activated
        pygame.draw.circle(screen, (255, 255, 255), (p.bulletRect.x+18, p.bulletRect.y+17), 10)
        p.bullet()

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
