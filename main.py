import pygame
import random
import math

# initializes the pygame library
pygame.init()

rectx =  500
recty = 600

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
        self.rect.x = 195
        self.rect.y = 350
        self.pos = pygame.math.Vector2(self.rect.x,self.rect.y)

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

    def user_imput(self):
        self.velocity_x = 0
        self.velocity_y = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
            # self.rect.x = self.pos[0]
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
            # self.rect.x = self.pos[0]
        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
            # self.rect.y = self.pos[1]
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
            # self.rect.y = self.pos[1]
        if self.velocity_y != 0 and self.velocity_x != 0:
            self.velocity_y /= math.sqrt(2)
            self.velocity_x /= math.sqrt(2)
            # self.rect.y = self.pos[1]
            # self.rect.x = self.pos[0]

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def updater(self):
        self.user_imput()
        self.move()
player = Player()

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
        self.northRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.northRect.midtop = self.rect.midbottom
        self.eastRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.eastRect.midright = self.rect.midbottom
        self.southRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.southRect.midbottom = self.rect.midbottom
        self.westRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.westRect.midleft = self.rect.midbottom
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.velocity_x = 0
        self.velocity_y = 0

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
        pass
    def Enemy_calc(self):
        if enemy.rect.y < p.rect.y:
            enemy.velocity_y = enemy.speed
        if enemy.rect.y > p.rect.y:
            enemy.velocity_y = -enemy.speed
        if enemy.rect.x < p.rect.x:
            enemy.velocity_x = enemy.speed
        if enemy.rect.x > p.rect.x:
            enemy.velocity_x = -enemy.speed
        if enemy.velocity_y !=0 and enemy.velocity_x !=0:
            enemy.velocity_y /= math.sqrt(2)
            enemy.velocity_x /= math.sqrt(2)

    def Enemy_move(self):
        if enemy.rect.colliderect(p.rect):
            pass
        else:
            enemy.rect.x += enemy.velocity_x
            enemy.rect.y += enemy.velocity_y

    def Enemy_updater(self):
        self.Enemy_calc()
        self.Enemy_move()



    """def follow_mc(self):
        # follows the main character around the map
        self.velocity_x = 0
        self.velocity_y = 0
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
                    if not self.eastRect.colliderect(enemies[i].rect):
                        # enemy moves East if unobstructed
                        moveEast += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(enemies[i].rect) and not self.eastRect.colliderect(enemies[i].rect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0,3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    moveNorth += 1
                                else:
                                    # enemy moves South
                                    moveSouth += 1
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.northRect.colliderect(enemies[i].rect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(enemies[i].rect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.westRect.colliderect(enemies[i].rect):
                                    # enemy moves West as a last resort
                                    moveWest += 1
            if moveEast == (len(enemies) - 1):
                # code to move East
                self.rect.x += self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3
            elif moveNorth == (len(enemies) - 1):
                # code to move North
                self.rect.y -= self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3
            elif moveSouth == (len(enemies) -1):
                # code to move South
                self.rect.y += self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3
            elif moveWest == (len(enemies) -1):
                # code to move West
                self.rect.x -= self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3

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
                    if not self.westRect.colliderect(enemies[i].rect):
                        # enemy moves West if unobstructed
                        moveWest += 1
                    else:
                        if (self.rect.x - p.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(enemies[i].rect) and not self.eastRect.colliderect(enemies[i].rect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0,3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    moveNorth += 1
                                else:
                                    # enemy moves South
                                    moveSouth += 1
                            else:
                                # if North and Sout are not both an option, check which direct is an option
                                if not self.northRect.colliderect(enemies[i].rect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(enemies[i].rect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.eastRect.colliderect(enemies[i].rect):
                                    # enemy moves East as a last resort
                                    moveEast += 1
            if moveWest == (len(enemies) -1):
                # code to move West
                self.rect.x -= self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3
            elif moveNorth == (len(enemies) - 1):
                # code to move North
                self.rect.y -= self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3
            elif moveSouth == (len(enemies) -1):
                # code to move South
                self.rect.y += self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3
            elif moveEast == (len(enemies) - 1):
                # code to move East
                self.rect.x += self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3

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
                    if not self.southRect.colliderect(enemies[i].rect):
                        # enemy moves South if unobstructed
                        moveSouth += 1
                    else:
                        if (p.rect.y - self.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(enemies[i].rect) and not self.westRect.colliderect(enemies[i].rect):
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
                                if not self.eastRect.colliderect(enemies[i].rect):
                                    moveEast += 1
                                elif not self.westRect.colliderect(enemies[i].rect):
                                    moveWest += 1
                                elif not self.northRect.colliderect(enemies[i].rect):
                                    # enemy moves North as a last resort
                                    moveNorth += 1
            if moveSouth == (len(enemies) -1):
                # code to move South
                self.rect.y += self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3
            elif moveEast == (len(enemies) - 1):
                # code to move East
                self.rect.x += self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3
            elif moveWest == (len(enemies) -1):
                # code to move West
                self.rect.x -= self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3
            elif moveNorth == (len(enemies) - 1):
                # code to move North
                self.rect.y -= self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3

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
                    if not self.northRect.colliderect(enemies[i].rect):
                        # enemy moves North if unobstructed
                        moveNorth += 1
                    else:
                        if (self.rect.y - p.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(enemies[i].rect) and not self.westRect.colliderect(enemies[i].rect):
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
                                if not self.eastRect.colliderect(enemies[i].rect):
                                    # enemy moves east
                                    moveEast += 1
                                elif not self.westRect.colliderect(enemies[i].rect):
                                    # enemy moves west
                                    moveWest += 1
                                elif not self.southRect.colliderect(enemies[i].rect):
                                    # enemy moves South as a last resort
                                    moveSouth += 1
            if moveNorth == (len(enemies) - 1):
                # code to move North
                self.rect.y -= self.speed
                self.velocity_y -= self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3
            elif moveEast == (len(enemies) - 1):
                # code to move East
                self.rect.x += self.speed
                self.velocity_x += self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3
            elif moveWest == (len(enemies) -1):
                # code to move West
                self.rect.x -= self.speed
                self.velocity_x -= self.speed
                self.northRect.x = self.rect.x + 3
                self.eastRect.x = self.rect.x + 8
                self.southRect.x = self.rect.x + 3
                self.westRect.x = self.rect.x - 3
            elif moveSouth == (len(enemies) -1):
                # code to move South
                self.rect.y += self.speed
                self.velocity_y += self.speed
                self.northRect.y = self.rect.y - 3
                self.eastRect.y = self.rect.y + 3
                self.southRect.y = self.rect.y + 10
                self.westRect.y = self.rect.y + 3
            elif self.velocity_y != 0 and self.velocity_x != 0:
                self.velocity_y /= math.sqrt(2)
                self.velocity_x /= math.sqrt(2)"""


    def attack_mc(self):
        # when enemy reaches player collision, initiate attack animation/wind up attack, if player still in collision (plus add offset due to weapon they might have) then the player will take damage.

        # if self.rect.colliderect(p.rect):
        #     if self.inRange == False:
        #         self.startTimer=pygame.time.get_ticks()
        #     self.inRange = True
        #     if self.startTimer > 3000:
        #         # print("TESTING)
        #         pass
        #     print(self.startTimer)
        pass

# initializes the Player and Enemy classes
p = Player()
m = Map()
enemies = [Enemy(500,100,80,40) for _ in range(50)]


# loads images
bg_img = pygame.image.load('./images/island.png').convert_alpha()
speedI = pygame.image.load("./images/Noodle.png").convert_alpha()


speed_item_visible = True
game = True

while game:
    # the core game loop

    fps= clock.get_fps()
    # print(fps)

    clock.tick(60)
    # sets the fps to 60
    pygame.time.delay(5)
    # adds a very small delay to make it feel more like a game

    key_presses = pygame.key.get_pressed()
    # stores the keys that are pressed
    p.updater()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the x in the top right corner of game is clicked, the program will close.
            game = False


    # makes the map visible
    # the first tuple dictates the size (2250, 2250)
    # the second tuple dictates the starting coordinates (m.mapX, m.mapY)
    # the coordinates start at the top left of the game, which is (0,0) instead of the center
    screen.blit(pygame.transform.scale(bg_img, (2250, 2250)), (m.mapX, m.mapY))

    # makes the main character visible

    #screen.blit(pygame.transform.scale(mc_img, (35, 30)), (p.mc_x,p.mc_y))
    screen.blit(mc_img,p.pos)
    p.rect.x = p.pos[0]
    p.rect.y = p.pos[1]
    # print(p.rect.y)
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
        screen.blit(enemy1, (rectx,recty))
        enemy.generate_enemy()

        enemy.Enemy_updater()
        pygame.draw.rect(screen, (255,0,0), enemy.rect)
        pygame.draw.rect(screen, (128,0,128), enemy.northRect)
        pygame.draw.rect(screen, (128,0,128), enemy.eastRect)
        pygame.draw.rect(screen, (128,0,128), enemy.southRect)
        pygame.draw.rect(screen, (128,0,128), enemy.westRect)
        """if enemy.rect.colliderect(p.rect) or enemy.northRect.colliderect(p.rect) or enemy.eastRect.colliderect(p.rect) or enemy.southRect.colliderect(p.rect) or enemy.westRect.colliderect(p.rect):
            print("COLLISION DETECTED!!!")
            p.health -= 1"""
    index = 0
    numOfEnemies = len(enemies)

    pygame.draw.rect(screen, (0,255,0), p.rect)

    print(p.health)
    pygame.display.update()
    # print(p.pos[0])
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




"""