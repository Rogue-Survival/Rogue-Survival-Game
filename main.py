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

enemyOriginal = pygame.image.load("./images/slime.png").convert_alpha()

enemy1 = pygame.image.load("./images/slime1.png").convert_alpha()
enemy2 = pygame.image.load("./images/slime2.png").convert_alpha()
enemy3 = pygame.image.load("./images/slime3.png").convert_alpha()
enemy4 = pygame.image.load("./images/slime4.png").convert_alpha()

batImg1 = pygame.image.load("./images/bat1.png").convert_alpha()
batImg2 = pygame.image.load("./images/bat2.png").convert_alpha()

minibee1 = pygame.image.load("./images/EarthElemental1.png").convert_alpha()
minibee2 = pygame.image.load("./images/EarthElemental2.png").convert_alpha()
minibee3 = pygame.image.load("./images/EarthElemental3.png").convert_alpha()
minibee4 = pygame.image.load("./images/EarthElemental4.png").convert_alpha()

skeletonKing1 = pygame.image.load("./images/skeletonKing1.png").convert_alpha()
skeletonKing2 = pygame.image.load("./images/skeletonKing2.png").convert_alpha()
skeletonKing3 = pygame.image.load("./images/skeletonKing3.png").convert_alpha()
skeletonKing4 = pygame.image.load("./images/skeletonKing4.png").convert_alpha()

bullet_upgrade = pygame.image.load("./images/Noodle.png").convert_alpha()


xp = []
xp_hit = []

class Map(pygame.sprite.Sprite):
    # Controls map boundaries and map camera
    def __init__(self, mapX=-800, mapY=-800):
        pygame.sprite.Sprite.__init__(self)
        self.mapX = mapX
        self.mapY = mapY
        self.cameraX = -140
        self.cameraY = -140
        self.leftBoundaryX = -245
        self.leftBoundaryY1 = -235
        self.leftBoundaryY2 = 1079

        self.rightBoundaryX = 1072
        self.rightBoundaryY1 = -235
        self.rightBoundaryY2 = 1079

        self.topBoundaryX1 = -240
        self.topBoundaryX2 = 1072
        self.topBoundaryY = -230

        self.bottomBoundaryX1 = -240
        self.bottomBoundaryX2 = 1072
        self.bottomBoundaryY = 1073

        self.leftBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.leftBoundaryX, self.leftBoundaryY1), (self.leftBoundaryX, self.leftBoundaryY2), 12)
        self.rightBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.rightBoundaryX, self.rightBoundaryY1), (self.rightBoundaryX, self.rightBoundaryY2), 12)
        self.topBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.topBoundaryX1, self.topBoundaryY), (self.topBoundaryX2, self.topBoundaryY), 12)
        self.bottomBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.bottomBoundaryX1, self.bottomBoundaryY), (self.bottomBoundaryX2, self.bottomBoundaryY), 12)

    def get_mapX(self):
        # returns the x coordinate of the map
        return self.mapX

    def get_mapY(self):
        # returns the y coordinate of the map
        return self.mapY

    def update_boundary(self):
        # keep the map boundaries updated
        self.leftBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.leftBoundaryX, self.leftBoundaryY1), (self.leftBoundaryX, self.leftBoundaryY2), 12)
        self.rightBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.rightBoundaryX, self.rightBoundaryY1), (self.rightBoundaryX, self.rightBoundaryY2), 12)
        self.topBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.topBoundaryX1, self.topBoundaryY), (self.topBoundaryX2, self.topBoundaryY), 12)
        self.bottomBoundary = pygame.draw.line(transparentSurface, (255, 0, 0), (self.bottomBoundaryX1, self.bottomBoundaryY), (self.bottomBoundaryX2, self.bottomBoundaryY), 12)


class Player(pygame.sprite.Sprite):
    # Player class controls basic functions relating to the player
    def __init__(self, speed=4, health=100):
        # inherits from the pygame.sprite.Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = "./images/MAIN_CHARACTER.png"
        self.health = health
        self.rect = mc_img.get_rect().scale_by(2,2)
        self.rect.x = 400
        self.rect.y = 400
        self.rect.width = 40
        self.gold = 0
        self.orspeed = 0
        self.bulletdamage = 25
        self.meleedamage = 50
        self.check = False

    def get_speed(self):
        # returns speed of player
        return self.speed

    def get_image(self):
        # returns image of player
        return self.image

    def move_west(self):
        # moves the player West
        if self.rect.x > m.leftBoundaryX + 25:
            m.cameraX -= self.speed
            # m.leftBoundaryY += self.speed
            m.leftBoundaryX += self.speed
            m.rightBoundaryX += self.speed
            m.topBoundaryX1 += self.speed
            m.topBoundaryX2 += self.speed
            m.bottomBoundaryX1 += self.speed
            m.bottomBoundaryX2 += self.speed
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
            for bat in bats:
                bat.rect.x += self.speed
                bat.northRect.x = bat.rect.x + bat.northXVal
                bat.eastRect.x = bat.rect.x + bat.eastXVal
                bat.southRect.x = bat.rect.x + bat.southXVal
                bat.westRect.x = bat.rect.x - bat.westXVal
            for x in xp:
                x.x += self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                sk.rect.x += self.speed
                sk.northRect.x = sk.rect.x + sk.northXVal
                sk.eastRect.x = sk.rect.x + sk.eastXVal
                sk.southRect.x = sk.rect.x + sk.southXVal
                sk.westRect.x = sk.rect.x - sk.westXVal
            if ee.activate and not ee.felled:
                ee.rect.x += self.speed
                ee.northRect.x = ee.rect.x + ee.northXVal
                ee.eastRect.x = ee.rect.x + ee.eastXVal
                ee.southRect.x = ee.rect.x + ee.southXVal
                ee.westRect.x = ee.rect.x - ee.westXVal
            if bup.upgradeout:
                bup.rect.x += self.speed

    def move_east(self):
        # moves the player East
        if self.rect.x < m.rightBoundaryX - 50:
            m.cameraX += self.speed
            # m.leftBoundaryY -= self.speed
            m.leftBoundaryX -= self.speed
            m.rightBoundaryX -= self.speed
            m.topBoundaryX1 -= self.speed
            m.topBoundaryX2 -= self.speed
            m.bottomBoundaryX1 -= self.speed
            m.bottomBoundaryX2 -= self.speed
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
            for bat in bats:
                bat.rect.x -= self.speed
                bat.northRect.x = bat.rect.x + bat.northXVal
                bat.eastRect.x = bat.rect.x + bat.eastXVal
                bat.southRect.x = bat.rect.x + bat.southXVal
                bat.westRect.x = bat.rect.x - bat.westXVal
            for x in xp:
                x.x -= self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                sk.rect.x -= self.speed
                sk.northRect.x = sk.rect.x + sk.northXVal
                sk.eastRect.x = sk.rect.x + sk.eastXVal
                sk.southRect.x = sk.rect.x + sk.southXVal
                sk.westRect.x = sk.rect.x - sk.westXVal
            if ee.activate and not ee.felled:
                ee.rect.x -= self.speed
                ee.northRect.x = ee.rect.x + ee.northXVal
                ee.eastRect.x = ee.rect.x + ee.eastXVal
                ee.southRect.x = ee.rect.x + ee.southXVal
                ee.westRect.x = ee.rect.x - ee.westXVal
            if bup.upgradeout:
                bup.rect.x -= self.speed

    def move_north(self):
        # moves the player North
        if self.rect.y > m.topBoundaryY + 25:
            m.cameraY -= self.speed
            m.leftBoundaryY1 += self.speed
            m.leftBoundaryY2 += self.speed
            m.rightBoundaryY1 += self.speed
            m.rightBoundaryY2 += self.speed
            m.topBoundaryY += self.speed
            m.bottomBoundaryY += self.speed
            # m.leftBoundaryX += self.speed
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
            for bat in bats:
                bat.rect.y += self.speed
                bat.northRect.y = bat.rect.y - bat.northYVal
                bat.eastRect.y = bat.rect.y + bat.eastYVal
                bat.southRect.y = bat.rect.y + bat.southYVal
                bat.westRect.y = bat.rect.y + bat.westYVal
            for x in xp:
                x.y += self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                sk.rect.y += self.speed
                sk.northRect.y = sk.rect.y - sk.northYVal
                sk.eastRect.y = sk.rect.y + sk.eastYVal
                sk.southRect.y = sk.rect.y + sk.southYVal
                sk.westRect.y = sk.rect.y + sk.westYVal
            if ee.activate and not ee.felled:
                ee.rect.y += self.speed
                ee.northRect.y = ee.rect.y - ee.northYVal
                ee.eastRect.y = ee.rect.y + ee.eastYVal
                ee.southRect.y = ee.rect.y + ee.southYVal
                ee.westRect.y = ee.rect.y + ee.westYVal
            if bup.upgradeout:
                bup.rect.y += self.speed

    def move_south(self):
        # moves the player South
        if self.rect.y < m.bottomBoundaryY - 50:
            m.cameraY += self.speed
            m.leftBoundaryY1 -= self.speed
            m.leftBoundaryY2 -= self.speed
            m.rightBoundaryY1 -= self.speed
            m.rightBoundaryY2 -= self.speed
            m.topBoundaryY -= self.speed
            m.bottomBoundaryY -= self.speed
            # m.leftBoundaryX -= self.speed
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
            for bat in bats:
                bat.rect.y -= self.speed
                bat.northRect.y = bat.rect.y - bat.northYVal
                bat.eastRect.y = bat.rect.y + bat.eastYVal
                bat.southRect.y = bat.rect.y + bat.southYVal
                bat.westRect.y = bat.rect.y + bat.westYVal
            for x in xp:
                x.y -= self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                sk.rect.y -= self.speed
                sk.northRect.y = sk.rect.y - sk.northYVal
                sk.eastRect.y = sk.rect.y + sk.eastYVal
                sk.southRect.y = sk.rect.y + sk.southYVal
                sk.westRect.y = sk.rect.y + sk.westYVal
            if ee.activate and not ee.felled:
                ee.rect.y -= self.speed
                ee.northRect.y = ee.rect.y - ee.northYVal
                ee.eastRect.y = ee.rect.y + ee.eastYVal
                ee.southRect.y = ee.rect.y + ee.southYVal
                ee.westRect.y = ee.rect.y + ee.westYVal
            if bup.upgradeout:
                bup.rect.y -= self.speed

    def move_northeast(self):
        # moves player north east
        if self.rect.y > m.topBoundaryY + 25 and self.rect.x <= m.rightBoundaryX - 50:
            Dspeed = self.speed / math.sqrt(2)
            m.cameraX += Dspeed
            m.cameraY -= Dspeed
            m.leftBoundaryY1 += Dspeed
            m.leftBoundaryY2 += Dspeed
            m.rightBoundaryY1 += Dspeed
            m.rightBoundaryY2 += Dspeed
            m.topBoundaryY += Dspeed
            m.bottomBoundaryY += Dspeed
            m.leftBoundaryX -= Dspeed
            m.rightBoundaryX -= Dspeed
            m.topBoundaryX1 -= Dspeed
            m.topBoundaryX2 -= Dspeed
            m.bottomBoundaryX1 -= Dspeed
            m.bottomBoundaryX2 -= Dspeed
            n = len(enemies)
            count = 0
            southCount = 0
            eastCount = 0
            westCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y += Dspeed
                enemy.rect.x -= Dspeed
                enemy.northRect.y = enemy.rect.y - enemy.northYVal
                enemy.eastRect.y = enemy.rect.y + enemy.eastYVal
                enemy.southRect.y = enemy.rect.y + enemy.southYVal
                enemy.westRect.y = enemy.rect.y + enemy.westYVal
                enemy.northRect.x = enemy.rect.x + enemy.northXVal
                enemy.eastRect.x = enemy.rect.x + enemy.eastXVal
                enemy.southRect.x = enemy.rect.x + enemy.southXVal
                enemy.westRect.x = enemy.rect.x - enemy.westXVal
            for x in xp:
                x.y += Dspeed
                x.x -= Dspeed
                x.xp_stationary()
            for bat in bats:
                bat.rect.y += Dspeed
                bat.rect.x -= Dspeed
                bat.northRect.y = bat.rect.y - bat.northYVal
                bat.eastRect.y = bat.rect.y + bat.eastYVal
                bat.southRect.y = bat.rect.y + bat.southYVal
                bat.westRect.y = bat.rect.y + bat.westYVal
                bat.northRect.x = bat.rect.x + bat.northXVal
                bat.eastRect.x = bat.rect.x + bat.eastXVal
                bat.southRect.x = bat.rect.x + bat.southXVal
                bat.westRect.x = bat.rect.x - bat.westXVal
            if sk.activate and not sk.felled:
                sk.rect.y += Dspeed
                sk.rect.x -= Dspeed
                sk.northRect.y = sk.rect.y - sk.northYVal
                sk.eastRect.y = sk.rect.y + sk.eastYVal
                sk.southRect.y = sk.rect.y + sk.southYVal
                sk.westRect.y = sk.rect.y + sk.westYVal
                sk.northRect.x = sk.rect.x + sk.northXVal
                sk.eastRect.x = sk.rect.x + sk.eastXVal
                sk.southRect.x = sk.rect.x + sk.southXVal
                sk.westRect.x = sk.rect.x - sk.westXVal
            if ee.activate and not ee.felled:
                ee.rect.y += Dspeed
                ee.rect.x -= Dspeed
                ee.northRect.y = ee.rect.y - ee.northYVal
                ee.eastRect.y = ee.rect.y + ee.eastYVal
                ee.southRect.y = ee.rect.y + ee.southYVal
                ee.westRect.y = ee.rect.y + ee.westYVal
                ee.northRect.x = ee.rect.x + ee.northXVal
                ee.eastRect.x = ee.rect.x + ee.eastXVal
                ee.southRect.x = ee.rect.x + ee.southXVal
                ee.westRect.x = ee.rect.x - ee.westXVal
            if bup.upgradeout:
                bup.rect.x -= Dspeed
                bup.rect.y += Dspeed
        elif self.rect.y > m.topBoundaryY + 25:
            self.move_north()
        elif self.rect.x <= m.rightBoundaryX - 50:
            self.move_east()

    def move_northwest(self):
        if self.rect.y > m.topBoundaryY + 25 and self.rect.x > m.leftBoundaryX + 25:
            Dspeed = self.speed / math.sqrt(2)
            m.cameraX -= Dspeed
            m.cameraY -= Dspeed
            m.leftBoundaryX += Dspeed
            m.rightBoundaryX += Dspeed
            m.topBoundaryX1 += Dspeed
            m.topBoundaryX2 += Dspeed
            m.bottomBoundaryX1 += Dspeed
            m.bottomBoundaryX2 += Dspeed
            m.leftBoundaryY1 += Dspeed
            m.leftBoundaryY2 += Dspeed
            m.rightBoundaryY1 += Dspeed
            m.rightBoundaryY2 += Dspeed
            m.topBoundaryY += Dspeed
            m.bottomBoundaryY += Dspeed
            n = len(enemies)
            count = 0
            northCount = 0
            eastCount = 0
            westCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y += Dspeed
                enemy.rect.x += Dspeed
                enemy.northRect.y = enemy.rect.y - enemy.northYVal
                enemy.eastRect.y = enemy.rect.y + enemy.eastYVal
                enemy.southRect.y = enemy.rect.y + enemy.southYVal
                enemy.westRect.y = enemy.rect.y + enemy.westYVal
                enemy.northRect.x = enemy.rect.x + enemy.northXVal
                enemy.eastRect.x = enemy.rect.x + enemy.eastXVal
                enemy.southRect.x = enemy.rect.x + enemy.southXVal
                enemy.westRect.x = enemy.rect.x - enemy.westXVal
            for x in xp:
                x.y += Dspeed
                x.x += Dspeed
                x.xp_stationary()
            for bat in bats:
                bat.rect.y += Dspeed
                bat.rect.x += Dspeed
                bat.northRect.y = bat.rect.y - bat.northYVal
                bat.eastRect.y = bat.rect.y + bat.eastYVal
                bat.southRect.y = bat.rect.y + bat.southYVal
                bat.westRect.y = bat.rect.y + bat.westYVal
                bat.northRect.x = bat.rect.x + bat.northXVal
                bat.eastRect.x = bat.rect.x + bat.eastXVal
                bat.southRect.x = bat.rect.x + bat.southXVal
                bat.westRect.x = bat.rect.x - bat.westXVal
            if sk.activate and not sk.felled:
                sk.rect.y += Dspeed
                sk.rect.x += Dspeed
                sk.northRect.y = sk.rect.y - sk.northYVal
                sk.eastRect.y = sk.rect.y + sk.eastYVal
                sk.southRect.y = sk.rect.y + sk.southYVal
                sk.westRect.y = sk.rect.y + sk.westYVal
                sk.northRect.x = sk.rect.x + sk.northXVal
                sk.eastRect.x = sk.rect.x + sk.eastXVal
                sk.southRect.x = sk.rect.x + sk.southXVal
                sk.westRect.x = sk.rect.x - sk.westXVal
            if ee.activate and not ee.felled:
                ee.rect.y += Dspeed
                ee.rect.x += Dspeed
                ee.northRect.y = ee.rect.y - ee.northYVal
                ee.eastRect.y = ee.rect.y + ee.eastYVal
                ee.southRect.y = ee.rect.y + ee.southYVal
                ee.westRect.y = ee.rect.y + ee.westYVal
                ee.northRect.x = ee.rect.x + ee.northXVal
                ee.eastRect.x = ee.rect.x + ee.eastXVal
                ee.southRect.x = ee.rect.x + ee.southXVal
                ee.westRect.x = ee.rect.x - ee.westXVal
            if bup.upgradeout:
                bup.rect.x += Dspeed
                bup.rect.y += Dspeed
        elif self.rect.y > m.topBoundaryY + 25:
            self.move_north()
        elif self.rect.x > m.leftBoundaryX + 25:
            self.move_west()

    def move_southeast(self):
        # Moves player south east
        if self.rect.y < m.bottomBoundaryY - 50 and self.rect.x < m.rightBoundaryX - 50:
            Dspeed = self.speed / math.sqrt(2)
            m.cameraX += Dspeed
            m.leftBoundaryX -= Dspeed
            m.rightBoundaryX -= Dspeed
            m.topBoundaryX1 -= Dspeed
            m.topBoundaryX2 -= Dspeed
            m.bottomBoundaryX1 -= Dspeed
            m.bottomBoundaryX2 -= Dspeed
            m.cameraY += Dspeed
            m.leftBoundaryY1 -= Dspeed
            m.leftBoundaryY2 -= Dspeed
            m.rightBoundaryY1 -= Dspeed
            m.rightBoundaryY2 -= Dspeed
            m.topBoundaryY -= Dspeed
            m.bottomBoundaryY -= Dspeed
            n = len(enemies)
            count = 0
            southCount = 0
            eastCount = 0
            westCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y -= Dspeed
                enemy.rect.x -= Dspeed
                enemy.northRect.y = enemy.rect.y - enemy.northYVal
                enemy.eastRect.y = enemy.rect.y + enemy.eastYVal
                enemy.southRect.y = enemy.rect.y + enemy.southYVal
                enemy.westRect.y = enemy.rect.y + enemy.westYVal
                enemy.northRect.x = enemy.rect.x + enemy.northXVal
                enemy.eastRect.x = enemy.rect.x + enemy.eastXVal
                enemy.southRect.x = enemy.rect.x + enemy.southXVal
                enemy.westRect.x = enemy.rect.x - enemy.westXVal
            for x in xp:
                x.y -= Dspeed
                x.x -= Dspeed
                x.xp_stationary()
            for bat in bats:
                bat.rect.y -= Dspeed
                bat.rect.x -= Dspeed
                bat.northRect.y = bat.rect.y - bat.northYVal
                bat.eastRect.y = bat.rect.y + bat.eastYVal
                bat.southRect.y = bat.rect.y + bat.southYVal
                bat.westRect.y = bat.rect.y + bat.westYVal
                bat.northRect.x = bat.rect.x + bat.northXVal
                bat.eastRect.x = bat.rect.x + bat.eastXVal
                bat.southRect.x = bat.rect.x + bat.southXVal
                bat.westRect.x = bat.rect.x - bat.westXVal
            if sk.activate and not sk.felled:
                sk.rect.y -= Dspeed
                sk.rect.x -= Dspeed
                sk.northRect.y = sk.rect.y - sk.northYVal
                sk.eastRect.y = sk.rect.y + sk.eastYVal
                sk.southRect.y = sk.rect.y + sk.southYVal
                sk.westRect.y = sk.rect.y + sk.westYVal
                sk.northRect.x = sk.rect.x + sk.northXVal
                sk.eastRect.x = sk.rect.x + sk.eastXVal
                sk.southRect.x = sk.rect.x + sk.southXVal
                sk.westRect.x = sk.rect.x - sk.westXVal
            if ee.activate and not ee.felled:
                ee.rect.y -= Dspeed
                ee.rect.x -= Dspeed
                ee.northRect.y = ee.rect.y - ee.northYVal
                ee.eastRect.y = ee.rect.y + ee.eastYVal
                ee.southRect.y = ee.rect.y + ee.southYVal
                ee.westRect.y = ee.rect.y + ee.westYVal
                ee.northRect.x = ee.rect.x + ee.northXVal
                ee.eastRect.x = ee.rect.x + ee.eastXVal
                ee.southRect.x = ee.rect.x + ee.southXVal
                ee.westRect.x = ee.rect.x - ee.westXVal
            if bup.upgradeout:
                bup.rect.x -= Dspeed
                bup.rect.y -= Dspeed
        elif self.rect.y < m.bottomBoundaryY - 50:
            self.move_south()
        elif self.rect.x < m.rightBoundaryX - 50:
            self.move_east()

    def move_southwest(self):
        # moves player south west
        if self.rect.y < m.bottomBoundaryY - 50 and self.rect.x > m.leftBoundaryX + 25:
            Dspeed = self.speed / math.sqrt(2)
            m.cameraX -= Dspeed
            m.leftBoundaryX += Dspeed
            m.rightBoundaryX += Dspeed
            m.topBoundaryX1 += Dspeed
            m.topBoundaryX2 += Dspeed
            m.bottomBoundaryX1 += Dspeed
            m.bottomBoundaryX2 += Dspeed
            m.cameraY += Dspeed
            m.leftBoundaryY1 -= Dspeed
            m.leftBoundaryY2 -= Dspeed
            m.rightBoundaryY1 -= Dspeed
            m.rightBoundaryY2 -= Dspeed
            m.topBoundaryY -= Dspeed
            m.bottomBoundaryY -= Dspeed
            n = len(enemies)
            count = 0
            southCount = 0
            eastCount = 0
            westCount = 0
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y -= Dspeed
                enemy.rect.x += Dspeed
                enemy.northRect.y = enemy.rect.y - enemy.northYVal
                enemy.eastRect.y = enemy.rect.y + enemy.eastYVal
                enemy.southRect.y = enemy.rect.y + enemy.southYVal
                enemy.westRect.y = enemy.rect.y + enemy.westYVal
                enemy.northRect.x = enemy.rect.x + enemy.northXVal
                enemy.eastRect.x = enemy.rect.x + enemy.eastXVal
                enemy.southRect.x = enemy.rect.x + enemy.southXVal
                enemy.westRect.x = enemy.rect.x - enemy.westXVal
            for x in xp:
                x.y -= Dspeed
                x.x += Dspeed
                x.xp_stationary()
            for bat in bats:
                bat.rect.x += Dspeed
                bat.rect.y -= Dspeed
                bat.northRect.x = bat.rect.x + bat.northXVal
                bat.eastRect.x = bat.rect.x + bat.eastXVal
                bat.southRect.x = bat.rect.x + bat.southXVal
                bat.westRect.x = bat.rect.x - bat.westXVal
                bat.northRect.y = bat.rect.y - bat.northYVal
                bat.eastRect.y = bat.rect.y + bat.eastYVal
                bat.southRect.y = bat.rect.y + bat.southYVal
                bat.westRect.y = bat.rect.y + bat.westYVal
            if sk.activate and not sk.felled:
                sk.rect.x += Dspeed
                sk.rect.y -= Dspeed
                sk.northRect.x = sk.rect.x + sk.northXVal
                sk.eastRect.x = sk.rect.x + sk.eastXVal
                sk.southRect.x = sk.rect.x + sk.southXVal
                sk.westRect.x = sk.rect.x - sk.westXVal
                sk.northRect.y = sk.rect.y - sk.northYVal
                sk.eastRect.y = sk.rect.y + sk.eastYVal
                sk.southRect.y = sk.rect.y + sk.southYVal
                sk.westRect.y = sk.rect.y + sk.westYVal
            if ee.activate and not ee.felled:
                ee.rect.x += Dspeed
                ee.rect.y -= Dspeed
                ee.northRect.x = ee.rect.x + ee.northXVal
                ee.eastRect.x = ee.rect.x + ee.eastXVal
                ee.southRect.x = ee.rect.x + ee.southXVal
                ee.westRect.x = ee.rect.x - ee.westXVal
                ee.northRect.y = ee.rect.y - ee.northYVal
                ee.eastRect.y = ee.rect.y + ee.eastYVal
                ee.southRect.y = ee.rect.y + ee.southYVal
                ee.westRect.y = ee.rect.y + ee.westYVal
            if bup.upgradeout:
                bup.rect.x += Dspeed
                bup.rect.y -= Dspeed

        elif self.rect.y < m.bottomBoundaryY - 50:
            self.move_south()
        elif self.rect.x > m.leftBoundaryX + 25:
            self.move_west()


class BasicAttack(pygame.sprite.Sprite):
    # Creates Basic Attacks for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = None
        self.hitBoxRect = pygame.draw.circle(transparentSurface, (255,255,255), (p.rect.x+19, p.rect.y+19), 64)

        self.east = False
        self.northEast = False
        self.north = False
        self.northWest = False
        self.west = False
        self.southWest = False
        self.south = False
        self.southEast = False
        self.eastEND = False

        self.eastCounter = 0
        self.northEastCounter = 0
        self.northCounter = 0
        self.northWestCounter = 0
        self.westCounter = 0
        self.southWestCounter = 0
        self.southCounter = 0
        self.southEastCounter = 0
        self.eastENDCounter = 0

        self.running = False
        self.finished = False


    def attack(self):
        # Initiate basic attack

        # self.east = pygame.draw.line(screen, (160,32,240), (p.rect.x+36, p.rect.y+17), (p.rect.x+80, p.rect.y+17), 6)
        # self.northEast = pygame.draw.line(screen, (160,32,240), (p.rect.x+33, p.rect.y+4), (p.rect.x+60, p.rect.y-22), 6)
        # self.north = pygame.draw.line(screen, (160,32,240), (p.rect.x+18, p.rect.y-4), (p.rect.x+18, p.rect.y-44), 6)
        # self.northWest = pygame.draw.line(screen, (160,32,240), (p.rect.x, p.rect.y+4), (p.rect.x-27, p.rect.y-22), 6)
        # self.west = pygame.draw.line(screen, (160,32,240), (p.rect.x, p.rect.y+17), (p.rect.x-44, p.rect.y+17), 6)
        # self.southWest = pygame.draw.line(screen, (160,32,240), (p.rect.x, p.rect.y+32), (p.rect.x-27, p.rect.y+60), 6)
        # self.south = pygame.draw.line(screen, (160,32,240), (p.rect.x+18, p.rect.y+32), (p.rect.x+18, p.rect.y+78), 6)
        # self.southEast = pygame.draw.line(screen, (160,32,240), (p.rect.x+33, p.rect.y+32), (p.rect.x+64, p.rect.y+60), 6)

        total_time = pygame.time.get_ticks() / 1000

        if int(total_time) % 2 == 0 and total_time > 1 and not self.east:
            self.running = True
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x+36, p.rect.y+17), (p.rect.x+80, p.rect.y+17), 6)
            self.eastCounter += 1
            if self.eastCounter > 2:
                self.rect = None
                self.east = True
        if self.east and not self.northEast:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x+33, p.rect.y+4), (p.rect.x+60, p.rect.y-22), 6)
            self.northEastCounter += 1
            if self.northEastCounter > 2:
                self.rect = None
                self.northEast = True
        if self.northEast and not self.north:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x+18, p.rect.y-4), (p.rect.x+18, p.rect.y-44), 6)
            self.northCounter += 1
            if self.northCounter > 2:
                self.rect = None
                self.north = True
        if self.north and not self.northWest:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x, p.rect.y+4), (p.rect.x-27, p.rect.y-22), 6)
            self.northWestCounter += 1
            if self.northWestCounter > 2:
                self.rect = None
                self.northWest = True
        if self.northWest and not self.west:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x, p.rect.y+17), (p.rect.x-44, p.rect.y+17), 6)
            self.westCounter += 1
            if self.westCounter > 2:
                self.rect = None
                self.west = True
        if self.west and not self.southWest:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x, p.rect.y+32), (p.rect.x-27, p.rect.y+60), 6)
            self.southWestCounter += 1
            if self.southWestCounter > 2:
                self.rect = None
                self.southWest = True
        if self.southWest and not self.south:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x+18, p.rect.y+32), (p.rect.x+18, p.rect.y+78), 6)
            self.southCounter += 1
            if self.southCounter > 2:
                self.rect = None
                self.south = True
        if self.south and not self.southEast:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x+33, p.rect.y+32), (p.rect.x+64, p.rect.y+60), 6)
            self.southEastCounter += 1
            if self.southEastCounter > 2:
                self.rect = None
                self.southEast = True
        if self.southEast and not self.eastEND:
            self.rect = pygame.draw.line(screen, (160,32,240), (p.rect.x+36, p.rect.y+17), (p.rect.x+80, p.rect.y+17), 6)
            # new_time = pygame.time.get_ticks()
            self.eastENDCounter += 1
            if self.eastENDCounter > 1:
                self.rect = None
                self.eastEND = True
                self.running = False
                self.finished = True

        if int(total_time) % 2 != 0 and self.east:
            self.east = False
            self.northEast = False
            self.north = False
            self.northWest = False
            self.west = False
            self.southWest = False
            self.south = False
            self.southEast = False
            self.eastEND = False

            self.eastCounter = 0
            self.northEastCounter = 0
            self.northCounter = 0
            self.northWestCounter = 0
            self.westCounter = 0
            self.southWestCounter = 0
            self.southCounter = 0
            self.southEastCounter = 0
            self.eastENDCounter = 0

            for enemy in enemies:
                enemy.meleeAttackCollisions.clear()
            if sk.activate and not sk.felled:
                sk.meleeAttackCollisions.clear()
            if ee.activate and not sk.felled:
                ee.meleeAttackCollisions.clear()
            for bat in bats:
                bat.meleeAttackCollisions.clear()

class Bullet_Upgrade():
    def __init__(self):
        self.rect = bullet_upgrade.get_rect().scale_by(1,1)
        self.rect.x = 0
        self.rect.y = 0
        self.upgradeout = True
        self.upgradeactive = False
        self.animation = 0




class Bullet(pygame.sprite.Sprite):
    # Bullet class allows the player to shoot bullets at enemies
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.draw.circle(transparentSurface, (255,255,255), (p.rect.x+18,p.rect.y+17), 10)
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
        self.shooting = False
        self.overflow = 0

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
                # print("1")
            elif (self.rect.x < self.startingPoint[0] and self.rect.y > self.startingPoint[1]) and self.positionReached:
                # third quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print('-------------------')
                # print("third quadrant - CONTINUING JOURNEY")
                # print('-------------------')
                # print("2")
            elif (self.rect.x < self.startingPoint[0] and self.rect.y < self.startingPoint[1]) and self.positionReached:
                # second quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print('-------------------')
                # print("second quadrant - CONTINUING JOURNEY")
                # print('-------------------')
                # print("3")
            elif (self.rect.x > self.startingPoint[0] and self.rect.y < self.startingPoint[1]) and self.positionReached:
                # first quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print('-------------------')
                # print("first quadrant - CONTINUING JOURNEY")
                # print('-------------------')
                # print("4")
            elif self.rect.x < self.mousePOS[0] and self.rect.y < self.mousePOS[1]:
                # fourth quadrant - travels to mouse position
                self.rect.y += math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                self.counterX += 1
                self.counterY += 1
                # print(self.counterX)
                # print(self.counterY)
                if self.mousePOS[1] - self.rect.y < 10 and self.mousePOS[0] - self.rect.x < 10:
                    self.positionReached = True
                # print('-------------------')
                # print("fourth quadrant")
                # print('-------------------')
                # print("5")
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
                # print("6")
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
                # print("7")
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
                # print("8")
            else:
                if self.mousePOS[1] > self.startingPoint[1] and (abs(self.mousePOS[0]) - abs(self.startingPoint[0])) < 15:
                    self.rect.y += math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                    # print("YEP")
                elif self.mousePOS[1] < self.startingPoint[1] and (abs(self.mousePOS[0]) - abs(self.startingPoint[0])) < 15:
                    self.rect.y -= math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                    self.rect.y -= math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                    # print("YEP2")
                self.counterX += 1
                self.counterY += 1
class calctargets():
    import math

    def calcclosest(t1, o1, n1):
        closest_targets = []
        close = []
        # Iterate through the enemies and checks their distances then adds them to the list
        for t1 in o1:
            xcor = t1.rect.x - p.rect.x
            ycor = t1.rect.y - p.rect.y
            distance = math.sqrt(xcor ** 2 + ycor ** 2)
            close.append((t1, distance))

        # Sorts and condenses the list to n closest targets.
        sorted_close = sorted(close, key=lambda x: x[1])
        closest_targets = sorted_close[:n1]
        return print(closest_targets)

    def calcfarthest(t1,o1,n1):
        farthesttarget = []
        for t1 in o1:
            # itterates through the enemies and checks thier distances then adds them to the list
            xcor = t1.rect.x - p.rect.x
            ycor = t1.rect.y - p.rect.y
            distance = math.sqrt(xcor ** 2 + ycor ** 2)
            farthesttarget.append((t1, distance))

        # sorts and condenses the list to targets.
        farthesttarget.sort(key=lambda x: x[1], reverse=True)
        farthest_one = farthesttarget[:n1]
        return farthest_one

    def calcdistance(self):
            xcor = self.rect.x - p.rect.x
            ycor = self.rect.y - p.rect.y
            distance = math.sqrt(xcor ** 2 + ycor ** 2)
            return distance





class Enemy(pygame.sprite.Sprite):
    # Enemy class controls basic functions relating to the enemy
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = random.uniform(1.3, 2)
        self.image = "./images/slimeRect.png"
        self.rect = enemy1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
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
        self.tempTime = 0
        self.previousPOS = ()
        self.meleeAttackCollisions = []
        self.spawned = []
        self.spawnTimer = 0
        self.spawnIndicator = None
        self.animation = 1
        self.bat = False
        self.mini = False
        self.skeletonKing = False
        self.enemyLength = 0
        self.enemyList = None


    def get_speed(self):
        # returns speed of player
        return self.speed

    def get_image(self):
        # returns image of player
        return self.image

    def generate_enemy(self):
        pass

    def spawn(self):
        self.spawned.append(1)

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

    def travel_northeast(self):
        # Enemy moves north-east
        Dspeed = self.speed / math.sqrt(2)
        self.rect.y -= Dspeed
        self.rect.x += Dspeed
        self.northRect.y = self.rect.y - self.northYVal
        self.eastRect.y = self.rect.y + self.eastYVal
        self.southRect.y = self.rect.y + self.southYVal
        self.westRect.y = self.rect.y + self.westYVal
        self.northRect.x = self.rect.x + self.northXVal
        self.eastRect.x = self.rect.x + self.eastXVal
        self.southRect.x = self.rect.x + self.southXVal
        self.westRect.x = self.rect.x - self.westXVal

    def travel_northwest(self):
        # Eneny moves north-west
        Dspeed = self.speed / math.sqrt(2)
        self.rect.y -= Dspeed
        self.rect.x -= Dspeed
        self.northRect.y = self.rect.y - self.northYVal
        self.eastRect.y = self.rect.y + self.eastYVal
        self.southRect.y = self.rect.y + self.southYVal
        self.westRect.y = self.rect.y + self.westYVal
        self.northRect.x = self.rect.x + self.northXVal
        self.eastRect.x = self.rect.x + self.eastXVal
        self.southRect.x = self.rect.x + self.southXVal
        self.westRect.x = self.rect.x - self.westXVal

    def travel_southeast(self):
        # Enemy moves south-east
        Dspeed = self.speed / math.sqrt(2)
        self.rect.y += Dspeed
        self.rect.x += Dspeed
        self.northRect.y = self.rect.y - self.northYVal
        self.eastRect.y = self.rect.y + self.eastYVal
        self.southRect.y = self.rect.y + self.southYVal
        self.westRect.y = self.rect.y + self.westYVal
        self.northRect.x = self.rect.x + self.northXVal
        self.eastRect.x = self.rect.x + self.eastXVal
        self.southRect.x = self.rect.x + self.southXVal
        self.westRect.x = self.rect.x - self.westXVal

    def travel_southwest(self):
        # Enemy moves soouth-west
        Dspeed = self.speed / math.sqrt(2)
        self.rect.y += Dspeed
        self.rect.x -= Dspeed
        self.northRect.y = self.rect.y - self.northYVal
        self.eastRect.y = self.rect.y + self.eastYVal
        self.southRect.y = self.rect.y + self.southYVal
        self.westRect.y = self.rect.y + self.westYVal
        self.northRect.x = self.rect.x + self.northXVal
        self.eastRect.x = self.rect.x + self.eastXVal
        self.southRect.x = self.rect.x + self.southXVal
        self.westRect.x = self.rect.x - self.westXVal

    def follow_mc(self):
        # follows the main character around the map
        beforeMovement = (self.rect.x, self.rect.y)
        stuckCounter = False
        if self.bat:
            self.enemyList = bats
            self.enemyLength = len(bats)
        else:
            self.enemyList = enemies
            self.enemyLength = len(enemies)
        if self.rect.x < p.rect.x and self.rect.y == p.rect.y:
            # enemy moves East
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.eastRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.eastRect.colliderect(self.enemyList[i].circleRect):
                        # enemy moves East if unobstructed
                        moveEast += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(self.enemyList[i].circleRect) and not self.eastRect.colliderect(self.enemyList[i].circleRect):
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
                                if not self.northRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.westRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves West as a last resort
                                    moveWest += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        self.rect.x += tempSpeed
                                    else:
                                        self.rect.x -= tempSpeed
                                    # print("UNSTUCK-1")

            if moveEast == self.enemyLength - 1:
                self.travel_east()
            elif moveNorth == self.enemyLength - 1:
                self.travel_north()
            elif moveSouth == self.enemyLength - 1:
                self.travel_south()
            elif moveWest == self.enemyLength - 1:
                self.travel_west()
        if self.rect.x == beforeMovement[0] and self.rect.y == beforeMovement[1]:
            if not self.tempTime:
                self.tempTime = seconds
                self.previousPOS = (self.rect.x, self.rect.y)
            if (seconds - self.tempTime) >= 2:
                if self.rect.x == self.previousPOS[0] and self.rect.y == self.previousPOS[1]:
                    # print("Standing Still")
                    pass
        else:
            self.tempTime = 0
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                else:
                    self.rect.y -= tempSpeed
                self.stuck = False
                stuckCounter = 0
                # print("Stopped Moving!")

        if self.rect.x > p.rect.x and self.rect.y == p.rect.y:
            # enemy moves West
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.westRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.westRect.colliderect(self.enemyList[i].circleRect):
                        # enemy moves West if unobstructed
                        moveWest += 1
                    else:
                        if (self.rect.x - p.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(self.enemyList[i].circleRect) and not self.eastRect.colliderect(self.enemyList[i].circleRect):
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
                                if not self.northRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.eastRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves East as a last resort
                                    moveEast += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        self.rect.x += tempSpeed
                                    else:
                                        self.rect.x -= tempSpeed
                                    # print("UNSTUCK-1")

            if moveWest == self.enemyLength - 1:
                self.travel_west()
            elif moveNorth == self.enemyLength - 1:
                self.travel_north()
            elif moveSouth == self.enemyLength - 1:
                self.travel_south()
            elif moveEast == self.enemyLength - 1:
                self.travel_east()
        if self.rect.x == beforeMovement[0] and self.rect.y == beforeMovement[1]:
            if not self.tempTime:
                self.tempTime = seconds
                self.previousPOS = (self.rect.x, self.rect.y)
            if (seconds - self.tempTime) >= 2:
                if self.rect.x == self.previousPOS[0] and self.rect.y == self.previousPOS[1]:
                    # print("Standing Still")
                    pass
        else:
            self.tempTime = 0
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                else:
                    self.rect.y -= tempSpeed
                self.stuck = False
                stuckCounter = 0
                # print("Stopped Moving!")

        if self.rect.y < p.rect.y and self.rect.x == p.rect.x:
            # enemy moves South
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.southRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.southRect.colliderect(self.enemyList[i].circleRect):
                        # enemy moves South if unobstructed
                        moveSouth += 1
                    else:
                        if (p.rect.y - self.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(self.enemyList[i].circleRect) and not self.westRect.colliderect(self.enemyList[i].circleRect):
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
                                if not self.eastRect.colliderect(self.enemyList[i].circleRect):
                                    moveEast += 1
                                elif not self.westRect.colliderect(self.enemyList[i].circleRect):
                                    moveWest += 1
                                elif not self.northRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves North as a last resort
                                    moveNorth += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        self.rect.y += tempSpeed
                                    else:
                                        self.rect.y -= tempSpeed
                                    # print("UNSTUCK-1")

            if moveSouth == self.enemyLength - 1:
                self.travel_south()
            elif moveEast == self.enemyLength - 1:
                self.travel_east()
            elif moveWest == self.enemyLength - 1:
                self.travel_west()
            elif moveNorth == self.enemyLength - 1:
                self.travel_north()
        if self.rect.x == beforeMovement[0] and self.rect.y == beforeMovement[1]:
            if not self.tempTime:
                self.tempTime = seconds
                self.previousPOS = (self.rect.x, self.rect.y)
            if (seconds - self.tempTime) >= 2:
                if self.rect.x == self.previousPOS[0] and self.rect.y == self.previousPOS[1]:
                    # print("Standing Still")
                    pass
        else:
            self.tempTime = 0
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                else:
                    self.rect.y -= tempSpeed
                self.stuck = False
                stuckCounter = 0
                # print("Stopped Moving!")

        if self.rect.y > p.rect.y and self.rect.x == p.rect.x:
            # enemy moves North
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.northRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.northRect.colliderect(self.enemyList[i].circleRect):
                        # enemy moves North if unobstructed
                        moveNorth += 1
                    else:
                        if (self.rect.y - p.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.eastRect.colliderect(self.enemyList[i].circleRect) and not self.westRect.colliderect(self.enemyList[i].circleRect):
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
                                if not self.eastRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves east
                                    moveEast += 1
                                elif not self.westRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves west
                                    moveWest += 1
                                elif not self.southRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves South as a last resort
                                    moveSouth += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        self.rect.y += tempSpeed
                                    else:
                                        self.rect.y -= tempSpeed
                                    # print("UNSTUCK-1")

            if moveNorth == self.enemyLength - 1:
                self.travel_north()
            elif moveEast == self.enemyLength - 1:
                self.travel_east()
            elif moveWest == self.enemyLength - 1:
                self.travel_west()
            elif moveSouth == self.enemyLength - 1:
                self.travel_south()
        if self.rect.x == beforeMovement[0] and self.rect.y == beforeMovement[1]:
            if not self.tempTime:
                self.tempTime = seconds
                self.previousPOS = (self.rect.x, self.rect.y)
            if (seconds - self.tempTime) >= 2:
                if self.rect.x == self.previousPOS[0] and self.rect.y == self.previousPOS[1]:
                    # print("Standing Still")
                    pass
        else:
            self.tempTime = 0
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                else:
                    self.rect.y -= tempSpeed
                self.stuck = False
                stuckCounter = 0
                # print("Stopped Moving!")

        if self.rect.x < p.rect.x and self.rect.y < p.rect.y:
            # enemy moves South East
            moveSouthEast = 0
            moveNorthEast = 0
            moveSouthWest = 0
            moveNorthWest = 0
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.eastRect.colliderect(p.rect) or self.southRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.eastRect.colliderect(self.enemyList[i].circleRect) and not self.southRect.colliderect(
                            self.enemyList[i].circleRect):
                        # enemy moves South East if unobstructed
                        moveSouthEast += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(
                                    self.enemyList[i].circleRect) and not self.eastRect.colliderect(self.enemyList[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0, 3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    self.rect.y -= 1
                                    moveNorth += 1
                                else:
                                    # enemy moves west
                                    self.rect.x -= 1
                                    moveWest += 1
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.northRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.westRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves West as a last resort
                                    moveWest += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        enemy.rect.y += tempSpeed
                                    else:
                                        enemy.rect.y -= tempSpeed
            if moveSouthEast == self.enemyLength -1:
                self.travel_southeast()
            elif moveNorth == self.enemyLength -1:
                self.travel_north()
            elif moveNorth == self.enemyLength -1:
                self.travel_north()
            elif moveSouth == self.enemyLength -1:
                self.travel_east()
            elif moveWest == self.enemyLength -1:
                self.travel_west()
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                    self.rect.x -= tempSpeed
                else:
                    self.rect.y -= tempSpeed
                    self.rect.x += tempSpeed
                self.stuck = False
                stuckCounter = 0

        if self.rect.x > p.rect.x and self.rect.y < p.rect.y:
            # enemy moves South West
            moveSouthEast = 0
            moveNorthEast = 0
            moveSouthWest = 0
            moveNorthWest = 0
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.westRect.colliderect(p.rect) or self.southRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.westRect.colliderect(self.enemyList[i].circleRect) and not self.southRect.colliderect(
                            self.enemyList[i].circleRect):
                        # enemy moves South West if unobstructed
                        moveSouthWest += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(
                                    self.enemyList[i].circleRect) and not self.eastRect.colliderect(self.enemyList[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0, 3)
                                if randomDirection <= 1:
                                    # enemy moves North
                                    self.rect.y -= 1
                                    moveNorth += 1
                                else:
                                    # enemy moves east
                                    self.rect.x += 1
                                    moveEast += 1
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.northRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.westRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves West as a last resort
                                    moveWest += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        enemy.rect.y += tempSpeed
                                    else:
                                        enemy.rect.y -= tempSpeed
            if moveSouthWest == self.enemyLength -1:
                self.travel_southwest()
            elif moveNorth == self.enemyLength -1:
                self.travel_north()
            elif moveNorth == self.enemyLength -1:
                self.travel_north()
            elif moveSouth == self.enemyLength -1:
                self.travel_east()
            elif moveWest == self.enemyLength -1:
                self.travel_west()
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                    self.rect.x -= tempSpeed
                else:
                    self.rect.y -= tempSpeed
                    self.rect.x += tempSpeed
                self.stuck = False
                stuckCounter = 0

        if self.rect.x < p.rect.x and self.rect.y > p.rect.y:
            # enemy moves North East
            moveSouthEast = 0
            moveNorthEast = 0
            moveSouthWest = 0
            moveNorthWest = 0
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.eastRect.colliderect(p.rect) or self.northRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.eastRect.colliderect(self.enemyList[i].circleRect) and not self.northRect.colliderect(
                            self.enemyList[i].circleRect):
                        # enemy moves North East if unobstructed
                        moveNorthEast += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(
                                    self.enemyList[i].circleRect) and not self.eastRect.colliderect(self.enemyList[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0, 3)
                                if randomDirection <= 1:
                                    # enemy moves west
                                    self.rect.x -= 1
                                    moveWest += 1
                                else:
                                    # enemy moves South
                                    self.rect.y += 1
                                    moveSouth += 1
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.northRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.westRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves West as a last resort
                                    moveWest += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        enemy.rect.y += tempSpeed
                                    else:
                                        enemy.rect.y -= tempSpeed
            if moveNorthEast == self.enemyLength -1:
                self.travel_northeast()
            elif moveNorth == self.enemyLength -1:
                self.travel_south()
            elif moveNorth == self.enemyLength -1:
                self.travel_north()
            elif moveWest == self.enemyLength -1:
                self.travel_west()
            elif moveSouth == self.enemyLength -1:
                self.travel_east()
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                    self.rect.x -= tempSpeed
                else:
                    self.rect.y -= tempSpeed
                    self.rect.x += tempSpeed
                self.stuck = False
                stuckCounter = 0

        if self.rect.x > p.rect.x and self.rect.y > p.rect.y:
            # enemy moves North West
            moveSouthEast = 0
            moveNorthEast = 0
            moveSouthWest = 0
            moveNorthWest = 0
            moveNorth = 0
            moveEast = 0
            moveSouth = 0
            moveWest = 0
            stuckCounter = 0
            for i in range(self.enemyLength):
                # iterate through each enemy
                if self.westRect.colliderect(p.rect) or self.northRect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemyList[i].rect.x and self.rect.y == self.enemyList[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuckCounter += 1
                else:
                    if not self.westRect.colliderect(self.enemyList[i].circleRect) and not self.northRect.colliderect(
                            self.enemyList[i].circleRect):
                        # enemy moves North West if unobstructed
                        moveNorthWest += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.northRect.colliderect(
                                    self.enemyList[i].circleRect) and not self.eastRect.colliderect(self.enemyList[i].circleRect):
                                # if enemy can go both North and South, pick a random direction
                                randomDirection = random.randint(0, 3)
                                if randomDirection <= 1:
                                    # enemy moves east
                                    self.rect.x += 1
                                    moveEast += 1
                                else:
                                    # enemy moves South
                                    self.rect.y += 1
                                    moveSouth += 1
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.northRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves North
                                    moveNorth += 1
                                elif not self.southRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves South
                                    moveSouth += 1
                                elif not self.westRect.colliderect(self.enemyList[i].circleRect):
                                    # enemy moves West as a last resort
                                    moveWest += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    tempSpeed = random.uniform(0.1, 1)
                                    if tempSpeed < .5:
                                        enemy.rect.y += tempSpeed
                                    else:
                                        enemy.rect.y -= tempSpeed
            if moveNorthWest == self.enemyLength -1:
                self.travel_northwest()
            elif moveNorth == self.enemyLength -1:
                self.travel_north()
            elif moveNorth == self.enemyLength -1:
                self.travel_north()
            elif moveSouth == self.enemyLength -1:
                self.travel_east()
            elif moveWest == self.enemyLength -1:
                self.travel_west()
        if stuckCounter:
            if stuckCounter > 1:
                # Helps enemies become unstuck on each other
                # print("STUCKCOUNTER!!!")
                tempSpeed = random.uniform(0.1, 1)
                if tempSpeed < .5:
                    self.rect.y += tempSpeed
                    self.rect.x -= tempSpeed
                else:
                    self.rect.y -= tempSpeed
                    self.rect.x += tempSpeed
                self.stuck = False
                stuckCounter = 0

    def attack_mc(self):
        pass


class Bat(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = batImg1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 40
        self.health = 215
        #self.speed = random.uniform(.6, .8)
        self.speed = .8
        self.follow_mc()
        self.travel_southeast()
        self.travel_southwest()
        self.travel_northwest()
        self.travel_northeast()
        self.travel_north()
        self.travel_east()
        self.travel_south()
        self.travel_west()
        self.bat = True

#First mini Boss clas code \/
class miniee(Enemy):
    #Earth Elemental Miniboss
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = minibee1.get_rect().scale_by(1,1)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 20
        self.health = 2500
        self.speed = 3
        self.travel_southeast()
        self.travel_southwest()
        self.travel_northwest()
        self.travel_northeast()
        self.travel_north()
        self.travel_east()
        self.travel_south()
        self.travel_west()
        self.mini = True
        self.felled = False
        self.activate = False
        self.notattacking = True
        self.isattacking = False
        self.attack_timer = 0
        self.lastatt = 0
        self.attackdur = 3
        self.attackarea = None
        self.attackrect = None
        self.rumblearea = None
        self.aoestart = 0
        self.rumblespeed = 0
        self.hitdamage = 25
        self.animation = 0
        self.lastauto = 0
        self.attackspeed = 2
        self.speedsnap = False

    def follow_mc(self):
        #Miniboss movment
        if self.rect.x < p.rect.x and self.rect.y == p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_east()
        elif self.rect.x > p.rect.x and self.rect.y == p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_west()
        elif self.rect.y < p.rect.y and self.rect.x == p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_south()
        elif self.rect.y > p.rect.y and self.rect.x == p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_north()
        elif self.rect.x < p.rect.x and self.rect.y < p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_southeast()
        elif self.rect.x > p.rect.x and self.rect.y < p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_southwest()
        elif self.rect.x < p.rect.x and self.rect.y > p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_northeast()
        elif self.rect.x > p.rect.x and self.rect.y > p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_northwest()
    def aoehit(self):
        calctargets.calcdistance(self)
        if calctargets.calcdistance(self) <= 80 and self.notattacking == True and (int(self.attack_timer) - self.lastatt >= 12):
            self.lastatt = int(self.attack_timer)
            self.notattacking = False
            self.isattacking = True
            #print("attacking")
            self.aoestart = int(self.attack_timer)
            p.orspeed = p.speed
            self.rumblespeed = (p.speed*.55)
        if self.isattacking == True:
            self.attackarea = pygame.draw.circle(screen, (252, 161, 3), (self.rect.x+18, self.rect.y+20), 240 , 1)
            self.rumblearea = pygame.draw.circle(screen, (209, 10, 10), (self.rect.x + 18, self.rect.y + 20), ((self.attack_timer - self.aoestart)*80),1)
            if p.rect.colliderect(self.rumblearea):
                p.speed = self.rumblespeed
            else:
                p.speed = p.orspeed
            if (int(self.attack_timer) == (self.lastatt + self.attackdur)):
                self.attacrect = self.attackarea = pygame.draw.circle(screen, (209, 10, 10), (self.rect.x+18, self.rect.y+20), 240, 1)
                if p.rect.colliderect(self.attacrect):
                    p.health -= 50
                    # print("Player hit")
                    # print(p.health)
            if (int(self.attack_timer) == (self.lastatt + self.attackdur)):
                self.notattacking = True
                self.isattacking = False
                self.attackarea = None
                self.attackrect = None
                p.speed = p.orspeed

    def autohitplayer(self):
        if self.rect.colliderect(p.rect) and (self.attack_timer - self.lastauto) >=self.attackspeed:
            self.lastauto = self.attack_timer
            p.health -= self.hitdamage
            #print("player hit")


class skeletonKing(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = batImg1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 40
        self.midBoxRect = pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.rect.x+122,self.rect.y+85,20,20))
        self.health = 5000
        self.speed = 2
        self.skeletonKing = True
        self.xCoord = 0
        self.yCoord = 0
        # self.legRectEven = None
        # self.legRectEvenRight = None
        # self.legRectOddLeft = None
        # self.legRectOddRight = None
        self.leftLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+50,self.rect.y+170,20,10))
        self.rightLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+226,self.rect.y+190,22,10))
        self.animationImage = 0
        self.mainLeftLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+17,self.rect.y+188,22,12))
        self.mainRightLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+226,self.rect.y+190,22,10))
        self.runActivation = False
        self.runCounter = 0
        self.animationInterval = 8
        self.runTarget = ()
        self.targetAquired = False
        self.felled = False
        self.activate = False


    def generate_enemy(self):
        # print('1')
        # self.legRectEvenLeft = pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.rect.x+17,self.rect.y+188,22,12))
        # self.legRectEvenRight = pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.rect.x+185,self.rect.y+170,18,10))
        # self.legRectOddLeft = pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.rect.x+50,self.rect.y+170,35,12))
        # self.legRectOddRight = pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.rect.x+226,self.rect.y+191,22,10))
        # pygame.draw.rect(screen, (0,255,0), p.rect)
        # self.legRectEven = pygame.draw.rect(screen, (255,0,0), (255,4))
        if not self.spawned:
            # print('2')
            self.xCoord = random.randint(-340, 990)
            self.yCoord = random.randint(-340, 990)
            while (abs(self.xCoord - p.rect.x) < 30 and abs(self.yCoord - p.rect.y) < 30) or (250 <= self.xCoord <= 550 and 250 <= self.yCoord <= 550) or self.xCoord < m.leftBoundaryX or self.xCoord > m.rightBoundaryX or self.yCoord < m.topBoundaryY or self.yCoord > m.bottomBoundaryY or abs(self.xCoord - m.leftBoundaryX) < 75 or abs(self.xCoord - m.rightBoundaryX) < 75 or abs(self.yCoord - m.topBoundaryY) < 75 or abs(self.yCoord - m.bottomBoundaryY) < 75:
                self.xCoord = random.randint(-340, 990)
                self.yCoord = random.randint(-340, 990)
                # print("AHHHHHH")

            self.rect.x = self.xCoord
            self.rect.y = self.yCoord
            self.spawned.append(1)
        else:
            # print('3')
            # if self.runCounter > 100:
            # print(abs(self.rect.x - p.rect.x), abs(self.rect.y - p.rect.y))
            if p.rect.x > self.midBoxRect.x:
                if abs(self.mainRightLegRect.x - p.rect.x) >= 300 or abs(self.mainRightLegRect.y - p.rect.y) >= 300 or (abs(self.mainRightLegRect.x - p.rect.x) + abs(self.mainRightLegRect.y - p.rect.y)) > 400:
                    if not self.targetAquired:
                        self.runTarget = (p.rect.x, p.rect.y)
                        self.targetAquired = True
                    self.runCounter += 1
                    self.speed = 7
                    self.animationInterval = 3
            if p.rect.x < self.midBoxRect.x:
                if abs(self.mainLeftLegRect.x - p.rect.x) >= 300 or abs(self.mainLeftLegRect.y - p.rect.y) >= 300 or (abs(self.mainLeftLegRect.x - p.rect.x) + abs(self.mainLeftLegRect.y - p.rect.y)) > 400:
                    if not self.targetAquired:
                        self.runTarget = (p.rect.x, p.rect.y)
                        self.targetAquired = True
                    self.runCounter += 1
                    self.speed = 7
                    self.animationInterval = 3
            if self.runCounter > 50 or self.rect.colliderect(p.rect):
                self.targetAquired = False
                self.runTarget = ()
                self.runCounter = 0
                self.speed = 1
                self.animationInterval = 15
            if self.animation <= self.animationInterval:
                screen.blit(skeletonKing1, (self.rect.x-30, self.rect.y-75))
                self.leftLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+50,self.rect.y+170,20,10))
                self.rightLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+226,self.rect.y+190,22,10))
                self.animation += 1
                self.animationImage = 1
            elif self.animation <= self.animationInterval * 2:
                screen.blit(skeletonKing2, (self.rect.x-30, self.rect.y-75))
                self.leftLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+17,self.rect.y+188,22,12))
                self.rightLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+185,self.rect.y+170,18,10))
                self.animation += 1
                self.animationImage = 2
            elif self.animation <= self.animationInterval * 3:
                screen.blit(skeletonKing3, (self.rect.x-30, self.rect.y-75))
                self.leftLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+66,self.rect.y+170,20,10))
                self.rightLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+226,self.rect.y+191,22,10))
                self.animation += 1
                self.animationImage = 3
            elif self.animation <= self.animationInterval * 4:
                screen.blit(skeletonKing4, (self.rect.x-30, self.rect.y-75))
                self.leftLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+17,self.rect.y+188,22,12))
                self.rightLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+185,self.rect.y+170,18,10))
                self.animation += 1
                self.animationImage = 4
            elif self.animation > self.animationInterval * 4:
                screen.blit(skeletonKing1, (self.rect.x-30, self.rect.y-75))
                self.animation = 1
                self.animationImage = 1
            self.rect.height = 195
            self.rect.width = 265
            self.midBoxRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+122,self.rect.y+85,20,20))
            self.mainLeftLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+17,self.rect.y+188,22,12))
            self.mainRightLegRect = pygame.draw.rect(transparentSurface, (255,0,0), pygame.Rect(self.rect.x+226,self.rect.y+190,22,10))

            # pygame.draw.rect(screen, (125,125,125), self.rect)
            # pygame.draw.rect(screen, (128,0,128), self.northRect)
            # pygame.draw.rect(screen, (128,0,128), self.eastRect)
            # pygame.draw.rect(screen, (128,0,128), self.southRect)
            # pygame.draw.rect(screen, (128,0,128), self.westRect)
        self.follow_mc()
        self.runCounter += 1


    def follow_mc(self):

        # if not self.rect.colliderect(p.rect):
        if self.mainRightLegRect.x < p.rect.x+12:
            # if player is to the right of main right leg
            self.rect.x += self.speed
        elif p.rect.x+12 > self.midBoxRect.x and p.rect.x+12 < self.mainRightLegRect.x:
            self.rect.x -= self.speed
        if self.mainRightLegRect.y != p.rect.y+13:
            if self.mainRightLegRect.y < p.rect.y+13:
                # if the player is to the south of the enemy
                self.rect.y += self.speed
            if self.mainRightLegRect.y > p.rect.y+13:
                # if the player is to the north of the enemy
                self.rect.y -= self.speed

        if self.mainLeftLegRect.x > p.rect.x+12:
            self.rect.x -= self.speed
        elif p.rect.x+12 <= self.midBoxRect.x and p.rect.x+12 > self.mainLeftLegRect.x:
            self.rect.x += self.speed
        if self.mainLeftLegRect.y != p.rect.y+13:
            if self.mainLeftLegRect.y < p.rect.y+13:
                # if the player is to the south of the enemy
                self.rect.y += self.speed
            if self.mainLeftLegRect.y > p.rect.y+13:
                # if the player is to the north of the enemy
                self.rect.y -= self.speed

    def attack(self):
        # pygame.draw.rect(screen, (140,38,28), enemy.midDotRect)
        for enemy in enemies:
            if self.leftLegRect.colliderect(enemy.midDotRect) or self.rightLegRect.colliderect(enemy.midDotRect):
                    if enemy in enemies:
                        enemies.remove(enemy)
                        # print("ENEMY REMOVED!!!")
                        # print("----------------")
            if self.leftLegRect.colliderect(p.rect) or self.rightLegRect.colliderect(p.rect):
                p.health -= 24


class XP(pygame.sprite.Sprite):
    # Controls the location of the XP and the XP hitbox
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = pygame.draw.circle(transparentSurface, (0,255,0), (x, y), 5)
        self.hitBoxRect = pygame.draw.circle(transparentSurface, (0,255,35), (x, y), 50)

    def xp_stationary(self):
        # Displays XP in a specific location
        self.rect = pygame.draw.circle(screen, (0,255,0), (self.x, self.y), 5)
        self.hitBoxRect = pygame.draw.circle(transparentSurface, (0,255,35), (self.x, self.y), 50)


class XP_Bar(pygame.sprite.Sprite):
    # Displays the XP Bar
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
        # displays XP bar
        self.xpBarBorderRect = pygame.draw.line(screen, (0,0,0), (90-self.offset,770), (710-self.offset, 770), 45)
        if self.xp:
            self.length = self.xp / self.level_xp_requirement
            if self.length >= 1 or self.length+self.leftover >= 1:
                # if player XP reached level requirement, increase XP level
                self.leftover = self.xp - self.level_xp_requirement
                self.level += 1
                self.xp = 0
                self.level_xp_requirement *= 1.25
                self.length = self.xp / self.level_xp_requirement
                if self.leftover:
                    # if any leftover XP from previous level, add it to the new level
                    self.leftoverSize = (((1 / self.level_xp_requirement)*self.total_length)*self.leftover)
                    self.xpBarRect = pygame.draw.line(screen, (28,36,192), (100-self.offset,770), (self.leftoverSize+100-self.offset, 770), 25)
                    self.leftover = 0
            else:
                self.xpBarRect = pygame.draw.line(screen, (28,36,192), (100-self.offset,770), ((self.total_length*self.length)+self.leftoverSize+100-self.offset, 770), 25)
                self.xpBarEmptyRect = pygame.draw.line(screen, (255,255,255), ((self.total_length*self.length)+self.leftoverSize+100-self.offset,770), (700-self.offset, 770), 25)
        else:
            # Displays if player has zero XP
            self.xpBarRect = pygame.draw.line(screen, (28,36,192), (100-self.offset,770), (self.leftoverSize+100-self.offset, 770), 25)
            self.xpBarEmptyRect = pygame.draw.line(screen, (255,255,255), (self.leftoverSize+100-self.offset,770), (700-self.offset, 770), 25)

        # Displays level number
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
            # moves the level number to the left to better accommodate another value fitting into the box
            screen.blit(levelRender, (747-self.offset, 758))


# initializes the Player and Enemy classes
p = Player()
m = Map()
b = Bullet()
ee = miniee(0,0)
sk = skeletonKing(0,0)
xpB = XP_Bar()
ba = BasicAttack()
enemies = []
bats = []
bullets = []
bup = Bullet_Upgrade()

# bullets = [Bullet() for _ in range(1)]

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
bg_img = pygame.image.load('images/dungeon.png').convert_alpha()
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
    gameTimer = font.render(str(text), True, textColor).convert_alpha()
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


    if key_presses[pygame.K_w] and key_presses[pygame.K_d]:
        p.move_northeast()

    elif key_presses[pygame.K_w] and key_presses[pygame.K_a]:
        p.move_northwest()

    elif key_presses[pygame.K_s] and key_presses[pygame.K_d]:
        p.move_southeast()

    elif key_presses[pygame.K_s] and key_presses[pygame.K_a]:
        p.move_southwest()


    elif key_presses[pygame.K_a]:
        # if 'a' is pressed, move left
        p.move_west()
    elif key_presses[pygame.K_LEFT]:
        # if left arrow is pressed, move left
        p.move_west()
        # p.rect.x -= 45

    elif key_presses[pygame.K_d]:
        # if 'd' is pressed, move right
        p.move_east()

    elif key_presses[pygame.K_RIGHT]:
        # if right arrow is pressed, move right
        p.move_east()
        # p.rect.x += 45

    elif key_presses[pygame.K_w]:
        # if 'w' is pressed, move up
        p.move_north()
    elif key_presses[pygame.K_UP]:
        # if up arrow is pressed, move up
        p.move_north()
        # p.rect.y -= 45

    elif key_presses[pygame.K_s]:
        # if 's' is pressed, move down
        p.move_south()
    elif key_presses[pygame.K_DOWN]:
        # if down arrow is pressed, move down
        p.move_south()
        # p.rect.y += 45

    if key_presses[pygame.K_ESCAPE]:
        # if ESC key is pressed, pause game
        pauseGame()
    #if key_presses[pygame.K_SPACE]:
        # Dash maybe

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
    # screen.blit(pygame.transform.scale(bg_img, (2250, 2250)), (-800 - m.cameraX, -800 - m.cameraY))
    screen.blit(bg_img,(-800 - m.cameraX, -800 - m.cameraY))

    for x in xp:
        # constantly display the XP
        x.xp_stationary()
        if x.hitBoxRect.colliderect(p.rect):
            # if player is in range of XP, add it to xp_hit list
            xp_hit.append(x)
            x.xp_stationary()

    for x in xp_hit:
        # for every xp the player has gone near, have the XP fly to the player
        if abs(x.rect.x - p.rect.x) < 35 and abs(x.rect.y - p.rect.y) < 35:
            # remove the XP from the world and increase player XP
            if x in xp:
                xp.remove(x)
                xpB.xp += 1
            if x in xp_hit:
                xp_hit.remove(x)
        else:
            # have the XP fly to the Player
            if x.rect.x+18 < p.rect.x:
                x.x += p.speed
            if x.rect.x+18 > p.rect.x:
                x.x -= p.speed
            if x.rect.y+18 < p.rect.y:
                x.y += p.speed
            if x.rect.y+18 > p.rect.y:
                x.y -= p.speed

    # makes the main character visible
    screen.blit(pygame.transform.scale(mc_img, (40, 35)), (p.rect.x, p.rect.y))
    if b.shooting == True:
        bulletTimer2 = (pygame.time.get_ticks() / 1000) - b.overflow
    # if bulletTimer1
    if b.shooting == True:
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


    if len(enemies) < 15:
        xCoord = random.randint(-340, 990)
        yCoord = random.randint(-340, 990)
        enemy_length = len(enemies)
        count = 0
        for enemy in enemies:
            while xCoord == enemy.rect.x or yCoord == enemy.rect.y or (abs(xCoord - enemy.rect.x) < 30 and abs(yCoord - enemy.rect.y) < 30) or (250 <= xCoord <= 550 and 250 <= yCoord <= 550) or xCoord < m.leftBoundaryX or xCoord > m.rightBoundaryX or yCoord < m.topBoundaryY or yCoord > m.bottomBoundaryY or abs(xCoord - m.leftBoundaryX) < 25 or abs(xCoord - m.rightBoundaryX) < 25 or abs(yCoord - m.topBoundaryY) < 25 or abs(yCoord - m.bottomBoundaryY) < 25:
                xCoord = random.randint(-340, 990)
                yCoord = random.randint(-340, 990)
        enemies.append(Enemy(xCoord, yCoord))

    if len(bats) < 8:
        xCoord = random.randint(-340, 990)
        yCoord = random.randint(-340, 990)
        bat_length = len(bats)
        count = 0
        for bat in bats:
            while xCoord == bat.rect.x or yCoord == bat.rect.y or (abs(xCoord - bat.rect.x) < 30 and abs(yCoord - bat.rect.y) < 30) or (250 <= xCoord <= 550 and 250 <= yCoord <= 550) or xCoord < m.leftBoundaryX or xCoord > m.rightBoundaryX or yCoord < m.topBoundaryY or yCoord > m.bottomBoundaryY or abs(xCoord - m.leftBoundaryX) < 25 or abs(xCoord - m.rightBoundaryX) < 25 or abs(yCoord - m.topBoundaryY) < 25 or abs(yCoord - m.bottomBoundaryY) < 25:
                xCoord = random.randint(-340, 990)
                yCoord = random.randint(-340, 990)
        bats.append(Bat(xCoord, yCoord))

    for enemy in enemies:
        # go through each enemy and control the spawning and movements
        if not enemy.spawned:
            # enemy.spawnTimer = pygame.time.get_ticks()
            pygame.draw.circle(screen, (128,0,32), (enemy.rect.x, enemy.rect.y), 16)
            enemy.spawnTimer += 1
            if enemy.spawnTimer >= 75:
                enemy.spawned.append(1)
                enemy.spawnIndicator = None
                # screen.blit(pygame.transform.scale(enemy1, (35, 30)), (enemy.rect.x, enemy.rect.y))
                # enemy.generate_enemy()
                # enemy.follow_mc()
                # enemy.spawnTimer = 0
        else:
            if enemy.animation <= 15:
                screen.blit(pygame.transform.scale(enemy4, (45, 40)), (enemy.rect.x-6, enemy.rect.y-6))
                enemy.animation += 1

            elif enemy.animation <= 30:
                screen.blit(pygame.transform.scale(enemy3, (45, 40)), (enemy.rect.x-6, enemy.rect.y-6))
                enemy.animation += 1

            elif enemy.animation <= 45:
                screen.blit(pygame.transform.scale(enemy2, (45, 40)), (enemy.rect.x-6, enemy.rect.y-6))
                enemy.animation += 1

            elif enemy.animation <= 60:
                screen.blit(pygame.transform.scale(enemy1, (45, 40)), (enemy.rect.x-6, enemy.rect.y-6))
                enemy.animation += 1

            elif enemy.animation > 60:
                screen.blit(pygame.transform.scale(enemy4, (45, 40)), (enemy.rect.x-6, enemy.rect.y-6))
                enemy.animation = 1

            # screen.blit(pygame.transform.scale(enemyOriginal, (45, 40)), (enemy.rect.x, enemy.rect.y))
            enemy.circleRect = pygame.draw.circle(transparentSurface, (0, 50, 0, 100), (enemy.rect.x+18, enemy.rect.y + 17), 10)
            enemy.midDotRect = pygame.draw.circle(transparentSurface, (0, 50, 0, 100), (enemy.rect.x + 16, enemy.rect.y + 16), 8)
            enemy.generate_enemy()
            enemy.follow_mc()
            # pygame.draw.rect(screen, (255,0,0), enemy.rect)
            # pygame.draw.rect(screen, (255,0,0), enemy.midDotRect)
            # pygame.draw.rect(screen, (128,0,128), enemy.northRect)
            # pygame.draw.rect(screen, (128,0,128), enemy.eastRect)
            # pygame.draw.rect(screen, (128,0,128), enemy.southRect)
            # pygame.draw.rect(screen, (128,0,128), enemy.westRect)


            if b.shooting == True:
                for bullet in bullets:
                    # for each active bullet, if the bullet hits an enemy, deal damage if appropriate conditions met.
                    if enemy.rect.colliderect(bullet.rect) and bullet.bulletValid:
                        if not enemy.bulletCollisions:
                            # if the enemy has encountered it's first bullet, add to the list and take damage
                            enemy.bulletCollisions.append(bullet)
                            enemy.health -= p.bulletdamage
                        elif enemy.bulletCollisions:
                            # if the list of bullets the enemy has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                            i = 0
                            for l in enemy.bulletCollisions:
                                if bullet.rect.x == enemy.bulletCollisions[i].rect.x and bullet.rect.y == enemy.bulletCollisions[i].rect.y:
                                    pass
                                elif bullet not in enemy.bulletCollisions and bullet.bulletValid:
                                    enemy.bulletCollisions.append(bullet)
                                    enemy.health -= p.bulletdamage
                                i += 1

            if enemy.rect.colliderect(ba.hitBoxRect) and ba.running and not enemy.meleeAttackCollisions:
                # Reduce enemy health from the Players basic attack if not hit by that same attack swing
                enemy.health -= p.meleedamage
                enemy.meleeAttackCollisions.append(1)

            if sk.activate and not sk.felled:
                if sk.rect.colliderect(ba.hitBoxRect) and ba.running and not sk.meleeAttackCollisions:
                    sk.health -= p.meleedamage
                    sk.meleeAttackCollisions.append(1)
            if ee.activate and not ee.felled:
                if ee.rect.colliderect(ba.hitBoxRect) and ba.running and not ee.meleeAttackCollisions:
                    # Reduce health from the mini boss from Players basic attack if not hit by that same attack swing
                    ee.health -= p.meleedamage + 10000
                    ee.meleeAttackCollisions.append(1)

        if enemy.health <= 0:
            # despawns the enemy if their health is 0 or below
            xp.append(XP(enemy.rect.x+18, enemy.rect.y+17))
            if enemy in enemies:
                enemies.remove(enemy)
            chance = random.randint(1,10)
            if chance <= 2:
                p.gold += 1

        if enemy.rect.colliderect(p.rect) or enemy.northRect.colliderect(p.rect) or enemy.eastRect.colliderect(p.rect) or enemy.southRect.colliderect(p.rect) or enemy.westRect.colliderect(p.rect):
            # print("COLLIDE!!!")
            p.health -= 1

    for bat in bats:
        if not bat.spawned:
            pygame.draw.circle(screen, (160,85,150), (bat.rect.x, bat.rect.y), 16)
            bat.spawnTimer += 1
            if bat.spawnTimer >= 75:
                    bat.spawned.append(1)
                    bat.spawnIndicator = None
        else:
            if bat.animation <= 15:
                screen.blit(pygame.transform.scale(batImg1, (45, 40)), (bat.rect.x-2, bat.rect.y+5))
                bat.animation += 1

            elif bat.animation <= 30:
                screen.blit(pygame.transform.scale(batImg2, (45, 40)), (bat.rect.x-2, bat.rect.y+5))
                bat.animation += 1

            elif bat.animation > 30:
                screen.blit(pygame.transform.scale(batImg1, (45, 40)), (bat.rect.x-2, bat.rect.y+5))
                bat.animation = 1

            bat.circleRect = pygame.draw.circle(transparentSurface, (0, 50, 0, 100), (bat.rect.x+18, bat.rect.y + 17), 10)
            bat.midDotRect = pygame.draw.circle(transparentSurface, (0, 50, 0, 100), (bat.rect.x + 16, bat.rect.y + 16), 1)
            # bat.generate_enemy()
            bat.follow_mc()

            if b.shooting == True:
                for bullet in bullets:
                    # for each active bullet, if the bullet hits a bat, deal damage if appropriate conditions met.
                    if bat.rect.colliderect(bullet.rect) and bullet.bulletValid:
                        if not bat.bulletCollisions:
                            # if the bat has encountered it's first bullet, add to the list and take damage
                            bat.bulletCollisions.append(bullet)
                            bat.health -= p.bulletdamage
                        elif bat.bulletCollisions:
                            # if the list of bullets the bat has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                            i = 0
                            for l in bat.bulletCollisions:
                                if bullet.rect.x == bat.bulletCollisions[i].rect.x and bullet.rect.y == bat.bulletCollisions[i].rect.y:
                                    pass
                                elif bullet not in bat.bulletCollisions and bullet.bulletValid:
                                    bat.bulletCollisions.append(bullet)
                                    bat.health -= p.bulletdamage
                                i += 1

            if bat.rect.colliderect(ba.hitBoxRect) and ba.running and not bat.meleeAttackCollisions:
                # Reduce bat health from the Players basic attack if not hit by that same attack swing
                bat.health -= p.meleedamage
                bat.meleeAttackCollisions.append(1)

        if bat.health <= 0:
            # despawns the bat if their health is 0 or below
            xp.append(XP(bat.rect.x+18, bat.rect.y+17))
            if bat in bats:
                bats.remove(bat)
            chance = random.randint(1,10)
            if chance <= 2:
                p.gold += 1

        if bat.rect.colliderect(p.rect) or bat.northRect.colliderect(p.rect) or bat.eastRect.colliderect(p.rect) or bat.southRect.colliderect(p.rect) or bat.westRect.colliderect(p.rect):
            # print("COLLIDE!!!")
            p.health -= 1
#First mini boss section \/
    if int(minutes) == 0 and int(seconds) == 0:
        ee.activate = True
    if ee.activate and not ee.felled:
        ee.attack_timer = (pygame.time.get_ticks() / 1000)
        ee.aoehit()
        bup.rect.x = ee.rect.x
        bup.rect.y = ee.rect.y
        if ee.animation<=15:
            screen.blit(pygame.transform.scale(minibee1, (40,45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        elif ee.animation<=30:
            screen.blit(pygame.transform.scale(minibee2, (40,45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        elif ee.animation<=45:
            screen.blit(pygame.transform.scale(minibee3, (40,45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        elif ee.animation<=60:
            screen.blit(pygame.transform.scale(minibee4, (40,45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        if ee.animation == 60:
            ee.animation = 0
        if ee.notattacking == True:
            ee.follow_mc()
            ee.autohitplayer()
    if ee.activate and not ee.felled:
        if b.shooting == True:
            for bullet in bullets:
                # for each active bullet, if the bullet hits ee, deal damage if appropriate.
                if ee.rect.colliderect(bullet.rect) and bullet.bulletValid:

                    if not ee.bulletCollisions:
                        # If ee has been hit by its first bullet add to list to take damage.
                        ee.bulletCollisions.append(bullet)
                        ee.health -= p.bulletdamage + 100
                        # print(ee.health)
                        # print('1')
                    elif ee.bulletCollisions:
                        # if the list of bullets that have collided ee is greater than 0, make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in ee.bulletCollisions:
                            if bullet.rect.x == ee.bulletCollisions[i].rect.x and bullet.rect.y == ee.bulletCollisions[i].rect.y:
                                pass
                            elif bullet not in ee.bulletCollisions and bullet.bulletValid:
                                ee.bulletCollisions.append(bullet)
                                ee.health -= p.bulletdamage + 100
                                #print(ee.health)
                            i += 1
            for bullet in bullets:
                # removes expired bullets
                if bullet in ee.bulletCollisions and not ee.rect.colliderect(bullet.rect):
                    ee.bulletCollisions.remove(bullet)
            if ee.bulletCollisions:
                # backup to remove expired bullets from the bullet collision list
                for g in ee.bulletCollisions:
                    if not g.rect.colliderect(ee.rect):
                        ee.bulletCollisions.remove(g)
    if ee.health <= 0:
    # Makes sure ee is actually dead
        ee.felled = True
        ee.activate = False
    if ee.felled and bup.upgradeactive == False:
        bup.upgradeout = True
        if p.orspeed > p.speed:
            p.speed = p.orspeed
        if bup.animation<=15:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y))
            bup.animation += 1
        elif bup.animation<=30:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y+5))
            bup.animation += 1
        elif bup.animation<=45:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y+10))
            bup.animation += 1
        elif bup.animation<=60:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y+5))
            bup.animation += 1
        if bup.animation == 60:
            bup.animation = 0
    if p.rect.colliderect(bup.rect) and bup.upgradeactive == False:
        bup.upgradeout = False
        b.shooting = True
        b.overflow = (pygame.time.get_ticks() / 1000)
        bup.upgradeactive = True
        # print(p.bulletdamage)
#End of first mini Boss section



    if int(minutes) == 5 and int(seconds) == 0:
        sk.activate = True
    if sk.activate and not sk.felled:
        sk.generate_enemy()
        sk.attack()

    if sk.activate and not sk.felled:
        if b.shooting == True:
            for bullet in bullets:
                # for each active bullet, if the bullet hits the skeleton king boss, deal damage if appropriate conditions met.
                if sk.rect.colliderect(bullet.rect) and bullet.bulletValid:
                    if not sk.bulletCollisions:
                        # if the skeleton king boss has encountered it's first bullet, add to the list and take damage
                        sk.bulletCollisions.append(bullet)
                        sk.health -= 300
                        # print('1')
                    elif sk.bulletCollisions:
                        # if the list of bullets the skeleton king boss has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in sk.bulletCollisions:
                            if bullet.rect.x == sk.bulletCollisions[i].rect.x and bullet.rect.y == sk.bulletCollisions[i].rect.y:
                                pass
                            elif bullet not in sk.bulletCollisions and bullet.bulletValid:
                                sk.bulletCollisions.append(bullet)
                                sk.health -= 300
                                # print('2')
                            i += 1
            if sk.bulletCollisions:
                # backup to remove expired bullets from the skeleton king boss bullet collision list
                for g in sk.bulletCollisions:
                    if not g.rect.colliderect(sk.rect):
                        sk.bulletCollisions.remove(g)
                        # print("BULLET REMOVED-2")

    if b.shooting == True:
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
            if bullet.rect.x <= m.leftBoundaryX or bullet.rect.x >= m.rightBoundaryX or bullet.rect.y <= m.topBoundaryY or bullet.rect.y >= m.bottomBoundaryY:
                if bullet in bullets:
                    bullets.remove(bullet)

    # print(sk.bulletCollisions)
    # print(sk.health)

    if sk.health <= 0:
        sk.felled = True
        sk.activate = False
        sk.rect = None

    # for bat in bats:
    #     if bat.spawned:
    #         rando = random.randint(1,10)
    #         if rando < 2:
    #             pygame.draw.rect(screen, (255,0,0), bat.rect)
    #             pygame.draw.rect(screen, (128,0,128), bat.northRect)
    #             pygame.draw.rect(screen, (128,0,128), bat.eastRect)
    #             pygame.draw.rect(screen, (128,0,128), bat.southRect)
    #             pygame.draw.rect(screen, (128,0,128), bat.westRect)


    ba.attack()
    m.update_boundary()
    display_timer(gameTimeStr, timerFont, (0, 0, 0))
    display_fps(fps, fpsFont, (0,255,0))
    xpB.show_xp_bar()
    index = 0
    numOfEnemies = len(enemies)
    pygame.display.flip()
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