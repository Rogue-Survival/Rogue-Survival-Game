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
        self.northRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.northRect.midtop = self.rect.midbottom
        self.eastRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.eastRect.midright = self.rect.midbottom
        self.southRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.southRect.midbottom = self.rect.midbottom
        self.westRect = pygame.rect.Rect((self.rect.x, self.rect.y), (10,10))
        self.westRect.midleft = self.rect.midbottom

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

    def follow_mc(self):
        # follows the main character around the map
        if self.rect.x < p.rect.x:
            # enemy moves East
            n = len(enemies)
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
                        self.rect.x += self.speed
                        self.northRect.x = self.rect.x + 3
                        self.eastRect.x = self.rect.x + 8
                        self.southRect.x = self.rect.x + 3
                        self.westRect.x = self.rect.x - 3
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(enemies[i].rect) and not self.eastRect.colliderect(enemies[i].rect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0,3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                                else:
                                    # enemy moves South
                                    self.rect.y -= self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.northRect.colliderect(enemies[i].rect):
                                    # enemy moves North
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                                elif not self.southRect.colliderect(enemies[i].rect):
                                    # enemy moves South
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                                elif not self.westRect.colliderect(enemies[i].rect):
                                    # enemy moves West as a last resort
                                    self.rect.x -= self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3

        if self.rect.x > p.rect.x:
            # enemy moves West
            n = len(enemies)
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
                        self.rect.x -= self.speed
                        self.northRect.x = self.rect.x + 3
                        self.eastRect.x = self.rect.x + 8
                        self.southRect.x = self.rect.x + 3
                        self.westRect.x = self.rect.x - 3
                    else:
                        if (self.rect.x - p.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(enemies[i].rect) and not self.eastRect.colliderect(enemies[i].rect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0,3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                                else:
                                    # enemy moves South
                                    self.rect.y -= self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                            else:
                                # if North and Sout are not both an option, check which direct is an option
                                if not self.northRect.colliderect(enemies[i].rect):
                                    # enemy moves North
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                                elif not self.southRect.colliderect(enemies[i].rect):
                                    # enemy moves South
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3
                                elif not self.eastRect.colliderect(enemies[i].rect):
                                    # enemy moves East as a last resort
                                    self.rect.x += self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3

        if self.rect.y < p.rect.y:
            # enemy moves South
            n = len(enemies)
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
                        self.rect.y += self.speed
                        self.northRect.y = self.rect.y - 3
                        self.eastRect.y = self.rect.y + 3
                        self.southRect.y = self.rect.y + 10
                        self.westRect.y = self.rect.y + 3
                    else:
                        if (p.rect.y - self.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(enemies[i].rect) and not self.westRect.colliderect(enemies[i].rect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0,3)
                                if randomDirection <= 1:
                                    # enemy moves East
                                    self.rect.x += self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                                else:
                                    # enemy moves West
                                    self.rect.x -= self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                            else:
                                # if East and West are not both an option, check which direct is an option
                                if not self.eastRect.colliderect(enemies[i].rect):
                                    self.rect.x += self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                                elif not self.westRect.colliderect(enemies[i].rect):
                                    self.rect.x -= self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                                elif not self.northRect.colliderect(enemies[i].rect):
                                    # enemy moves North as a last resort
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3

        if self.rect.y > p.rect.y:
            # enemy moves North
            n = len(enemies)
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
                        self.rect.y -= self.speed
                        self.northRect.y = self.rect.y - 3
                        self.eastRect.y = self.rect.y + 3
                        self.southRect.y = self.rect.y + 10
                        self.westRect.y = self.rect.y + 3
                    else:
                        if (self.rect.y - p.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(enemies[i].rect) and not self.westRect.colliderect(enemies[i].rect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0,3)
                                if randomDirection <= 1:
                                    # enemy moves East
                                    self.rect.x += self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                                else:
                                    # enemy moves West
                                    self.rect.x -= self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                            else:
                                # if East and West are not both an option, check which direct is an option
                                if not self.eastRect.colliderect(enemies[i].rect):
                                    # enemy moves east
                                    self.rect.x += self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                                elif not self.westRect.colliderect(enemies[i].rect):
                                    # enemy moves west
                                    self.rect.x -= self.speed
                                    self.northRect.x = self.rect.x + 3
                                    self.eastRect.x = self.rect.x + 8
                                    self.southRect.x = self.rect.x + 3
                                    self.westRect.x = self.rect.x - 3
                                elif not self.southRect.colliderect(enemies[i].rect):
                                    # enemy moves South as a last resort
                                    self.rect.y += self.speed
                                    self.northRect.y = self.rect.y - 3
                                    self.eastRect.y = self.rect.y + 3
                                    self.southRect.y = self.rect.y + 10
                                    self.westRect.y = self.rect.y + 3

    def attack_mc(self):
        if self.rect.colliderect(p.rect):
            if self.inRange == False:
                self.startTimer=pygame.time.get_ticks()
            self.inRange = True
            if self.startTimer > 3000:
                # print("TESTING)
                pass
            print(self.startTimer)

# initializes the Player and Enemy classes
p = Player()
m = Map()
enemies = [Enemy(500,100,80,40) for _ in range(2)]


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
    screen.blit(pygame.transform.scale(bg_img, (2250, 2250)), (m.mapX, m.mapY))

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
        if enemy.rect.colliderect(p.rect) or enemy.northRect.colliderect(p.rect) or enemy.eastRect.colliderect(p.rect) or enemy.southRect.colliderect(p.rect) or enemy.westRect.colliderect(p.rect):
            print("COLLISION DETECTED!!!")
            p.health -= 1
    index = 0
    numOfEnemies = len(enemies)

    pygame.draw.rect(screen, (0,255,0), p.rect)

    print(p.health)
    pygame.display.update()

pygame.quit()








# when enemy reaches player collision, initiate attack animation/wind up attack, if player still in collision (plus add offset due to weapon they might have) then the player will take damage.





