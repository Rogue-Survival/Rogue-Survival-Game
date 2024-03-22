import sys
import math
import random
import numpy
import pygame


# initializes the pygame library
pygame.init()

# creates the window and dimensions for the game
screen = pygame.display.set_mode((800, 800))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
transparent_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
# sets the window caption at the top
pygame.display.set_caption("Rogue Survival")

# creates variable to control game fps
clock = pygame.time.Clock()
x = pygame.time.get_ticks()

# instantiating a game time string for when the player dies
prevGameTime = 0

# initializing the images of the main character and some enemies
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

skeleton_king1 = pygame.image.load("./images/skeletonking1.png").convert_alpha()
skeleton_king2 = pygame.image.load("./images/skeletonking2.png").convert_alpha()
skeleton_king3 = pygame.image.load("./images/skeletonking3.png").convert_alpha()
skeleton_king4 = pygame.image.load("./images/skeletonking4.png").convert_alpha()

# initializing images of scrolls used for buttons and backgrounds
tallScroll = pygame.image.load("./images/tall.png").convert_alpha()
mediumScroll = pygame.image.load("./images/medium2.png").convert_alpha()
horizontalScroll = pygame.image.load("./images/horizontalScroll.png").convert_alpha()
horizontalScroll = pygame.transform.scale_by(horizontalScroll, 0.3)
buttonScroll = pygame.image.load("./images/buttonScroll.png").convert_alpha()
buttonScroll = pygame.transform.scale_by(buttonScroll, 0.6)

# initializing the dungeon background
dungeonBackground = pygame.image.load("./images/dungeonBackground2.png").convert_alpha()

bullet_upgrade = pygame.image.load("./images/Noodle.png").convert_alpha()

# instantiating pause and gameTime function for later
gameTime = 0
pause = True
# instantiating the XP arrays
xp = []
xp_hit = []


class Map:
    # Controls map boundaries and map camera
    def __init__(self, map_x=-800, map_y=-800):
        self.map_x = map_x
        self.map_y = map_y
        self.cameraX = -140
        self.cameraY = -140
        self.left_boundary_x = -245
        self.left_boundary_y1 = -235
        self.left_boundary_y2 = 1079

        self.right_boundary_x = 1072
        self.right_boundary_y1 = -235
        self.right_boundary_y2 = 1079

        self.top_boundary_x1 = -240
        self.top_boundary_x2 = 1072
        self.top_boundary_y = -230

        self.bottom_boundary_x1 = -240
        self.bottom_boundary_x2 = 1072
        self.bottom_boundary_y = 1073

        self.left_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                              (self.left_boundary_x, self.left_boundary_y1),
                                              (self.left_boundary_x, self.left_boundary_y2), 12)
        self.right_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                               (self.right_boundary_x, self.right_boundary_y1),
                                               (self.right_boundary_x, self.right_boundary_y2), 12)
        self.top_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                             (self.top_boundary_x1, self.top_boundary_y),
                                             (self.top_boundary_x2, self.top_boundary_y), 12)
        self.bottom_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                                (self.bottom_boundary_x1, self.bottom_boundary_y),
                                                (self.bottom_boundary_x2, self.bottom_boundary_y), 12)

    def update_boundary(self):
        # keep the map boundaries updated
        self.left_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                              (self.left_boundary_x, self.left_boundary_y1),
                                              (self.left_boundary_x, self.left_boundary_y2), 12)
        self.right_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                               (self.right_boundary_x, self.right_boundary_y1),
                                               (self.right_boundary_x, self.right_boundary_y2), 12)
        self.top_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                             (self.top_boundary_x1, self.top_boundary_y),
                                             (self.top_boundary_x2, self.top_boundary_y), 12)
        self.bottom_boundary = pygame.draw.line(transparent_surface, (255, 0, 0),
                                                (self.bottom_boundary_x1, self.bottom_boundary_y),
                                                (self.bottom_boundary_x2, self.bottom_boundary_y), 12)


class Player(pygame.sprite.Sprite):
    # Player class controls basic functions relating to the player
    def __init__(self):
        # inherits from the pygame.sprite.Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.health = 5000000
        self.image = "./images/MAIN_CHARACTER.png"
        self.death = False
        self.rect = mc_img.get_rect().scale_by(2, 2)
        self.rect.x = 400
        self.rect.y = 400
        self.rect.width = 40
        self.gold = 0
        self.dodgeChance = 0
        self.death = True
        self.health_font = pygame.font.SysFont('futura', 46)
        self.orspeed = 0
        # self.playerGroup = pygame.sprite.Group()
        # self.playerGroup.add(self.rect)

    def display_health(self):
        # displays health to the screen
        health_string = f"HP: {str(self.health)}"
        health_display = self.health_font.render(health_string, True, (255, 0, 0))
        screen.blit(health_display, (350, 10))

    def move_west(self):
        # moves the player and camera West, while moving every other entity in the opposite direction
        if self.rect.x > m.left_boundary_x + 25:
            # checks if player is within map boundaries
            m.cameraX -= self.speed
            m.left_boundary_x += self.speed
            m.right_boundary_x += self.speed
            m.top_boundary_x1 += self.speed
            m.top_boundary_x2 += self.speed
            m.bottom_boundary_x1 += self.speed
            m.bottom_boundary_x2 += self.speed
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.x += self.speed
                enemy.north_rect.x = enemy.rect.x + enemy.north_x_val
                enemy.east_rect.x = enemy.rect.x + enemy.east_x_val
                enemy.south_rect.x = enemy.rect.x + enemy.south_x_val
                enemy.west_rect.x = enemy.rect.x - enemy.west_x_val
            for bat in bats:
                # moves the bats and associated rects due to the effects of the player camera
                bat.rect.x += self.speed
                bat.north_rect.x = bat.rect.x + bat.north_x_val
                bat.east_rect.x = bat.rect.x + bat.east_x_val
                bat.south_rect.x = bat.rect.x + bat.south_x_val
                bat.west_rect.x = bat.rect.x - bat.west_x_val

                bat.bulletRect.x += self.speed
                if bat.bulletValid:
                    bat.playerPOS[0] += self.speed
                    bat.startingPoint[0] += self.speed
            for x in xp:
                # moves the XP due to the effects of the player camera
                x.x += self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                # moves the skeleton king when spawned in due to the effects of the player camera
                sk.rect.x += self.speed
                sk.north_rect.x = sk.rect.x + sk.north_x_val
                sk.east_rect.x = sk.rect.x + sk.east_x_val
                sk.south_rect.x = sk.rect.x + sk.south_x_val
                sk.west_rect.x = sk.rect.x - sk.west_x_val
            if ee.activate and not ee.felled:
                ee.rect.x += self.speed
                ee.north_rect.x = ee.rect.x + ee.north_x_val
                ee.east_rect.x = ee.rect.x + ee.east_x_val
                ee.south_rect.x = ee.rect.x + ee.south_x_val
                ee.west_rect.x = ee.rect.x - ee.west_x_val
            if bup.upgrade_out:
                bup.rect.x += self.speed

    def move_east(self):
        # moves the player and camera East, while moving every other entity in the opposite direction
        if self.rect.x < m.right_boundary_x - 50:
            # checks if player is within map boundaries
            m.cameraX += self.speed
            # m.left_boundaryY -= self.speed
            m.left_boundary_x -= self.speed
            m.right_boundary_x -= self.speed
            m.top_boundary_x1 -= self.speed
            m.top_boundary_x2 -= self.speed
            m.bottom_boundary_x1 -= self.speed
            m.bottom_boundary_x2 -= self.speed
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.x -= self.speed
                enemy.north_rect.x = enemy.rect.x + enemy.north_x_val
                enemy.east_rect.x = enemy.rect.x + enemy.east_x_val
                enemy.south_rect.x = enemy.rect.x + enemy.south_x_val
                enemy.west_rect.x = enemy.rect.x - enemy.west_x_val
            for bat in bats:
                # moves the bats and associated rects due to the effects of the player camera
                bat.rect.x -= self.speed
                bat.north_rect.x = bat.rect.x + bat.north_x_val
                bat.east_rect.x = bat.rect.x + bat.east_x_val
                bat.south_rect.x = bat.rect.x + bat.south_x_val
                bat.west_rect.x = bat.rect.x - bat.west_x_val

                bat.bulletRect.x -= self.speed
                if bat.bulletValid:
                    bat.playerPOS[0] -= self.speed
                    bat.startingPoint[0] -= self.speed
            for x in xp:
                # moves the XP due to the effects of the player camera
                x.x -= self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                # moves the skeleton king when spawned in due to the effects of the player camera
                sk.rect.x -= self.speed
                sk.north_rect.x = sk.rect.x + sk.north_x_val
                sk.east_rect.x = sk.rect.x + sk.east_x_val
                sk.south_rect.x = sk.rect.x + sk.south_x_val
                sk.west_rect.x = sk.rect.x - sk.west_x_val
            if ee.activate and not ee.felled:
                ee.rect.x -= self.speed
                ee.north_rect.x = ee.rect.x + ee.north_x_val
                ee.east_rect.x = ee.rect.x + ee.east_x_val
                ee.south_rect.x = ee.rect.x + ee.south_x_val
                ee.west_rect.x = ee.rect.x - ee.west_x_val
            if bup.upgrade_out:
                bup.rect.x -= self.speed

    def move_north(self):
        # moves the player and camera North, while moving every other entity in the opposite direction
        if self.rect.y > m.top_boundary_y + 25:
            # checks if player is within map boundaries
            m.cameraY -= self.speed
            m.left_boundary_y1 += self.speed
            m.left_boundary_y2 += self.speed
            m.right_boundary_y1 += self.speed
            m.right_boundary_y2 += self.speed
            m.top_boundary_y += self.speed
            m.bottom_boundary_y += self.speed
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y += self.speed
                enemy.north_rect.y = enemy.rect.y - enemy.north_y_val
                enemy.east_rect.y = enemy.rect.y + enemy.east_y_val
                enemy.south_rect.y = enemy.rect.y + enemy.south_y_val
                enemy.west_rect.y = enemy.rect.y + enemy.west_y_val
            for bat in bats:
                # moves the bats and associated rects due to the effects of the player camera
                bat.rect.y += self.speed
                bat.north_rect.y = bat.rect.y - bat.north_y_val
                bat.east_rect.y = bat.rect.y + bat.east_y_val
                bat.south_rect.y = bat.rect.y + bat.south_y_val
                bat.west_rect.y = bat.rect.y + bat.west_y_val

                bat.bulletRect.y += self.speed
                if bat.bulletValid:
                    bat.playerPOS[1] += self.speed
                    bat.startingPoint[1] += self.speed
            for x in xp:
                # moves the XP due to the effects of the player camera
                x.y += self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                # moves the skeleton king when spawned in due to the effects of the player camera
                sk.rect.y += self.speed
                sk.north_rect.y = sk.rect.y - sk.north_y_val
                sk.east_rect.y = sk.rect.y + sk.east_y_val
                sk.south_rect.y = sk.rect.y + sk.south_y_val
                sk.west_rect.y = sk.rect.y + sk.west_y_val
            if ee.activate and not ee.felled:
                ee.rect.y += self.speed
                ee.north_rect.y = ee.rect.y - ee.north_y_val
                ee.east_rect.y = ee.rect.y + ee.east_y_val
                ee.south_rect.y = ee.rect.y + ee.south_y_val
                ee.west_rect.y = ee.rect.y + ee.west_y_val
            if bup.upgrade_out:
                bup.rect.y += self.speed

    def move_south(self):
        # moves the player and camera South, while moving every other entity in the opposite direction
        if self.rect.y < m.bottom_boundary_y - 50:
            # checks if player is within map boundaries
            m.cameraY += self.speed
            m.left_boundary_y1 -= self.speed
            m.left_boundary_y2 -= self.speed
            m.right_boundary_y1 -= self.speed
            m.right_boundary_y2 -= self.speed
            m.top_boundary_y -= self.speed
            m.bottom_boundary_y -= self.speed
            for enemy in enemies:
                # moves the enemy and associated rects due to the effects of the player camera
                enemy.rect.y -= self.speed
                enemy.north_rect.y = enemy.rect.y - enemy.north_y_val
                enemy.east_rect.y = enemy.rect.y + enemy.east_y_val
                enemy.south_rect.y = enemy.rect.y + enemy.south_y_val
                enemy.west_rect.y = enemy.rect.y + enemy.west_y_val
            for bat in bats:
                # moves the bats and associated rects due to the effects of the player camera
                bat.rect.y -= self.speed
                bat.north_rect.y = bat.rect.y - bat.north_y_val
                bat.east_rect.y = bat.rect.y + bat.east_y_val
                bat.south_rect.y = bat.rect.y + bat.south_y_val
                bat.west_rect.y = bat.rect.y + bat.west_y_val

                bat.bulletRect.y -= self.speed
                if bat.bulletValid:
                    bat.playerPOS[1] -= self.speed
                    bat.startingPoint[1] -= self.speed
            for x in xp:
                # moves the XP due to the effects of the player camera
                x.y -= self.speed
                x.xp_stationary()
            if sk.activate and not sk.felled:
                # moves the skeleton king when spawned in due to the effects of the player camera
                sk.rect.y -= self.speed
                sk.north_rect.y = sk.rect.y - sk.north_y_val
                sk.east_rect.y = sk.rect.y + sk.east_y_val
                sk.south_rect.y = sk.rect.y + sk.south_y_val
                sk.west_rect.y = sk.rect.y + sk.west_y_val
            if ee.activate and not ee.felled:
                ee.rect.y -= self.speed
                ee.north_rect.y = ee.rect.y - ee.north_y_val
                ee.east_rect.y = ee.rect.y + ee.east_y_val
                ee.south_rect.y = ee.rect.y + ee.south_y_val
                ee.west_rect.y = ee.rect.y + ee.west_y_val
            if bup.upgrade_out:
                bup.rect.y -= self.speed


class BasicAttack:
    # Creates Basic Attacks for the Player
    def __init__(self):
        self.rect = None
        self.hitbox_rect = pygame.draw.circle(transparent_surface, (255, 255, 255), (p.rect.x + 19, p.rect.y + 19), 78)

        self.east = False
        self.north_east = False
        self.north = False
        self.north_west = False
        self.west = False
        self.south_west = False
        self.south = False
        self.south_east = False
        self.east_end = False

        self.east_counter = 0
        self.north_east_counter = 0
        self.north_counter = 0
        self.north_west_counter = 0
        self.west_counter = 0
        self.south_west_counter = 0
        self.south_counter = 0
        self.south_east_counter = 0
        self.east_endCounter = 0

        self.running = False
        self.finished = False

        self.damage = 45
        self.basic_attack_timer = 0
        self.timer_target = 40
        self.range_increase = 10
        self.hitbox_radius = 78

    def attack(self):
        # goes through various animations and hitbox creations for basic attacks to hit all enemies
        total_time = pygame.time.get_ticks() / 1000
        self.hitbox_rect = pygame.draw.circle(transparent_surface, (255, 255, 255),
                                              (p.rect.x + 19, p.rect.y + 19), self.hitbox_radius)
        if self.basic_attack_timer > self.timer_target and total_time > 1 and not self.east:
            # start with the sword at the east position and then go in a counter-clockwise direction
            self.running = True
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x + 36, p.rect.y + 17),
                                         (p.rect.x + 80 + self.range_increase, p.rect.y + 17), 6)
            self.east_counter += 1
            if self.east_counter > 2:
                self.rect = None
                self.east = True
        if self.east and not self.north_east:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x + 33, p.rect.y + 4),
                                         (p.rect.x + 60 + self.range_increase, p.rect.y - 22 - self.range_increase), 6)
            self.north_east_counter += 1
            if self.north_east_counter > 2:
                self.rect = None
                self.north_east = True
        if self.north_east and not self.north:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x + 18, p.rect.y - 4),
                                         (p.rect.x + 18, p.rect.y - 44 - self.range_increase), 6)
            self.north_counter += 1
            if self.north_counter > 2:
                self.rect = None
                self.north = True
        if self.north and not self.north_west:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x, p.rect.y + 4),
                                         (p.rect.x - 27 - self.range_increase, p.rect.y - 22 - self.range_increase), 6)
            self.north_west_counter += 1
            if self.north_west_counter > 2:
                self.rect = None
                self.north_west = True
        if self.north_west and not self.west:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x, p.rect.y + 17),
                                         (p.rect.x - 44 - self.range_increase, p.rect.y + 17), 6)
            self.west_counter += 1
            if self.west_counter > 2:
                self.rect = None
                self.west = True
        if self.west and not self.south_west:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x, p.rect.y + 32),
                                         (p.rect.x - 27 - self.range_increase, p.rect.y + 60 + self.range_increase), 6)
            self.south_west_counter += 1
            if self.south_west_counter > 2:
                self.rect = None
                self.south_west = True
        if self.south_west and not self.south:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x + 18, p.rect.y + 32),
                                         (p.rect.x + 18, p.rect.y + 78 + self.range_increase), 6)
            self.south_counter += 1
            if self.south_counter > 2:
                self.rect = None
                self.south = True
        if self.south and not self.south_east:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x + 33, p.rect.y + 32),
                                         (p.rect.x + 64 + self.range_increase, p.rect.y + 60 + self.range_increase), 6)
            self.south_east_counter += 1
            if self.south_east_counter > 2:
                self.rect = None
                self.south_east = True
        if self.south_east and not self.east_end:
            self.rect = pygame.draw.line(screen, (160, 32, 240), (p.rect.x + 36, p.rect.y + 17),
                                         (p.rect.x + 80 + self.range_increase, p.rect.y + 17), 6)
            self.east_endCounter += 1
            if self.east_endCounter > 1:
                self.rect = None
                self.east_end = True
                self.running = False
                self.finished = True

        if self.basic_attack_timer > self.timer_target + (self.timer_target * 2) and self.east:
            # reset basic attack variables if the basic attack finished
            self.east = False
            self.north_east = False
            self.north = False
            self.north_west = False
            self.west = False
            self.south_west = False
            self.south = False
            self.south_east = False
            self.east_end = False

            self.east_counter = 0
            self.north_east_counter = 0
            self.north_counter = 0
            self.north_west_counter = 0
            self.west_counter = 0
            self.south_west_counter = 0
            self.south_counter = 0
            self.south_east_counter = 0
            self.east_endCounter = 0

            for enemy in enemies:
                # clear the hitbox for all enemies
                enemy.melee_attack_collisions.clear()
            for bat in bats:
                # clear the hitbox for all bats
                bat.melee_attack_collisions.clear()
            if sk.activate and not sk.felled:
                # clear the hitbox for the skeleton king
                sk.melee_attack_collisions.clear()
            self.basic_attack_timer = 0
        self.basic_attack_timer += 1


class BulletUpgrade:
    def __init__(self):
        self.rect = bullet_upgrade.get_rect().scale_by(1, 1)
        self.rect.x = 0
        self.rect.y = 0
        self.upgrade_out = True
        self.upgrade_active = False
        self.animation = 0


class Bullet(pygame.sprite.Sprite):
    # Bullet class allows the player to shoot bullets at enemies
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.draw.circle(transparent_surface, (255, 255, 255), (p.rect.x + 18, p.rect.y + 17), 10)
        self.image = False
        self.starting_point = pygame.math.Vector2(0, 0)
        self.mouse_pos = pygame.mouse.get_pos()
        self.bullet_valid = False
        self.bullet_speed = 50 / 3
        self.bullet_increment = .5
        self.counterX = 0
        self.counterY = 0
        self.bullet_distance = 12
        self.angle = 200
        self.position_reached = False
        self.damage = 20
        self.go_fourth_a = False
        self.go_third_a = False
        self.go_second_a = False
        self.go_first_a = False
        self.bullet_counter = 0
        self.bullet_spawn_speed = 45
        self.shooting = False

    def bullet(self):
        if self.mouse_pos[0] > self.starting_point[0] and self.mouse_pos[1] < self.starting_point[1]:
            # first quadrant
            new_triangle = pygame.math.Vector2(self.mouse_pos[0] - self.starting_point[0], self.mouse_pos[1] -
                                               self.starting_point[1])
            self.angle = -(numpy.rad2deg(numpy.arctan(new_triangle[1] / new_triangle[0])))
        elif self.mouse_pos[0] > self.starting_point[0] and self.mouse_pos[1] > self.starting_point[1]:
            # fourth quadrant
            new_triangle = pygame.math.Vector2(self.mouse_pos[0] - self.starting_point[0], self.mouse_pos[1] -
                                               self.starting_point[1])
            self.angle = (numpy.rad2deg(numpy.arctan(new_triangle[1] / new_triangle[0])))
        elif self.mouse_pos[0] < self.starting_point[0] and self.mouse_pos[1] < self.starting_point[1]:
            # second quadrant
            new_triangle = pygame.math.Vector2(self.starting_point[0] - self.mouse_pos[0], self.starting_point[1] -
                                               self.mouse_pos[1])
            self.angle = (numpy.rad2deg(numpy.arctan(new_triangle[1] / new_triangle[0])))
        elif self.mouse_pos[0] < self.starting_point[0] and self.mouse_pos[1] > self.starting_point[1]:
            # second quadrant
            new_triangle = pygame.math.Vector2(self.starting_point[0] - self.mouse_pos[0], self.starting_point[1] -
                                               self.mouse_pos[1])
            self.angle = (numpy.rad2deg(numpy.arctan(new_triangle[1] / new_triangle[0])))
        if self.counterX >= self.bullet_distance or self.counterY >= self.bullet_distance:  # or
            self.rect.x = p.rect.x
            self.rect.y = p.rect.y
            self.bullet_valid = False
            self.position_reached = False
            self.counterX = 0
            self.counterY = 0
            self.go_fourth_a = False
            self.go_third_a = False
            self.go_second_a = False
            self.go_first_a = False
            bullet_counter = 0
            for bullet in bullets:
                if bullet.rect.x == bullets[bullet_counter].rect.x and bullet.rect.y == bullets[bullet_counter].rect.y:
                    bullets.remove(bullet)
                bullet_counter += 1
        else:
            self.bullet_valid = True
            if (self.rect.x >= self.starting_point[0] and self.rect.y >= self.starting_point[
                1]) and self.position_reached:
                # fourth quadrant - continues traveling after reaching mouse position
                self.rect.y += math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x += math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1

            elif ((self.rect.x <= self.starting_point[0] and self.rect.y >= self.starting_point[1]) and
                  self.position_reached):
                # third quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x -= math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1

            elif ((self.rect.x <= self.starting_point[0] and self.rect.y <= self.starting_point[1]) and
                  self.position_reached):
                # second quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x -= math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1

            elif ((self.rect.x >= self.starting_point[0] and self.rect.y <= self.starting_point[1]) and
                  self.position_reached):
                # first quadrant - continues traveling after reaching mouse position
                self.rect.y -= math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x += math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1

            elif self.rect.x <= self.mouse_pos[0] and self.rect.y <= self.mouse_pos[1] and not self.mouse_pos[1] <= \
                                                                                               self.starting_point[
                                                                                                   1] and not \
            self.mouse_pos[0] <= self.starting_point[
                0] or self.go_fourth_a and not self.go_first_a and not self.go_second_a and not self.go_third_a:
                # fourth quadrant - travels to mouse position
                self.rect.y += math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x += math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1
                self.go_fourth_a = True
                if self.mouse_pos[1] - self.rect.y < 10 and self.mouse_pos[0] - self.rect.x < 10:
                    self.position_reached = True

            elif (self.rect.x >= self.mouse_pos[0] and self.rect.y <= self.mouse_pos[1] and
                  not abs(self.mouse_pos[0] - self.starting_point[
                      0]) < 12 or self.go_third_a and not self.go_first_a and not
                  self.go_second_a and not self.go_fourth_a):
                # third quadrant - travels to mouse position
                self.rect.y -= math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x -= math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1
                self.go_third_a = True
                if self.mouse_pos[1] - self.rect.y <= 10 and self.rect.x - self.mouse_pos[0] <= 10:
                    self.position_reached = True

            elif self.rect.x >= self.mouse_pos[0] and self.rect.y >= self.mouse_pos[1] or self.go_second_a and not self.go_first_a and not self.go_third_a and not self.go_fourth_a:
                # second quadrant - travels to mouse position
                self.rect.y -= math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x -= math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1
                self.go_second_a = True
                if self.rect.y - self.mouse_pos[1] <= 10 and self.mouse_pos[0] - self.rect.x <= 10:
                    self.position_reached = True

            elif self.rect.x <= self.mouse_pos[0] and self.rect.y >= self.mouse_pos[
                1] or self.go_first_a and not self.go_second_a and not self.go_third_a and not self.go_fourth_a:
                # first quadrant - travels to mouse position
                self.rect.y -= math.sin(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.rect.x += math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1
                self.go_first_a = True
                if self.rect.y - self.mouse_pos[1] <= 10 and self.mouse_pos[0] - self.rect.x <= 10:
                    self.position_reached = True

            else:
                # calculates directions for if the bullet is perfectly above or beside the Player
                if self.mouse_pos[1] >= self.starting_point[1] and (
                        abs(self.mouse_pos[0]) - self.starting_point[0]) < 15:
                    self.rect.y += math.sin(90 * (2 * math.pi / 360)) * self.bullet_speed
                elif self.mouse_pos[1] <= self.starting_point[1] and (
                        abs(self.mouse_pos[0]) - self.starting_point[0]) < 15:
                    self.rect.y -= math.sin(90 * (2 * math.pi / 360)) * self.bullet_speed
                elif abs(self.mouse_pos[1] - self.starting_point[1]) <= 5 and self.mouse_pos[0] >= self.starting_point[
                    0]:
                    self.rect.x += math.cos(self.angle * (2 * math.pi / 360)) * self.bullet_speed
                self.counterX += 1
                self.counterY += 1
            if self.rect.x > m.right_boundary_x or self.rect.x < m.left_boundary_x or self.rect.y > m.bottom_boundary_y or self.rect.y < m.top_boundary_y:
                # destroy the bullet if it goes out of the map boundaries
                self.rect = pygame.draw.circle(transparent_surface, (255, 255, 255), (p.rect.x + 18, p.rect.y + 17), 10)
                self.kill()


class Enemy(pygame.sprite.Sprite):
    # Enemy class controls basic functions relating to the enemy
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = random.uniform(1.3, 2)
        self.image = "./images/slimeRect.png"
        self.rect = enemy1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
        self.in_range = False
        self.north_rect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.north_rect.midtop = self.rect.midtop
        self.east_rect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.east_rect.midright = self.rect.midright
        self.south_rect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.south_rect.midbottom = self.rect.midbottom
        self.west_rect = pygame.rect.Rect((self.rect.x, self.rect.y), (10, 10))
        self.west_rect.midleft = self.rect.midleft
        self.north_x_val = 12
        self.north_y_val = -5
        self.east_x_val = 17
        self.east_y_val = 10
        self.south_x_val = 12
        self.south_y_val = 17
        self.west_x_val = -5
        self.west_y_val = 10
        self.circle_rect = pygame.draw.circle(transparent_surface, (0, 50, 0), (self.rect.x, self.rect.y), 10)
        self.middot_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                              (self.rect.x + 16, self.rect.y + 16), 1)
        self.health = 50
        self.bullet_collisions = []
        self.temp_time = 0
        self.previous_pos = ()
        self.melee_attack_collisions = []
        self.spawned = []
        self.spawn_timer = 0
        self.spawn_indicator = None
        self.animation = 1
        self.bat = False
        self.skeleton_king = False
        self.enemy_length = 0
        self.enemy_list = None
        self.player_collide_counter = 0

    def generate_enemy(self):
        pass

    def spawn(self):
        # allows programmer to know if this enemy has spawned
        self.spawned.append(1)

    def travel_north(self):
        # enemy moves North
        self.rect.y -= self.speed
        self.north_rect.y = self.rect.y - self.north_y_val
        self.east_rect.y = self.rect.y + self.east_y_val
        self.south_rect.y = self.rect.y + self.south_y_val
        self.west_rect.y = self.rect.y + self.west_y_val

    def travel_east(self):
        # enemy moves East
        self.rect.x += self.speed
        self.north_rect.x = self.rect.x + self.north_x_val
        self.east_rect.x = self.rect.x + self.east_x_val
        self.south_rect.x = self.rect.x + self.south_x_val
        self.west_rect.x = self.rect.x - self.west_x_val

    def travel_south(self):
        # enemy moves South
        self.rect.y += self.speed
        self.north_rect.y = self.rect.y - self.north_y_val
        self.east_rect.y = self.rect.y + self.east_y_val
        self.south_rect.y = self.rect.y + self.south_y_val
        self.west_rect.y = self.rect.y + self.west_y_val

    def travel_west(self):
        # enemy moves West
        self.rect.x -= self.speed
        self.north_rect.x = self.rect.x + self.north_x_val
        self.east_rect.x = self.rect.x + self.east_x_val
        self.south_rect.x = self.rect.x + self.south_x_val
        self.west_rect.x = self.rect.x - self.west_x_val

    def follow_mc(self):
        # follows the main character around the map
        before_movement = (self.rect.x, self.rect.y)
        stuck_counter = False
        if self.bat:
            # if the enemy is a bat
            self.enemy_list = bats
            self.enemy_length = len(bats)
        else:
            # if the enemy is a slime
            self.enemy_list = enemies
            self.enemy_length = len(enemies)
        if self.rect.x < p.rect.x:
            # enemy moves East
            move_north_counter = 0
            move_east_counter = 0
            move_south_counter = 0
            move_west_counter = 0
            stuck_counter = 0
            for i in range(self.enemy_length):
                # iterate through each enemy
                if self.east_rect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemy_list[i].rect.x and self.rect.y == self.enemy_list[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuck_counter += 1
                else:
                    if not self.east_rect.colliderect(self.enemy_list[i].circle_rect):
                        # enemy moves East if unobstructed
                        move_east_counter += 1
                    else:
                        if (p.rect.x - self.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.north_rect.colliderect(
                                    self.enemy_list[i].circle_rect) and not self.east_rect.colliderect(
                                    self.enemy_list[i].circle_rect):
                                # if enemy can go both North and South, pick a random direction
                                random_direction = random.randint(0, 3)
                                if random_direction <= 1:
                                    # enemy moves North
                                    move_north_counter += 1
                                else:
                                    # enemy moves South
                                    move_south_counter += 1
                            else:
                                # if North and South are not both an option, check which direct is an option
                                if not self.north_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves North
                                    move_north_counter += 1
                                elif not self.south_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves South
                                    move_south_counter += 1
                                elif not self.west_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves West as a last resort
                                    move_west_counter += 1
                                else:
                                    # if enemy has no other option, go along the x-axis
                                    temp_speed = random.uniform(0.1, 1)
                                    if temp_speed < .5:
                                        self.rect.x += temp_speed
                                    else:
                                        self.rect.x -= temp_speed

            if move_east_counter == self.enemy_length - 1:
                self.travel_east()
            elif move_north_counter == self.enemy_length - 1:
                self.travel_north()
            elif move_south_counter == self.enemy_length - 1:
                self.travel_south()
            elif move_west_counter == self.enemy_length - 1:
                self.travel_west()
        if self.rect.x == before_movement[0] and self.rect.y == before_movement[1]:
            if not self.temp_time:
                self.temp_time = seconds
                self.previous_pos = (self.rect.x, self.rect.y)
            if (seconds - self.temp_time) >= 2:
                if self.rect.x == self.previous_pos[0] and self.rect.y == self.previous_pos[1]:
                    # print("Standing Still")
                    pass
        else:
            self.temp_time = 0
        if stuck_counter:
            # helps detect if enemies are stuck
            if stuck_counter > 1:
                # Helps enemies become unstuck on each other
                temp_speed = random.uniform(0.1, 1)
                if temp_speed < .5:
                    self.rect.y += temp_speed
                else:
                    self.rect.y -= temp_speed
                self.stuck = False
                stuck_counter = 0
                # print("Stopped Moving!")

        if self.rect.x > p.rect.x:
            # enemy moves West
            move_north_counter = 0
            move_east_counter = 0
            move_south_counter = 0
            move_west_counter = 0
            stuck_counter = 0
            for i in range(self.enemy_length):
                # iterate through each enemy
                if self.west_rect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemy_list[i].rect.x and self.rect.y == self.enemy_list[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuck_counter += 1
                else:
                    if not self.west_rect.colliderect(self.enemy_list[i].circle_rect):
                        # enemy moves West if unobstructed
                        move_west_counter += 1
                    else:
                        if (self.rect.x - p.rect.x) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.north_rect.colliderect(
                                    self.enemy_list[i].circle_rect) and not self.east_rect.colliderect(
                                    self.enemy_list[i].circle_rect):
                                # if enemy can go both North and South, pick a random direction
                                random_direction = random.randint(0, 3)
                                if random_direction <= 1:
                                    # enemy moves North
                                    move_north_counter += 1
                                else:
                                    # enemy moves South
                                    move_south_counter += 1
                            else:
                                # if North and Sout are not both an option, check which direct is an option
                                if not self.north_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves North
                                    move_north_counter += 1
                                elif not self.south_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves South
                                    move_south_counter += 1
                                elif not self.east_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves East as a last resort
                                    move_east_counter += 1
                                else:
                                    # if enemy has no other option, go along the x-axis in a random direction
                                    temp_speed = random.uniform(0.1, 1)
                                    if temp_speed < .5:
                                        self.rect.x += temp_speed
                                    else:
                                        self.rect.x -= temp_speed

            if move_west_counter == self.enemy_length - 1:
                self.travel_west()
            elif move_north_counter == self.enemy_length - 1:
                self.travel_north()
            elif move_south_counter == self.enemy_length - 1:
                self.travel_south()
            elif move_east_counter == self.enemy_length - 1:
                self.travel_east()
        if self.rect.x == before_movement[0] and self.rect.y == before_movement[1]:
            if not self.temp_time:
                self.temp_time = seconds
                self.previous_pos = (self.rect.x, self.rect.y)
            if (seconds - self.temp_time) >= 2:
                if self.rect.x == self.previous_pos[0] and self.rect.y == self.previous_pos[1]:
                    # print("Standing Still")
                    pass
        else:
            self.temp_time = 0
        if stuck_counter:
            # helps detect if enemies are stuck
            if stuck_counter > 1:
                # Helps enemies become unstuck on each other
                # print("stuck_counter!!!")
                temp_speed = random.uniform(0.1, 1)
                if temp_speed < .5:
                    self.rect.y += temp_speed
                else:
                    self.rect.y -= temp_speed
                self.stuck = False
                stuck_counter = 0
                # print("Stopped Moving!")

        if self.rect.y < p.rect.y:
            # enemy moves South
            move_north_counter = 0
            move_east_counter = 0
            move_south_counter = 0
            move_west_counter = 0
            stuck_counter = 0
            for i in range(self.enemy_length):
                # iterate through each enemy
                if self.south_rect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemy_list[i].rect.x and self.rect.y == self.enemy_list[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuck_counter += 1
                else:
                    if not self.south_rect.colliderect(self.enemy_list[i].circle_rect):
                        # enemy moves South if unobstructed
                        move_south_counter += 1
                    else:
                        if (p.rect.y - self.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.east_rect.colliderect(
                                    self.enemy_list[i].circle_rect) and not self.west_rect.colliderect(
                                    self.enemy_list[i].circle_rect):
                                # if enemy can go both North and South, pick a random direction
                                random_direction = random.randint(0, 3)
                                if random_direction <= 1:
                                    # enemy moves East
                                    move_east_counter += 1
                                else:
                                    # enemy moves West
                                    move_west_counter += 1
                            else:
                                # if East and West are not both an option, check which direct is an option
                                if not self.east_rect.colliderect(self.enemy_list[i].circle_rect):
                                    move_east_counter += 1
                                elif not self.west_rect.colliderect(self.enemy_list[i].circle_rect):
                                    move_west_counter += 1
                                elif not self.north_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves North as a last resort
                                    move_north_counter += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    temp_speed = random.uniform(0.1, 1)
                                    if temp_speed < .5:
                                        self.rect.y += temp_speed
                                    else:
                                        self.rect.y -= temp_speed

            if move_south_counter == self.enemy_length - 1:
                self.travel_south()
            elif move_east_counter == self.enemy_length - 1:
                self.travel_east()
            elif move_west_counter == self.enemy_length - 1:
                self.travel_west()
            elif move_north_counter == self.enemy_length - 1:
                self.travel_north()
        if self.rect.x == before_movement[0] and self.rect.y == before_movement[1]:
            if not self.temp_time:
                self.temp_time = seconds
                self.previous_pos = (self.rect.x, self.rect.y)
            if (seconds - self.temp_time) >= 2:
                if self.rect.x == self.previous_pos[0] and self.rect.y == self.previous_pos[1]:
                    # print("Standing Still")
                    pass
        else:
            self.temp_time = 0
        if stuck_counter:
            # helps detect if enemies are stuck
            if stuck_counter > 1:
                # Helps enemies become unstuck on each other
                temp_speed = random.uniform(0.1, 1)
                if temp_speed < .5:
                    self.rect.y += temp_speed
                else:
                    self.rect.y -= temp_speed
                self.stuck = False
                stuck_counter = 0
                # print("Stopped Moving!")

        if self.rect.y > p.rect.y:
            # enemy moves North
            move_north_counter = 0
            move_east_counter = 0
            move_south_counter = 0
            move_west_counter = 0
            stuck_counter = 0
            for i in range(self.enemy_length):
                # iterate through each enemy
                if self.north_rect.colliderect(p.rect):
                    # if enemy collides with player, do not move
                    pass
                elif self.rect.x == self.enemy_list[i].rect.x and self.rect.y == self.enemy_list[i].rect.y:
                    # checks if the enemy is checking itself in the list of enemies, and if it is itself, skip
                    stuck_counter += 1
                else:
                    if not self.north_rect.colliderect(self.enemy_list[i].circle_rect):
                        # enemy moves North if unobstructed
                        move_north_counter += 1
                    else:
                        if (self.rect.y - p.rect.y) > 50:
                            # enemy continues trying to move towards player if further than 50 pixels away.
                            if not self.east_rect.colliderect(
                                    self.enemy_list[i].circle_rect) and not self.west_rect.colliderect(
                                    self.enemy_list[i].circle_rect):
                                # if enemy can go both North and South, pick a random direction
                                random_direction = random.randint(0, 3)
                                if random_direction <= 1:
                                    # enemy moves East
                                    move_east_counter += 1
                                else:
                                    # enemy moves West
                                    move_west_counter += 1
                            else:
                                # if East and West are not both an option, check which direct is an option
                                if not self.east_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves east
                                    move_east_counter += 1
                                elif not self.west_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves west
                                    move_west_counter += 1
                                elif not self.south_rect.colliderect(self.enemy_list[i].circle_rect):
                                    # enemy moves South as a last resort
                                    move_south_counter += 1
                                else:
                                    # if enemy has no other option, go along the y-axis
                                    temp_speed = random.uniform(0.1, 1)
                                    if temp_speed < .5:
                                        self.rect.y += temp_speed
                                    else:
                                        self.rect.y -= temp_speed

            if move_north_counter == self.enemy_length - 1:
                self.travel_north()
            elif move_east_counter == self.enemy_length - 1:
                self.travel_east()
            elif move_west_counter == self.enemy_length - 1:
                self.travel_west()
            elif move_south_counter == self.enemy_length - 1:
                self.travel_south()
        if self.rect.x == before_movement[0] and self.rect.y == before_movement[1]:
            if not self.temp_time:
                self.temp_time = seconds
                self.previous_pos = (self.rect.x, self.rect.y)
            if (seconds - self.temp_time) >= 2:
                if self.rect.x == self.previous_pos[0] and self.rect.y == self.previous_pos[1]:
                    # print("Standing Still")
                    pass
        else:
            self.temp_time = 0
        if stuck_counter:
            # helps detect if enemies are stuck
            if stuck_counter > 1:
                # Helps enemies become unstuck on each other
                temp_speed = random.uniform(0.1, 1)
                if temp_speed < .5:
                    self.rect.y += temp_speed
                else:
                    self.rect.y -= temp_speed
                self.stuck = False
                stuck_counter = 0
                # print("Stopped Moving!")

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
        self.speed = random.uniform(.6, .8)
        self.follow_mc()
        self.travel_north()
        self.travel_east()
        self.travel_south()
        self.travel_west()
        self.bat = True
        self.playerPOS = ()
        self.found = False
        self.bulletRect = pygame.draw.circle(transparent_surface, (128,12,128), (self.rect.x, self.rect.y), 12)
        self.bulletSpeed = 25/3
        self.spawned2 = []
        self.positionReached = False
        self.goFourthA = False
        self.goThirdA = False
        self.goSecondA = False
        self.goFirstA = False
        self.angle = 0
        self.counter = 0
        self.targetX = 0
        self.targetY = 0
        self.startingPoint = []
        self.shoot_timer = 0
        self.bulletValid = False
        self.hitCounter = 0
        self.spawned = False

    def decide_action(self):
        # time to run at player (If within a certain distance from player, then just run, ignore shooting)
        # time to stop and shoot at player (get close enough to player to shoot but keep distance, doesn't run if too close)

        if (abs(self.rect.x - p.rect.x) >= 165 or abs(self.rect.y - p.rect.y) >= 165) and self.spawned:
            self.follow_mc()
            # print(self.spawned)
        if self.shoot_timer >= 150:
            self.shoot()

        self.shoot_timer += 1


    def find_angle(self):
        if self.spawned:
            if not self.found:
                self.targetX = p.rect.x+18
                self.targetY = p.rect.y+17
                self.startingPoint = [self.rect.x, self.rect.y]
                self.playerPOS = [self.targetX, self.targetY]
                self.bulletRect.x = self.rect.x
                self.bulletRect.y = self.rect.y

                if self.targetX > self.startingPoint[0] and self.targetY < self.startingPoint[1]:
                    # first quadrant
                    newTriangle = pygame.math.Vector2(self.targetX - self.startingPoint[0], self.targetY - self.startingPoint[1])
                    self.angle = -(numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
                elif self.targetX > self.startingPoint[0] and self.targetY > self.startingPoint[1]:
                    # fourth quadrant
                    newTriangle = pygame.math.Vector2(self.targetX - self.startingPoint[0], self.targetY - self.startingPoint[1])
                    self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
                elif self.targetX < self.startingPoint[0] and self.targetY < self.startingPoint[1]:
                    # second quadrant
                    newTriangle = pygame.math.Vector2(self.startingPoint[0] - self.targetX, self.startingPoint[1] - self.targetY)
                    self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
                elif self.targetX < self.startingPoint[0] and self.targetY > self.startingPoint[1]:
                    # third quadrant
                    newTriangle = pygame.math.Vector2(self.startingPoint[0] - self.targetX, self.startingPoint[1] - self.targetY)
                    self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))

                self.found = True
                self.shoot()
    def shoot(self):
        if self.spawned:
            if not self.found:
                self.find_angle()
            # print(f'b.x: {self.bulletRect.x}')
            # print(f'b.y: {self.bulletRect.y}')
            # print(f'p.x: {self.playerPOS[0]}')
            # print(f'p.y: {self.playerPOS[1]}')
            # if abs(self.bulletRect.x - self.playerPOS[0]) < 25 and abs(self.bulletRect.y - self.playerPOS[1]) < 25 or self.counter >= 300:
            if self.counter >= 150:
                self.bulletRect.x = self.rect.x
                self.bulletRect.y = self.rect.y
                self.bulletRect = pygame.draw.circle(transparent_surface, (128,12,128), (self.rect.x, self.rect.y), 12)
                self.bulletValid = False
                self.positionReached = False
                self.goFourthA = False
                self.goThirdA = False
                self.goSecondA = False
                self.goFirstA = False
                self.found = False
                self.counter = 0
                self.shoot_timer = 0
                self.playerPOS = ()
                self.angle = 0
                self.hitCounter = 0
                # print("RESET")

            else:
                self.bulletValid = True

                if self.bulletRect.x <= self.playerPOS[0] and self.bulletRect.y <= self.playerPOS[1] and not self.goFirstA and not self.goSecondA and not self.goThirdA or self.goFourthA:
                    # fourth quadrant - travels to mouse position
                    self.bulletRect.y += math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.bulletRect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.goFourthA = True
                    # print(self.angle)
                    # print("YUHH")
                    # self.bulletRect.y += self.bulletSpeed
                    # self.bulletRect.x += self.bulletSpeed

                elif self.bulletRect.x >= self.playerPOS[0] and self.bulletRect.y <= self.playerPOS[1] and not self.goFirstA and not self.goSecondA and not self.goFourthA or self.goThirdA:
                    # third quadrant - travels to mouse position
                    self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.bulletRect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.goThirdA = True
                    # print("OOOOOOO")
                    # self.bulletRect.y -= self.bulletSpeed
                    # self.bulletRect.x -= self.bulletSpeed

                elif self.bulletRect.x >= self.playerPOS[0] and self.bulletRect.y >= self.playerPOS[1] and not self.goFirstA and not self.goThirdA and not self.goFourthA or self.goSecondA:
                    # second quadrant - travels to mouse position
                    self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.bulletRect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.goSecondA = True
                    # print("AHHHHHH")
                    # self.bulletRect.y -= self.bulletSpeed
                    # self.bulletRect.x -= self.bulletSpeed

                elif self.bulletRect.x <= self.playerPOS[0] and self.bulletRect.y >= self.playerPOS[1] and not self.goSecondA and not self.goThirdA and not self.goFourthA or self.goFirstA:
                    # first quadrant - travels to mouse position
                    self.bulletRect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.bulletRect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                    self.goFirstA = True
                    # print("EEEEEEE")
                    # self.bulletRect.y -= self.bulletSpeed
                    # self.bulletRect.x += self.bulletSpeed

                # else:
                #     print("NUUUUUU")
                #     # if self.playerPOS[1] == self.startingPoint
                #     if self.playerPOS[1] >= self.startingPoint[1] and (abs(self.playerPOS[0]) - self.startingPoint[0]) < 15:
                #         self.bulletRect.y += math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                #     elif self.playerPOS[1] <= self.startingPoint[1] and (abs(self.playerPOS[0]) - self.startingPoint[0]) < 15:
                #         self.bulletRect.y -= math.sin(90 * (2*math.pi/360)) * self.bulletSpeed
                #     elif abs(self.playerPOS[1] - self.startingPoint[1]) <= 5 and self.playerPOS[0] >= self.startingPoint[0]:
                #         self.bulletRect.x += math.cos(self.angle * (2*math.pi/360)) * self.bulletSpeed
                # self.bulletRect = pygame.draw.circle(screen, (128,12,128), (self.bulletRect.x, self.bulletRect.y), 12)

                pygame.draw.circle(screen, (167,28,111), (self.bulletRect.x+12, self.bulletRect.y+12), 12)



                # pygame.draw.rect(screen, (100,0,255), self.bulletRect)
                if self.bulletRect.colliderect(p.rect) and not self.hitCounter:
                    p.health -= 15
                    self.hitCounter += 1
                self.counter += 1


# First mini Boss clas code \/
class MiniEarthElemental(Enemy):
    # Earth Elemental Miniboss
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = minibee1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 20
        self.health = 10
        self.speed = 3
        self.travel_north()
        self.travel_east()
        self.travel_south()
        self.travel_west()
        self.mini = True
        self.felled = False
        self.activate = False
        self.not_attacking = True
        self.is_attacking = False
        self.attack_timer = 0
        self.last_attack = 0
        self.attack_duration = 3
        self.attack_area = None
        self.attack_rect = None
        self.rumble_area = None
        self.aoe_start = 0
        self.rumble_speed = 0
        self.hit_damage = 25
        self.animation = 0
        self.last_auto = 0
        self.attack_speed = 2
        self.speed_snap = False

    def follow_mc(self):
        # Miniboss movment
        if self.rect.x < p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_east()
        if self.rect.x > p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_west()
        if self.rect.y < p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_south()
        if self.rect.y > p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_north()

    def aoe_hit(self):
        CalcTargets.calc_distance(self)
        if CalcTargets.calc_distance(self) <= 80 and self.not_attacking and (
                int(self.attack_timer) - self.last_attack >= 12):
            self.last_attack = int(self.attack_timer)
            self.not_attacking = False
            self.is_attacking = True
            self.aoe_start = int(self.attack_timer)
            p.orspeed = p.speed
            self.rumble_speed = (p.speed * .55)
        if self.is_attacking:
            self.attack_area = pygame.draw.circle(screen, (252, 161, 3), (self.rect.x + 18, self.rect.y + 20), 240, 1)
            self.rumble_area = pygame.draw.circle(screen, (209, 10, 10), (self.rect.x + 18, self.rect.y + 20),
                                                  ((self.attack_timer - self.aoe_start) * 80), 1)
            if p.rect.colliderect(self.rumble_area):
                p.speed = self.rumble_speed
            else:
                p.speed = p.orspeed
            if (int(self.attack_timer) == (self.last_attack + self.attack_duration)):
                self.attacrect = self.attack_area = pygame.draw.circle(screen, (209, 10, 10),
                                                                       (self.rect.x + 18, self.rect.y + 20), 240, 1)
                if p.rect.colliderect(self.attacrect):
                    p.health -= 50
                    # print("Player hit")
                    # print(p.health)
            if (int(self.attack_timer) == (self.last_attack + self.attack_duration)):
                self.not_attacking = True
                self.is_attacking = False
                self.attack_area = None
                self.attack_rect = None
                p.speed = p.orspeed

    def auto_hit_player(self):
        if self.rect.colliderect(p.rect) and (self.attack_timer - self.last_auto) >= self.attack_speed:
            self.last_auto = self.attack_timer
            p.health -= self.hit_damage


class CalcTargets:
    def calc_closest(t1, o1, n1):
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

    def calc_farthest(t1, o1, n1):
        farthest_target = []
        for t1 in o1:
            # itterates through the enemies and checks thier distances then adds them to the list
            xcor = t1.rect.x - p.rect.x
            ycor = t1.rect.y - p.rect.y
            distance = math.sqrt(xcor ** 2 + ycor ** 2)
            farthest_target.append((t1, distance))

        # sorts and condenses the list to targets.
        farthest_target.sort(key=lambda x: x[1], reverse=True)
        farthest_one = farthest_target[:n1]
        return farthest_one

    def calc_distance(self):
        xcor = self.rect.x - p.rect.x
        ycor = self.rect.y - p.rect.y
        distance = math.sqrt(xcor ** 2 + ycor ** 2)
        return distance


class SkeletonKing(Enemy):
    # this class is the games first boss
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = batImg1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 40
        self.mid_box_rect = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.rect.x + 122,
                                                                              self.rect.y + 85, 20, 20))
        self.health = 1250
        self.speed = 1.25
        self.skeleton_king = True
        self.x_coord = 0
        self.y_coord = 0
        self.left_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                              pygame.Rect(self.rect.x + 50, self.rect.y + 170, 20, 10))
        self.right_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                               pygame.Rect(self.rect.x + 226, self.rect.y + 190, 22, 10))
        self.animation_image = 0
        self.main_left_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0), pygame.Rect(self.rect.x + 17,
                                                                                                 self.rect.y + 188, 22,
                                                                                                 12))
        self.main_right_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0), pygame.Rect(self.rect.x + 226,
                                                                                                  self.rect.y + 190, 22,
                                                                                                  10))
        self.run_activation = False
        self.run_counter = 0
        self.animation_interval = 8
        self.run_target = ()
        self.target_aquired = False
        self.felled = False
        self.activate = False

        self.player_collide_counter = 0

    def generate_enemy(self):
        # create the enemy and have it run through its animations and get the coordinates of the player for it to run towards
        if not self.spawned:
            # print('2')
            self.x_coord = random.randint(-340, 990)
            self.y_coord = random.randint(-340, 990)
            while ((abs(self.x_coord - p.rect.x) < 30 and
                    abs(self.y_coord - p.rect.y) < 30) or (250 <= self.x_coord <= 550 and 250 <= self.y_coord <= 550) or
                   self.x_coord < m.left_boundary_x or self.x_coord > m.right_boundary_x or self.y_coord < m.top_boundary_y or
                   self.y_coord > m.bottom_boundary_y or abs(self.x_coord - m.left_boundary_x) < 75 or
                   abs(self.x_coord - m.right_boundary_x) < 75 or abs(self.y_coord - m.top_boundary_y) < 75 or
                   abs(self.y_coord - m.bottom_boundary_y) < 75):
                # looping until the boss spawns in a location inside the map boundaries and also not on top of the player
                self.x_coord = random.randint(-340, 990)
                self.y_coord = random.randint(-340, 990)

            self.rect.x = self.x_coord
            self.rect.y = self.y_coord
            self.spawned.append(1)
        else:
            # animations are ran through and targeting of player position takes place
            if p.rect.x > self.mid_box_rect.x:
                # has the enemy focus his attack on his right main leg
                if (abs(self.main_right_leg_rect.x - p.rect.x) >= 300 or abs(
                        self.main_right_leg_rect.y - p.rect.y) >= 300 or
                        (abs(self.main_right_leg_rect.x - p.rect.x) + abs(
                            self.main_right_leg_rect.y - p.rect.y)) > 400):
                    if not self.target_aquired:
                        # run if the boss does not have the players position
                        self.run_target = (p.rect.x, p.rect.y)
                        self.target_aquired = True
                    self.run_counter += 1
                    self.speed = 7
                    self.animation_interval = 3
            if p.rect.x < self.mid_box_rect.x:
                if (abs(self.main_left_leg_rect.x - p.rect.x) >= 300 or abs(
                        self.main_left_leg_rect.y - p.rect.y) >= 300 or
                        (abs(self.main_left_leg_rect.x - p.rect.x) + abs(self.main_left_leg_rect.y - p.rect.y)) > 400):
                    if not self.target_aquired:
                        self.run_target = (p.rect.x, p.rect.y)
                        self.target_aquired = True
                    self.run_counter += 1
                    self.speed = 7
                    self.animation_interval = 3
            if self.run_counter > 50 or self.rect.colliderect(p.rect):
                self.target_aquired = False
                self.run_target = ()
                self.run_counter = 0
                self.speed = 1
                self.animation_interval = 15
            if self.animation <= self.animation_interval:
                # starts the first animation
                screen.blit(skeleton_king1, (self.rect.x - 30, self.rect.y - 75))
                self.left_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                      pygame.Rect(self.rect.x + 50, self.rect.y + 170, 20, 10))
                self.right_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                       pygame.Rect(self.rect.x + 226, self.rect.y + 190, 22, 10))
                self.animation += 1
                self.animation_image = 1
            elif self.animation <= self.animation_interval * 2:
                # starts the first animation
                screen.blit(skeleton_king2, (self.rect.x - 30, self.rect.y - 75))
                self.left_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                      pygame.Rect(self.rect.x + 17, self.rect.y + 188, 22, 12))
                self.right_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                       pygame.Rect(self.rect.x + 185, self.rect.y + 170, 18, 10))
                self.animation += 1
                self.animation_image = 2
            elif self.animation <= self.animation_interval * 3:
                # starts the first animation
                screen.blit(skeleton_king3, (self.rect.x - 30, self.rect.y - 75))
                self.left_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                      pygame.Rect(self.rect.x + 66, self.rect.y + 170, 20, 10))
                self.right_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                       pygame.Rect(self.rect.x + 226, self.rect.y + 191, 22, 10))
                self.animation += 1
                self.animation_image = 3
            elif self.animation <= self.animation_interval * 4:
                # starts the first animation
                screen.blit(skeleton_king4, (self.rect.x - 30, self.rect.y - 75))
                self.left_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                      pygame.Rect(self.rect.x + 17, self.rect.y + 188, 22, 12))
                self.right_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                       pygame.Rect(self.rect.x + 185, self.rect.y + 170, 18, 10))
                self.animation += 1
                self.animation_image = 4
            elif self.animation > self.animation_interval * 4:
                # starts the first animation
                screen.blit(skeleton_king1, (self.rect.x - 30, self.rect.y - 75))
                self.animation = 1
                self.animation_image = 1
            self.rect.height = 195
            self.rect.width = 265
            self.mid_box_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                 pygame.Rect(self.rect.x + 122, self.rect.y + 85, 20, 20))
            self.main_left_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                       pygame.Rect(self.rect.x + 17, self.rect.y + 188, 22, 12))
            self.main_right_leg_rect = pygame.draw.rect(transparent_surface, (255, 0, 0),
                                                        pygame.Rect(self.rect.x + 226, self.rect.y + 190, 22, 10))

        # self.follow_mc()
        self.run_counter += 1

    def follow_mc(self):
        # the boss will follow the player
        if self.main_right_leg_rect.x < p.rect.x + 12:
            # if player is to the right of main right leg, boss travels east
            self.rect.x += self.speed
        elif p.rect.x + 12 > self.mid_box_rect.x and p.rect.x + 12 < self.main_right_leg_rect.x:
            # if player is to the left of main right leg, boss travels west
            self.rect.x -= self.speed
        if self.main_right_leg_rect.y != p.rect.y + 13:
            if self.main_right_leg_rect.y < p.rect.y + 13:
                # if the player is to the south of the enemy, boss travels south
                self.rect.y += self.speed
            if self.main_right_leg_rect.y > p.rect.y + 13:
                # if the player is to the north of the enemy, boss travels north
                self.rect.y -= self.speed

        if self.main_left_leg_rect.x > p.rect.x + 12:
            # if player is to the right of main right leg, boss travels west
            self.rect.x -= self.speed
        elif p.rect.x + 12 <= self.mid_box_rect.x and p.rect.x + 12 > self.main_left_leg_rect.x:
            # if player is to the left of main right leg, boss travels west
            self.rect.x += self.speed
        if self.main_left_leg_rect.y != p.rect.y + 13:
            if self.main_left_leg_rect.y < p.rect.y + 13:
                # if the player is to the south of the enemy, boss travels south
                self.rect.y += self.speed
            if self.main_left_leg_rect.y > p.rect.y + 13:
                # if the player is to the north of the enemy, boss travels north
                self.rect.y -= self.speed

    def attack(self):
        # handles boss attacks on the player and enemies
        for enemy in enemies:
            # for every enemy that steps on the bosses leg that just touched the ground, have the enemy be destroyed
            if self.left_leg_rect.colliderect(enemy.middot_rect) or self.right_leg_rect.colliderect(enemy.middot_rect):
                if enemy in enemies:
                    enemies.remove(enemy)
        if self.left_leg_rect.colliderect(p.rect) or self.right_leg_rect.colliderect(p.rect):
            # if the player collides with the activated legs, have the player take damage
            if self.player_collide_counter >= 10:
                # measures how fast the player should take damage after entering collision with boss
                checkingDodge = random.randint(0, 100)
                if checkingDodge <= p.dodgeChance:
                    # dodges damage if dodge percent is rolled
                    sk.player_collide_counter = 0
                else:
                    # have the player take damage
                    p.health -= 24
                    sk.player_collide_counter = 0
            else:
                # increase counter if player is still colliding with enemy
                self.player_collide_counter += 1
        else:
            # reset counter
            sk.player_collide_counter = 0


class XP(pygame.sprite.Sprite):
    # Controls the location of the XP and the XP hitbox
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect = pygame.draw.circle(transparent_surface, (0, 255, 0), (x, y), 5)
        self.hitbox_rect = pygame.draw.circle(transparent_surface, (0, 255, 35), (x, y), 50)

    def xp_stationary(self):
        # Displays XP in a specific location
        self.rect = pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 5)
        self.hitbox_rect = pygame.draw.circle(transparent_surface, (0, 255, 35), (self.x, self.y), 50)


speed_item_visible = True
gameTimerOn = False


# gameTime = 0


class XPBar:
    # Displays the XP Bar and upgrade menu
    def __init__(self):
        self.xp_bar_border_rect = None
        self.xp_bar_rect = None
        self.xp_bar_empty_rect = None
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
        self.upgrade_title_font = pygame.font.SysFont('Jenson', 24)
        self.upgrade_desc_font = pygame.font.SysFont('Garamond', 22)
        self.offset = 35
        self.leftover = 0
        self.leftover_size = 0
        self.level_menu = False
        self.pauseTimer = 0
        self.available_upgrades = []
        self.selected_upgrade_choices = False
        self.option1 = None
        self.option2 = None
        self.button_rect1 = None
        self.button_rect2 = None
        self.selected = False

    def show_xp_bar(self):
        # displays XP bar
        self.xp_bar_border_rect = pygame.draw.line(screen, (0, 0, 0), (90 - self.offset, 770),
                                                   (710 - self.offset, 770), 45)
        if self.xp:
            # runs if player has XP
            self.length = self.xp / self.level_xp_requirement
            if self.length >= 1 or self.length + self.leftover >= 1:
                # if player XP reached level requirement, increase XP level and give the Player an upgrade choice
                self.level_menu = True
                self.selected = False
                # temp_timer = gameTimeStr
                while self.level_menu:
                    # while level menu is active
                    global gameTimerStr
                    global gameTime
                    temp_timer = pygame.time.get_ticks() - gameTime
                    self.pauseTimer = temp_timer
                    if pygame.key.get_pressed()[pygame.K_2]:
                        # close upgrade menu if 2 is pressed
                        self.level_menu = False
                        gameTimerStr = temp_timer
                        # gameTimerOn = True
                        gameTime -= temp_timer
                        self.timeAfterPause = gameTime
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.level_menu = False
                            global game
                            game = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # checks for which option the user clicks for option 1
                            if self.button_rect1.collidepoint(event.pos):
                                if self.option1 == 'BA-Dam':
                                    self.basic_attack_damage_upgrade(0)
                                if self.option1 == 'BA-Ran':
                                    self.basic_attack_range_upgrade(0)
                                if self.option1 == 'BA-Spe':
                                    self.basic_attack_speed_upgrade(0)
                                if self.option1 == 'Mov-Spe':
                                    self.move_speed_upgrade(0)
                                if self.option1 == 'Dod-Cha':
                                    self.dodge_chance_upgrade(0)
                                if self.option1 == 'Bul-Dam':
                                    self.bullet_damage_upgrade(0)
                                if self.option1 == 'Bul-Ran':
                                    self.bullet_range_upgrade(0)
                                if self.option1 == 'Bul-Spe':
                                    self.bullet_speed_upgrade(0)
                            elif self.button_rect2.collidepoint(event.pos):
                                # checks for which option the user clicks for option 2
                                if self.option2 == 'BA-Dam':
                                    self.basic_attack_damage_upgrade(0)
                                if self.option2 == 'BA-Ran':
                                    self.basic_attack_range_upgrade(0)
                                if self.option2 == 'BA-Spe':
                                    self.basic_attack_speed_upgrade(0)
                                if self.option2 == 'Mov-Spe':
                                    self.move_speed_upgrade(0)
                                if self.option2 == 'Dod-Cha':
                                    self.dodge_chance_upgrade(0)
                                if self.option2 == 'Bul-Dam':
                                    self.bullet_damage_upgrade(0)
                                if self.option2 == 'Bul-Ran':
                                    self.bullet_range_upgrade(0)
                                if self.option2 == 'Bul-Spe':
                                    self.bullet_speed_upgrade(0)
                    screen.blit(dungeonBackground, (0, 0))
                    screen.blit(mediumScroll, (100, 225))
                    screen.blit(mediumScroll, (450, 225))
                    upgrade_title1_render = self.upgrade_title_font.render('OPTION 1', True, (0, 0, 0))
                    screen.blit(upgrade_title1_render, (202, 330))
                    upgrade_title2_render = self.upgrade_title_font.render('OPTION 2', True, (0, 0, 0))
                    screen.blit(upgrade_title2_render, (550, 330))

                    self.button_rect1 = pygame.Rect(100, 222, 285, 370)
                    self.button_rect2 = pygame.Rect(450, 222, 285, 370)

                    pygame.draw.rect(transparent_surface, (0, 0, 255), self.button_rect1)
                    pygame.draw.rect(transparent_surface, (0, 0, 255), self.button_rect2)

                    if not self.selected_upgrade_choices and not self.selected:
                        # if two random options have not been generated, then generate them
                        self.available_upgrades = ['BA-Dam', 'BA-Ran',
                                                   'BA-Spe', 'Mov-Spe', 'Dod-Cha', 'Bul-Dam', 'Bul-Ran', 'Bul-Spe']
                        random_upgrade1 = random.randint(0, (len(self.available_upgrades) - 1))
                        self.option1 = self.available_upgrades[random_upgrade1]
                        random_upgrade2 = random.randint(0, (len(self.available_upgrades) - 1))
                        while random_upgrade2 == random_upgrade1:
                            # checks to make sure two options are not the same
                            random_upgrade2 = random.randint(0, (len(self.available_upgrades) - 1))
                        self.option2 = self.available_upgrades[random_upgrade2]
                        self.selected_upgrade_choices = True
                        self.two_upgrade_choices = [self.available_upgrades[random_upgrade1],
                                                    self.available_upgrades[random_upgrade2]]

                        self.button_rect1 = pygame.Rect(100, 222, 285, 370)
                        self.button_rect2 = pygame.Rect(450, 222, 285, 370)

                    if self.selected_upgrade_choices:
                        # if two random choices have been generated, call the appropriate function and blit the information
                        # to the screen.
                        if 'BA-Dam' in self.two_upgrade_choices:
                            # basic attack damage
                            if self.option1 == 'BA-Dam':
                                self.basic_attack_damage_upgrade(1)
                            else:
                                self.basic_attack_damage_upgrade(2)
                        if 'BA-Ran' in self.two_upgrade_choices:
                            # basic attack range
                            if self.option1 == 'BA-Ran':
                                self.basic_attack_range_upgrade(1)
                            else:
                                self.basic_attack_range_upgrade(2)
                        if 'BA-Spe' in self.two_upgrade_choices:
                            # basic attack speed
                            if self.option1 == 'BA-Spe':
                                self.basic_attack_speed_upgrade(1)
                            else:
                                self.basic_attack_speed_upgrade(2)
                        if 'Mov-Spe' in self.two_upgrade_choices:
                            # player movement speed
                            if self.option1 == 'Mov-Spe':
                                self.move_speed_upgrade(1)
                            else:
                                self.move_speed_upgrade(2)
                        if 'Dod-Cha' in self.two_upgrade_choices:
                            # dodge chance
                            if self.option1 == 'Dod-Cha':
                                self.dodge_chance_upgrade(1)
                            else:
                                self.dodge_chance_upgrade(2)
                        if 'Bul-Dam' in self.two_upgrade_choices:
                            # bullet damage
                            if self.option1 == 'Bul-Dam':
                                self.bullet_damage_upgrade(1)
                            else:
                                self.bullet_damage_upgrade(2)
                        if 'Bul-Ran' in self.two_upgrade_choices:
                            # bullet range
                            if self.option1 == 'Bul-Ran':
                                self.bullet_range_upgrade(1)
                            else:
                                self.bullet_range_upgrade(2)
                        if 'Bul-Spe' in self.two_upgrade_choices:
                            # bullet speed
                            if self.option1 == 'Bul-Spe':
                                self.bullet_speed_upgrade(1)
                            else:
                                self.bullet_speed_upgrade(2)

                    clock.tick(15)
                    pygame.display.update()

                self.leftover = self.xp - self.level_xp_requirement
                self.level += 1
                self.xp = 0
                self.level_xp_requirement *= 1.25
                self.length = self.xp / self.level_xp_requirement
                if self.leftover:
                    # if any leftover XP from previous level, add it to the new level
                    self.leftover_size = (((1 / self.level_xp_requirement) * self.total_length) * self.leftover)
                    self.xp_bar_rect = pygame.draw.line(screen, (28, 36, 192), (100 - self.offset, 770),
                                                        (self.leftover_size + 100 - self.offset, 770), 25)
                    self.leftover = 0
            else:
                # if player has XP but not enough for a full XP level, display the xp bar
                self.xp_bar_rect = pygame.draw.line(screen, (28, 36, 192), (100 - self.offset, 770),
                                                    ((self.total_length * self.length) + self.leftover_size
                                                     + 100 - self.offset, 770), 25)
                self.xp_bar_empty_rect = pygame.draw.line(screen, (255, 255, 255),
                                                          ((self.total_length * self.length) +
                                                           self.leftover_size + 100 - self.offset, 770),
                                                          (700 - self.offset, 770), 25)
        else:
            # Displays if player has zero XP
            self.xp_bar_rect = pygame.draw.line(screen, (28, 36, 192), (100 - self.offset, 770),
                                                (self.leftover_size + 100 - self.offset, 770), 25)
            self.xp_bar_empty_rect = pygame.draw.line(screen, (255, 255, 255),
                                                      (self.leftover_size + 100 - self.offset, 770),
                                                      (700 - self.offset, 770), 25)

        # Displays level number
        self.connector = pygame.draw.line(screen, (0, 0, 0), (710 - self.offset, 770), (740 - self.offset, 770), 5)
        self.left = pygame.draw.line(screen, (0, 0, 0), (740 - self.offset, 790), (740 - self.offset, 750), 6)
        self.top = pygame.draw.line(screen, (0, 0, 0), (738 - self.offset, 750), (785 - self.offset, 750), 6)
        self.bottom = pygame.draw.line(screen, (0, 0, 0), (738 - self.offset, 790), (785 - self.offset, 790), 6)
        self.right = pygame.draw.line(screen, (0, 0, 0), (785 - self.offset, 793), (785 - self.offset, 748), 6)
        self.level_background = pygame.draw.line(screen, (255, 255, 255), (744 - self.offset, 770),
                                                 (782 - self.offset, 770), 33)
        level_render = self.level_font.render(str(self.level), True, (0, 0, 0))
        if self.level < 10:
            screen.blit(level_render, (756 - self.offset, 758))
        else:
            # moves the level number to the left to better accommodate another value fitting into the box
            screen.blit(level_render, (747 - self.offset, 758))

    def basic_attack_damage_upgrade(self, option):
        # display information regarding the basic attack damage upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_ba_damage1_render = self.upgrade_desc_font.render('Increase Basic Attack', True, (0, 0, 0))
            screen.blit(upgrade_ba_damage1_render, (150, 365))
            upgrade_ba_damage2_render = self.upgrade_desc_font.render('Damage by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_damage2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_ba_damage1_render = self.upgrade_desc_font.render('Increase Basic Attack', True, (0, 0, 0))
            screen.blit(upgrade_ba_damage1_render, (500, 365))
            upgrade_ba_damage2_render = self.upgrade_desc_font.render('Damage by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_damage2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            ba.damage *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def basic_attack_range_upgrade(self, option):
        # display information regarding the basic attack range upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_ba_range1_render = self.upgrade_desc_font.render('Increase Basic Attack', True, (0, 0, 0))
            screen.blit(upgrade_ba_range1_render, (150, 365))
            upgrade_ba_range2_render = self.upgrade_desc_font.render('Range by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_range2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_ba_range1_render = self.upgrade_desc_font.render('Increase Basic Attack', True, (0, 0, 0))
            screen.blit(upgrade_ba_range1_render, (500, 365))
            upgrade_ba_range2_render = self.upgrade_desc_font.render('Range by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_range2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            ba.range_increase += 10
            ba.hitbox_radius += 14
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def basic_attack_speed_upgrade(self, option):
        # display information regarding the basic attack speed upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_ba_speed1_render = self.upgrade_desc_font.render('Increase Basic Attack', True, (0, 0, 0))
            screen.blit(upgrade_ba_speed1_render, (150, 365))
            upgrade_ba_speed2_render = self.upgrade_desc_font.render('Speed by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_speed2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_ba_speed1_render = self.upgrade_desc_font.render('Increase Basic Attack', True, (0, 0, 0))
            screen.blit(upgrade_ba_speed1_render, (500, 365))
            upgrade_ba_speed2_render = self.upgrade_desc_font.render('Speed by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_speed2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            ba.timer_target *= .9
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def move_speed_upgrade(self, option):
        # display information regarding the movement speed upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_move_speed1_render = self.upgrade_desc_font.render('Increase Player Move', True, (0, 0, 0))
            screen.blit(upgrade_move_speed1_render, (150, 365))
            upgrade_move_speed2_render = self.upgrade_desc_font.render('Speed by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_move_speed2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_move_speed1_render = self.upgrade_desc_font.render('Increase Player Move', True, (0, 0, 0))
            screen.blit(upgrade_move_speed1_render, (500, 365))
            upgrade_move_speed2_render = self.upgrade_desc_font.render('Speed by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_move_speed2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            p.speed *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def dodge_chance_upgrade(self, option):
        # display information regarding the dodge chance upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_dodge1_render = self.upgrade_desc_font.render('Increase Dodge', True, (0, 0, 0))
            screen.blit(upgrade_dodge1_render, (150, 365))
            upgrade_dodge2_render = self.upgrade_desc_font.render('Chance by 2%.', True, (0, 0, 0))
            screen.blit(upgrade_dodge2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_dodge1_render = self.upgrade_desc_font.render('Increase Dodge', True, (0, 0, 0))
            screen.blit(upgrade_dodge1_render, (500, 365))
            upgrade_dodge2_render = self.upgrade_desc_font.render('Chance by 2%.', True, (0, 0, 0))
            screen.blit(upgrade_dodge2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            p.dodgeChance += 2
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def bullet_damage_upgrade(self, option):
        # display information regarding the bullet damage upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_bul_damage1_render = self.upgrade_desc_font.render('Increase Bullet', True, (0, 0, 0))
            screen.blit(upgrade_bul_damage1_render, (150, 365))
            upgrade_bul_damage2_render = self.upgrade_desc_font.render('Damage by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_damage2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_bul_damage1_render = self.upgrade_desc_font.render('Increase Bullet', True, (0, 0, 0))
            screen.blit(upgrade_bul_damage1_render, (500, 365))
            upgrade_bul_damage2_render = self.upgrade_desc_font.render('Damage by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_damage2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            b.damage *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def bullet_range_upgrade(self, option):
        # display information regarding the bullet range upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_bul_range1_render = self.upgrade_desc_font.render('Increase Bullet', True, (0, 0, 0))
            screen.blit(upgrade_bul_range1_render, (150, 365))
            upgrade_bul_range2_render = self.upgrade_desc_font.render('Range by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_range2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_bul_range1_render = self.upgrade_desc_font.render('Increase Bullet', True, (0, 0, 0))
            screen.blit(upgrade_bul_range1_render, (500, 365))
            upgrade_bul_range2_render = self.upgrade_desc_font.render('Range by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_range2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            b.bullet_distance *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def bullet_speed_upgrade(self, option):
        # display information regarding the bullet speed upgrade and if selected, implement the upgrade.
        if option == 1:
            # displays to the left
            upgrade_bul_speed1_render = self.upgrade_desc_font.render('Increase Bullet', True, (0, 0, 0))
            screen.blit(upgrade_bul_speed1_render, (150, 365))
            upgrade_bul_speed2_render = self.upgrade_desc_font.render('Speed by 5%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_speed2_render, (150, 390))

        elif option == 2:
            # displays to the right
            upgrade_bul_speed1_render = self.upgrade_desc_font.render('Increase Bullet', True, (0, 0, 0))
            screen.blit(upgrade_bul_speed1_render, (500, 365))
            upgrade_bul_speed2_render = self.upgrade_desc_font.render('Speed by 5%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_speed2_render, (500, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            b.bullet_spawn_speed *= .95
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True


# initializes the Player and Enemy classes
p = Player()
m = Map()
b = Bullet()
ee = MiniEarthElemental(0, 0)
sk = SkeletonKing(0, 0)
xpB = XPBar()
ba = BasicAttack()
enemies = []
bats = []
bullets = []
bup = BulletUpgrade()


# bullets = [Bullet() for _ in range(1)]


def reset_stats():
    # resets the stats so the player can start fresh when they die
    global gameTime
    global xpB
    global xp
    global sk
    global ba
    global p
    global m
    global b
    xpB = XPBar()
    xp.clear()
    enemies.clear()
    bats.clear()
    bullets.clear()
    sk = SkeletonKing(0, 0)
    ba = BasicAttack()
    p = Player()
    m = Map()
    b = Bullet()
    gameTime = 0
    p.death = False


# adds ability for text to be on screen
def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


# adding the ability to implement buttons
def button(msg, x, y, w, h, ic, ac, action):
    # if buttons are pressed, activate the appropriate functions
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global pause
    global game
    global activate_bullet
    global bullet_timer1
    global bullet_timer2
    # does a specific action based on button text and if it was clicked
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h), border_radius=20)
        if click[0] == 1 and action != None:
            if action == "Settings":
                pause = False
                settings_menu()
            elif action == "Fullscreen Toggle":
                fullscreen_toggle()
                pygame.display.update()
            elif action == "Credits":
                pause = False
                credits()
            elif action == "Quit":
                game = False
                pygame.quit()
                sys.exit()
            elif action == "Play":
                if p.death:
                    reset_stats()
                pause = False
                game = True
                activate_bullet = True
                bullet_timer1 = 2
                bullet_timer2 = 0
            elif action == "main_menu":
                main_menu()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h), border_radius=20)

    small_text = pygame.font.SysFont('Garamond', 20, bold=True)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


# loads images
bg_img = pygame.image.load('images/dungeon.png').convert_alpha()
speed_img = pygame.image.load("./images/Noodle.png").convert_alpha()

# setting up the fonts for the timer and the fps tracker
timer_font = pygame.font.SysFont('futura', 64)
fps_font = pygame.font.SysFont('futura', 28)

gameTimeStr = 0
minutes = 0
seconds = 0


# starts keeping track of the time within the game
def start_game_time():
    global gameTime
    if xpB.pauseTimer:
        # if a menu was paused, subtract the time paused from the global game time
        gameTime = pygame.time.get_ticks() - xpB.pauseTimer
    else:
        gameTime = pygame.time.get_ticks()
    # print(gameTime)
    global gameTimeStr
    gameTimeStr = int((gameTime - prevGameTime) / 1000)
    if gameTimeStr < 60:
        # if the game time is less than a minute, set gameTimeStr to the time
        gameTimeStr = str(int((gameTime - prevGameTime) / 1000))
        global seconds
        seconds = int(gameTimeStr) % 60
    elif gameTimeStr >= 60:
        # if the game time is more than or equal than a minute, set gameTimeStr to the game time
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


# function to display the game timer to show how long you have been in-game
def display_timer(text, font, text_color):
    gameTimer = font.render(str(text), True, text_color).convert_alpha()
    screen.blit(gameTimer, (675, 15))
    # timerRect = gameTimer.get_rect()
    # screen.blit(gameTimer, (675, 15), timerRect)


# function to show the frames per second in the corner
def display_fps(text, font, text_color):
    text = str(int(text))
    # print(text)
    fps_display = font.render(text, True, text_color).convert_alpha()
    # print(fps_display)
    screen.blit(fps_display, (0, 0))


# adds the ability to fullscreen the game (not toggle yet)
def fullscreen_toggle():
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.update()


# function to show the credits menu, which will contain the credits to all resources used
def credits():
    start_time = pygame.time.get_ticks()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    global pause  # risky
    pause = True

    while pause:
        global gameTimerStr
        global gameTime
        temp_timer = pygame.time.get_ticks() - gameTime
        xpB.pauseTimer = temp_timer
        # if you press escape, you go back to the settings menu
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and (pygame.time.get_ticks() - start_time >= 500):
            pause = False
            settings_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        # setting menu background
        screen.blit(dungeonBackground, (0, 0))
        # establishing text for menu
        large_text = pygame.font.SysFont('Garamond', 100, bold=True)
        main_text = pygame.font.SysFont('Garamond', 20, bold=True)
        text_surf, text_rect = text_objects("Credits", large_text)
        text_surf3, text_rect3 = text_objects("twitter @HelloRumin - map tiles", main_text)
        text_surf4, text_rect4 = text_objects("itch.io NekoIndie - slime/bat enemies", main_text)
        text_surf5, text_rect5 = text_objects("pngtree.com - scroll image behind menu screen titles", main_text)
        text_surf6, text_rect6 = text_objects("gamedeveloperstudio.itch.io/ - Upgrade scroll buttons", main_text)
        text_surf7, text_rect7 = text_objects("rawpixel.com - scroll image behind these credits!", main_text)
        text_rect.center = ((screen_width / 2), (screen_height / 3.3))
        text_rect3.center = ((screen_width / 2), (screen_height / 3.3) + 200)
        text_rect4.center = ((screen_width / 2), (screen_height / 3.3) + 230)
        text_rect5.center = ((screen_width / 2), (screen_height / 3.3) + 260)
        text_rect6.center = ((screen_width / 2), (screen_height / 3.3) + 290)
        text_rect7.center = ((screen_width / 2), (screen_height / 3.3) + 320)
        screen.blit(horizontalScroll, (screen_width / 2 - 288, screen_height / 10))
        screen.blit(buttonScroll, ((screen_width / 2) - 360, (screen_height / 2.2)))
        # putting text on menu
        screen.blit(text_surf, text_rect)
        screen.blit(text_surf3, text_rect3)
        screen.blit(text_surf4, text_rect4)
        screen.blit(text_surf5, text_rect5)
        screen.blit(text_surf6, text_rect6)
        screen.blit(text_surf7, text_rect7)
        # need to put credits in here

        pygame.display.update()
        clock.tick(15)


# function to show the Main Menu before the game starts
def main_menu():
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    global pause

    while pause:
        global gameTime
        temp_timer = pygame.time.get_ticks() - gameTime
        xpB.pauseTimer = temp_timer
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        # sets the main menu background
        screen.blit(dungeonBackground, (0, 0))
        # establishing the text for the title on the menu
        large_text = pygame.font.SysFont('Garamond', 80, bold=True)
        main_text = pygame.font.SysFont('Garamond', 20, bold=True)
        text_surf, text_rect = text_objects("Rogue", large_text)
        text_surf2, text_rect2 = text_objects("Survival", large_text)
        text_rect.center = ((screen_width / 2), (screen_height / 3.3) - 40)
        text_rect2.center = ((screen_width / 2), (screen_height / 3.3) + 40)
        screen.blit(horizontalScroll, (screen_width / 2 - 288, screen_height / 10))
        # displays the buttons available on the Main Menu
        button("Play!", (screen_width / 4) - 100, (screen_height / 1.6), 200, 100, (247, 167, 82), (184, 120, 51),
               "Play")
        button("Close :(", (screen_width / 1.3) - 100, (screen_height / 1.6), 200,
               100, (247, 167, 82),
               (184, 120, 51), "Quit")
        # puts all of the text on the screen
        screen.blit(text_surf, text_rect)
        screen.blit(text_surf2, text_rect2)
        pygame.display.update()
        clock.tick(15)


def death_screen():
    # displays a death screen if the player dies
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    global pause
    pause = True
    while pause:
        global gameTimerStr
        global gameTime
        temp_timer = pygame.time.get_ticks() - gameTime
        xpB.pauseTimer = temp_timer
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        screen.blit(dungeonBackground, (0, 0))

        large_text = pygame.font.SysFont('Garamond', 70, bold=True)
        text_surf, text_rect = text_objects("YOU DIED", large_text)
        text_rect.center = ((screen_width / 2), (screen_height / 3.3))
        screen.blit(horizontalScroll, (screen_width / 2 - 288, screen_height / 10))
        # shows the buttons needed on the pause menu
        button("Main Menu", ((screen_width / 4) - 100), (screen_height / 2), 200, 100, (247, 167, 82),
               (184, 120, 51), "main_menu")
        button("Quit", (screen_width / 1.3) - 100, (screen_height / 2), 200,
               100, (247, 167, 82),
               (184, 120, 51), "Quit")
        # puts the menu text on the screen
        screen.blit(text_surf, text_rect)

        pygame.display.update()
        clock.tick(15)


def pause_game():
    # displays a pause menu while the game is paused
    start_time = pygame.time.get_ticks()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    global pause  # risky
    pause = True

    while pause:
        # tracks the time when you entered menu to set it back to that afterward
        global gameTimerStr
        global gameTime
        temp_timer = pygame.time.get_ticks() - gameTime
        xpB.pauseTimer = temp_timer
        # if you hit escape you go back to the game and the time is put back to when you paused
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and (pygame.time.get_ticks() - start_time >= 500):
            pause = False
            gameTimerStr = temp_timer
            gameTime -= temp_timer
            xpB.timeAfterPause = gameTime
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        screen.blit(dungeonBackground, (0, 0))

        large_text = pygame.font.SysFont('Garamond', 100, bold=True)
        text_surf, text_rect = text_objects("Paused", large_text)
        text_rect.center = ((screen_width / 2), (screen_height / 3.3))
        screen.blit(horizontalScroll, (screen_width / 2 - 288, screen_height / 10))
        # shows the buttons needed on the pause menu
        button("Settings", ((screen_width / 4) - 100), (screen_height / 2), 200, 100, (247, 167, 82),
               (184, 120, 51), "Settings")
        button("Main Menu", (screen_width / 1.3) - 100, (screen_height / 2), 200,
               100, (247, 167, 82),
               (184, 120, 51), "main_menu")
        # puts the menu text on the screen
        screen.blit(text_surf, text_rect)

        pygame.display.update()
        clock.tick(15)


# function to run the settings menu, which is accessible through the pause menu
def settings_menu():
    # displays the settings menu
    start_time = pygame.time.get_ticks()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    global pause  # risky
    pause = True

    while pause:
        # tracks the current time to set it back when you leave the menu
        global gameTimerStr
        global gameTime
        temp_timer = pygame.time.get_ticks() - gameTime
        xpB.pauseTimer = temp_timer
        # if you press escape, go back to the pause menu
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and (pygame.time.get_ticks() - start_time >= 500):
            pause = False
            pause_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
        screen.blit(dungeonBackground, (0, 0))
        large_text = pygame.font.SysFont('Garamond', 100, bold=True)
        text_surf, text_rect = text_objects("Settings", large_text)
        text_rect.center = ((screen_width / 2), (screen_height / 3.3))
        screen.blit(horizontalScroll, (screen_width / 2 - 288, screen_height / 10))
        # putting the needed buttons on the settings Menu
        button("Fullscreen", (screen_width / 4) - 100, (screen_height / 1.4), 200, 100, (247, 167, 82),
               (184, 120, 51), "Fullscreen Toggle")
        button("Credits", (screen_width / 1.3) - 100, (screen_height / 1.4), 200,
               100, (247, 167, 82), (184, 120, 51), "Credits")
        # putting the menu text on the screen
        screen.blit(text_surf, text_rect)

        pygame.display.update()
        clock.tick(15)

# unpausing func for the buttons
def unpause():
    pause = False


# def to store all the keypress functions
def key_pressed():
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

    if key_presses[pygame.K_ESCAPE]:
        # if ESC key is pressed, pause game
        pause_game()


# begin the game by opening to the main menu, which has a play button to start the game
main_menu()

# activating the character shooting and needed variables to maintain it
activate_bullet = True
bullet_timer1 = 2
bullet_timer2 = 0

# game is now running
while game:
    # the core game loop
    start_game_time()

    fps = clock.get_fps()

    # sets the fps to 60
    clock.tick(60)

    # Introducing a pause function for the buttons and game pause functionality
    pause = False
    # making sure the X button still closes the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the x in the top right corner of game is clicked, the program will close.
            game = False

    # cycling through the possible key presses
    key_pressed()

    # if the player reaches no health, show the death screen
    if p.health <= 0:
        prevGameTime = gameTime
        p.death = True
        death_screen()
        while p.death:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    p.death = False
                    game = False
    # makes the map visible
    # screen.blit(pygame.transform.scale(bg_img, (2250, 2250)), (-800 - m.cameraX, -800 - m.cameraY))
    screen.blit(bg_img, (-800 - m.cameraX, -800 - m.cameraY))

    for x in xp:
        # constantly display the XP
        x.xp_stationary()
        if x.hitbox_rect.colliderect(p.rect):
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
            if x.rect.x + 18 < p.rect.x:
                x.x += p.speed
            if x.rect.x + 18 > p.rect.x:
                x.x -= p.speed
            if x.rect.y + 18 < p.rect.y:
                x.y += p.speed
            if x.rect.y + 18 > p.rect.y:
                x.y -= p.speed

    # makes the main character visible
    screen.blit(pygame.transform.scale(mc_img, (40, 35)), (p.rect.x, p.rect.y))

    bullet_timer2 = gameTime / 1000
    # if seconds % b.bullet_increment == 0:
    if b.shooting:
        activate_bullet = True
    # if bullet_timer2 > bullet_timer1:
    # if b.bullet_counter >= b.bullet_spawn_speed:
    if b.shooting and b.bullet_counter and b.bullet_counter >= b.bullet_spawn_speed:
        # controls the speed of shooting the bullets
        bullets.append(b)
        for bullet in bullets:
            bullet.mouse_pos = pygame.mouse.get_pos()
            bullet.mouse_pos = (pygame.math.Vector2(bullet.mouse_pos[0], bullet.mouse_pos[1]))
            bullet.starting_point = pygame.math.Vector2(p.rect.x, p.rect.y)
            bullet.bullet()
        bullet_timer1 += b.bullet_increment
        activate_bullet = False
        b.bullet_counter = 0
        # print(activate_bullet)
    for bullet in bullets:
        if bullet.bullet_valid:
            # if bullet ability has been activated, then have the bullet move
            pygame.draw.circle(screen, (255, 255, 255), (bullet.rect.x + 18, bullet.rect.y + 17), 10)
            bullet.bullet()

    if len(enemies) < 15:
        # if the number of slimes is less than 15, spawn more slime in
        x_coord = random.randint(-340, 990)
        y_coord = random.randint(-340, 990)
        enemy_length = len(enemies)
        count = 0
        for enemy in enemies:
            while x_coord == enemy.rect.x or y_coord == enemy.rect.y or (
                    abs(x_coord - enemy.rect.x) < 30 and abs(y_coord - enemy.rect.y) < 30) or (
                    250 <= x_coord <= 550 and 250 <= y_coord <= 550) or x_coord < m.left_boundary_x or x_coord > m.right_boundary_x or y_coord < m.top_boundary_y or y_coord > m.bottom_boundary_y or abs(
                    x_coord - m.left_boundary_x) < 25 or abs(x_coord - m.right_boundary_x) < 25 or abs(
                    y_coord - m.top_boundary_y) < 25 or abs(y_coord - m.bottom_boundary_y) < 25:
                x_coord = random.randint(-340, 990)
                y_coord = random.randint(-340, 990)
        enemies.append(Enemy(x_coord, y_coord))

    if len(bats) < 8:
        # if the number of bats is less than 8, spawn more bats in
        x_coord = random.randint(-340, 990)
        y_coord = random.randint(-340, 990)
        bat_length = len(bats)
        count = 0
        for bat in bats:
            while x_coord == bat.rect.x or y_coord == bat.rect.y or (
                    abs(x_coord - bat.rect.x) < 30 and abs(y_coord - bat.rect.y) < 30) or (
                    250 <= x_coord <= 550 and 250 <= y_coord <= 550) or x_coord < m.left_boundary_x or x_coord > m.right_boundary_x or y_coord < m.top_boundary_y or y_coord > m.bottom_boundary_y or abs(
                    x_coord - m.left_boundary_x) < 25 or abs(x_coord - m.right_boundary_x) < 25 or abs(
                    y_coord - m.top_boundary_y) < 25 or abs(y_coord - m.bottom_boundary_y) < 25:
                x_coord = random.randint(-340, 990)
                y_coord = random.randint(-340, 990)
        bats.append(Bat(x_coord, y_coord))

    for enemy in enemies:
        # go through each enemy and control the spawning and movements
        if not enemy.spawned:
            pygame.draw.circle(screen, (128, 0, 32), (enemy.rect.x, enemy.rect.y), 16)
            enemy.spawn_timer += 1
            if enemy.spawn_timer >= 75:
                enemy.spawned.append(1)
                enemy.spawn_indicator = None
        else:
            # if enemy has spawned, go through the animations and collision detection
            if enemy.animation <= 15:
                screen.blit(pygame.transform.scale(enemy4, (45, 40)), (enemy.rect.x - 6, enemy.rect.y - 6))
                enemy.animation += 1

            elif enemy.animation <= 30:
                screen.blit(pygame.transform.scale(enemy3, (45, 40)), (enemy.rect.x - 6, enemy.rect.y - 6))
                enemy.animation += 1

            elif enemy.animation <= 45:
                screen.blit(pygame.transform.scale(enemy2, (45, 40)), (enemy.rect.x - 6, enemy.rect.y - 6))
                enemy.animation += 1

            elif enemy.animation <= 60:
                screen.blit(pygame.transform.scale(enemy1, (45, 40)), (enemy.rect.x - 6, enemy.rect.y - 6))
                enemy.animation += 1

            elif enemy.animation > 60:
                screen.blit(pygame.transform.scale(enemy4, (45, 40)), (enemy.rect.x - 6, enemy.rect.y - 6))
                enemy.animation = 1

            # screen.blit(pygame.transform.scale(enemyOriginal, (45, 40)), (enemy.rect.x, enemy.rect.y))
            enemy.circle_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                   (enemy.rect.x + 18, enemy.rect.y + 17), 10)
            enemy.middot_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                   (enemy.rect.x + 16, enemy.rect.y + 16), 8)
            enemy.generate_enemy()
            enemy.follow_mc()

            if b.shooting:
                for bullet in bullets:
                    # for each active bullet, if the bullet hits an enemy, deal damage if appropriate conditions met.
                    if enemy.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                        if not enemy.bullet_collisions:
                            # if the enemy has encountered it's first bullet, add to the list and take damage
                            enemy.bullet_collisions.append(bullet)
                            enemy.health -= b.damage
                        elif enemy.bullet_collisions:
                            # if the list of bullets the enemy has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                            i = 0
                            for l in enemy.bullet_collisions:
                                if bullet.rect.x == enemy.bullet_collisions[i].rect.x and bullet.rect.y == \
                                        enemy.bullet_collisions[i].rect.y:
                                    pass
                                elif bullet not in enemy.bullet_collisions and bullet.bullet_valid:
                                    enemy.bullet_collisions.append(bullet)
                                    enemy.health -= b.damage
                                i += 1
            for bullet in bullets:
                # for each active bullet, if the bullet hits an enemy, deal damage if appropriate conditions met.
                if enemy.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                    if not enemy.bullet_collisions:
                        # if the enemy has encountered it's first bullet, add to the list and take damage
                        enemy.bullet_collisions.append(bullet)
                        enemy.health -= b.damage
                    elif enemy.bullet_collisions:
                        # if the list of bullets the enemy has collided with is greater than 0,
                        # make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in enemy.bullet_collisions:
                            if (bullet.rect.x == enemy.bullet_collisions[i].rect.x and
                                    bullet.rect.y == enemy.bullet_collisions[i].rect.y):
                                pass
                            elif bullet not in enemy.bullet_collisions and bullet.bullet_valid:
                                enemy.bullet_collisions.append(bullet)
                                enemy.health -= b.damage
                            i += 1

            if enemy.rect.colliderect(ba.hitbox_rect) and ba.running and not enemy.melee_attack_collisions:
                # Reduce enemy health from the Players basic attack if not hit by that same attack swing
                enemy.health -= ba.damage
                enemy.melee_attack_collisions.append(1)

            if sk.activate and not sk.felled:
                # if the skeleton king is active and not killed and it hit by the players basic attack, the boss  takes damage
                if sk.rect.colliderect(ba.hitbox_rect) and ba.running and not sk.melee_attack_collisions:
                    sk.health -= ba.damage
                    sk.melee_attack_collisions.append(1)
            if ee.activate and not ee.felled:
                if ee.rect.colliderect(ba.hitbox_rect) and ba.running and not ee.melee_attack_collisions:
                    # Reduce health from the mini boss from Players basic attack if not hit by that same attack swing
                    ee.health -= ba.damage
                    ee.melee_attack_collisions.append(1)

        if enemy.health <= 0:
            # despawns the enemy if their health is 0 or below
            xp.append(XP(enemy.rect.x + 18, enemy.rect.y + 17))
            if enemy in enemies:
                enemies.remove(enemy)
            chance = random.randint(1, 10)
            if chance <= 2:
                # chance for the player to get gold
                p.gold += 1
        if (enemy.rect.colliderect(p.rect) or enemy.north_rect.colliderect(p.rect) or
                enemy.east_rect.colliderect(p.rect) or enemy.south_rect.colliderect(p.rect) or
                enemy.west_rect.colliderect(p.rect)):
            # activates if the player collides with any of the slimes directional hitboxes
            if enemy.player_collide_counter >= 17:
                # measures how fast the player should take damage after entering collision with slime
                checkingDodge = random.randint(0, 100)
                if checkingDodge <= p.dodgeChance:
                    # dodges damage if dodge percent is rolled
                    enemy.player_collide_counter = 0
                else:
                    # have the player take damage
                    p.health -= 15
                    enemy.player_collide_counter = 0
            else:
                # increase counter if player is still colliding with enemy
                enemy.player_collide_counter += 1
        else:
            # reset counter
            enemy.player_collide_counter = 0

    for bat in bats:
        if not bat.spawned:
            pygame.draw.circle(screen, (160, 85, 150), (bat.rect.x, bat.rect.y), 16)
            bat.spawn_timer += 1
            if bat.spawn_timer >= 75:
                # bat.spawned.append(1)
                bat.spawned = True
                bat.spawn_indicator = None
        else:
            # go through bat animations and collision detection
            if bat.animation <= 15:
                screen.blit(pygame.transform.scale(batImg1, (45, 40)), (bat.rect.x - 2, bat.rect.y + 5))
                bat.animation += 1

            elif bat.animation <= 30:
                screen.blit(pygame.transform.scale(batImg2, (45, 40)), (bat.rect.x - 2, bat.rect.y + 5))
                bat.animation += 1

            elif bat.animation > 30:
                screen.blit(pygame.transform.scale(batImg1, (45, 40)), (bat.rect.x - 2, bat.rect.y + 5))
                bat.animation = 1

            bat.circle_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                 (bat.rect.x + 18, bat.rect.y + 17), 10)
            bat.middot_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                 (bat.rect.x + 16, bat.rect.y + 16), 1)
            # bat.generate_enemy()


            if b.shooting:
                for bullet in bullets:
                    # for each active bullet, if the bullet hits a bat, deal damage if appropriate conditions met.
                    if bat.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                        if not bat.bullet_collisions:
                            # if the bat has encountered it's first bullet, add to the list and take damage
                            bat.bullet_collisions.append(bullet)
                            bat.health -= b.damage
                        elif bat.bullet_collisions:
                            # if the list of bullets the bat has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                            i = 0
                            for l in bat.bullet_collisions:
                                if bullet.rect.x == bat.bullet_collisions[i].rect.x and bullet.rect.y == \
                                        bat.bullet_collisions[i].rect.y:
                                    pass
                                elif bullet not in bat.bullet_collisions and bullet.bullet_valid:
                                    bat.bullet_collisions.append(bullet)
                                    bat.health -= b.damage
                                i += 1
            for bullet in bullets:
                # for each active bullet, if the bullet hits a bat, deal damage if appropriate conditions met.
                if bat.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                    if not bat.bullet_collisions:
                        # if the bat has encountered it's first bullet, add to the list and take damage
                        bat.bullet_collisions.append(bullet)
                        bat.health -= b.damage
                    elif bat.bullet_collisions:
                        # if the list of bullets the bat has collided with is greater than 0,
                        # make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in bat.bullet_collisions:
                            if (bullet.rect.x == bat.bullet_collisions[i].rect.x and bullet.rect.y ==
                                    bat.bullet_collisions[i].rect.y):
                                pass
                            elif bullet not in bat.bullet_collisions and bullet.bullet_valid:
                                bat.bullet_collisions.append(bullet)
                                bat.health -= b.damage
                            i += 1

            if bat.rect.colliderect(ba.hitbox_rect) and ba.running and not bat.melee_attack_collisions:
                # Reduce bat health from the Players basic attack if not hit by that same attack swing
                bat.health -= ba.damage
                bat.melee_attack_collisions.append(1)

        if bat.health <= 0:
            # despawns the bat if their health is 0 or below
            xp.append(XP(bat.rect.x + 18, bat.rect.y + 17))
            if bat in bats:
                bats.remove(bat)
            chance = random.randint(1, 10)
            if chance <= 2:
                # chance for the player to get gold
                p.gold += 1

        if (bat.rect.colliderect(p.rect) or bat.north_rect.colliderect(p.rect) or
                bat.east_rect.colliderect(p.rect) or bat.south_rect.colliderect(p.rect) or
                bat.west_rect.colliderect(p.rect)):
            # activates if the player collides with any of the bats directional hitboxes
            if bat.player_collide_counter >= 17:
                # measures how fast the player should take damage after entering collision with bats
                checkingDodge = random.randint(0, 100)
                if checkingDodge <= p.dodgeChance:
                    # dodges damage if dodge percent is rolled
                    bat.player_collide_counter = 0
                else:
                    # have the player take damage
                    p.health -= 16
                    bat.player_collide_counter = 0

            else:
                # increase counter if player is still colliding with enemy
                bat.player_collide_counter += 1
        else:
            # reset counter
            bat.player_collide_counter = 0

    if int(minutes) == 0 and int(seconds) == 15:
        ee.activate = True
    if ee.activate and not ee.felled:
        ee.attack_timer = (pygame.time.get_ticks() / 1000)
        ee.aoe_hit()
        bup.rect.x = ee.rect.x
        bup.rect.y = ee.rect.y
        if ee.animation <= 15:
            screen.blit(pygame.transform.scale(minibee1, (40, 45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        elif ee.animation <= 30:
            screen.blit(pygame.transform.scale(minibee2, (40, 45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        elif ee.animation <= 45:
            screen.blit(pygame.transform.scale(minibee3, (40, 45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        elif ee.animation <= 60:
            screen.blit(pygame.transform.scale(minibee4, (40, 45)), (ee.rect.x, ee.rect.y))
            ee.animation += 1
        if ee.animation == 60:
            ee.animation = 0
        if ee.not_attacking:
            ee.follow_mc()
            ee.auto_hit_player()
    if ee.activate and not ee.felled:
        if b.shooting:
            for bullet in bullets:
                # for each active bullet, if the bullet hits ee, deal damage if appropriate.
                if ee.rect.colliderect(bullet.rect) and bullet.bullet_valid:

                    if not ee.bullet_collisions:
                        # If ee has been hit by its first bullet add to list to take damage.
                        ee.bullet_collisions.append(bullet)
                        ee.health -= b.damage
                        # print(ee.health)
                        # print('1')
                    elif ee.bullet_collisions:
                        # if the list of bullets that have collided ee is greater than 0, make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in ee.bullet_collisions:
                            if bullet.rect.x == ee.bullet_collisions[i].rect.x and bullet.rect.y == \
                                    ee.bullet_collisions[i].rect.y:
                                pass
                            elif bullet not in ee.bullet_collisions and bullet.bullet_valid:
                                ee.bullet_collisions.append(bullet)
                                ee.health -= b.damage
                                # print(ee.health)
                            i += 1
            for bullet in bullets:
                # removes expired bullets
                if bullet in ee.bullet_collisions and not ee.rect.colliderect(bullet.rect):
                    ee.bullet_collisions.remove(bullet)
            if ee.bullet_collisions:
                # backup to remove expired bullets from the bullet collision list
                for g in ee.bullet_collisions:
                    if not g.rect.colliderect(ee.rect):
                        ee.bullet_collisions.remove(g)
    if ee.health <= 0:
        # Makes sure ee is actually dead
        ee.felled = True
        ee.activate = False
    if ee.felled and bup.upgrade_active == False:
        bup.upgrade_out = True
        if p.orspeed > p.speed:
            p.speed = p.orspeed
        if bup.animation <= 15:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y))
            bup.animation += 1
        elif bup.animation <= 30:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y + 5))
            bup.animation += 1
        elif bup.animation <= 45:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y + 10))
            bup.animation += 1
        elif bup.animation <= 60:
            screen.blit(pygame.transform.scale(bullet_upgrade, (40, 45)), (bup.rect.x, bup.rect.y + 5))
            bup.animation += 1
        if bup.animation == 60:
            bup.animation = 0
    if p.rect.colliderect(bup.rect) and bup.upgrade_active == False and ee.felled:
        bup.upgrade_out = False
        b.shooting = True
        # b.overflow = (pygame.time.get_ticks() / 1000)
        bup.upgrade_active = True

    if int(minutes) == 1 and int(seconds) == 30:
        # skeleton king spawns once the game time reaches a minute and thirty seconds
        sk.activate = True

    if sk.activate and not sk.felled:
        # if the skeleton king has spawned and not been killed, have them follow around the player
        sk.generate_enemy()
        sk.follow_mc()
        sk.attack()

    if sk.activate and not sk.felled:
        # check for collisions for the skeleton king
        if b.shooting:
            for bullet in bullets:
                # for each active bullet, if the bullet hits the skeleton king boss,
                # deal damage if appropriate conditions met.
                if sk.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                    if not sk.bullet_collisions:
                        # if the skeleton king boss has encountered it's first bullet, add to the list and take damage
                        sk.bullet_collisions.append(bullet)
                        sk.health -= b.damage
                    elif sk.bullet_collisions:
                        # if the list of bullets the skeleton king boss has collided with is greater than 0,
                        # make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in sk.bullet_collisions:
                            if (bullet.rect.x == sk.bullet_collisions[i].rect.x and
                                    bullet.rect.y == sk.bullet_collisions[i].rect.y):
                                pass
                            elif bullet not in sk.bullet_collisions and bullet.bullet_valid:
                                # have the skeleton king take damage if hit with a bullet they havent been hit by
                                sk.bullet_collisions.append(bullet)
                                sk.health -= b.damage
                            i += 1
        for bullet in bullets:
            # removes expired bullets from the skeleton king boss bullet collision list
            if bullet in sk.bullet_collisions and not sk.rect.colliderect(bullet.rect):
                sk.bullet_collisions.remove(bullet)
                # print("BULLET REMOVED")
        if sk.bullet_collisions:
            # backup to remove expired bullets from the skeleton king boss bullet collision list
            for g in sk.bullet_collisions:
                if not g.rect.colliderect(sk.rect):
                    # removes collided bullet from skeleton kings bullet collisions list
                    sk.bullet_collisions.remove(g)

    if b.shooting:
        for bullet in bullets:
            # check if any of the bullets are actually still colliding with enemies,
            # if not, remove the bullet from the enemies' collision list
            counter = 0
            enemies_hit = []
            enemies_not_hit = []
            for enemy in enemies:
                # checking for if active and non-active bullets are colliding with enemies, and if not, remove those bullets
                # from the enemies bullet collision list
                if bullet.rect.colliderect(enemy.rect):
                    counter += 1
                    enemies_hit.append(enemy)
                else:
                    enemies_not_hit.append(enemy)
            if not counter:
                # if a bullet is no longer hitting the enemy it collided with before, then remove that bullet from the enemies bullet collision list
                for l in enemies_not_hit:
                    if bullet in l.bullet_collisions:
                        l.bullet_collisions.remove(bullet)
            if (
                    bullet.rect.x <= m.left_boundary_x or bullet.rect.x >= m.right_boundary_x or bullet.rect.y <= m.top_boundary_y or
                    bullet.rect.y >= m.bottom_boundary_y):
                # removes bullets if they go out of the map boundaries
                if bullet in bullets:
                    bullets.remove(bullet)

    for bullet in bullets:
        # check if any of the bullets are actually still colliding with enemies,
        # if not, remove the bullet from the enemies' collision list
        counter = 0
        bats_hit = []
        bats_not_hit = []
        for bat in bats:
            # checking for if active and non-active bullets are colliding with bats, and if not, remove those bullets
            # from the enemies bullet collision list
            if bullet.rect.colliderect(bat.rect):
                counter += 1
                bats_hit.append(bat)
            else:
                bats_not_hit.append(bat)
        if not counter:
            # if a bullet is no longer hitting the enemy it collided with before, then remove that bullet from the bats bullet collision list
            for l in bats_not_hit:
                if bullet in l.bullet_collisions:
                    l.bullet_collisions.remove(bullet)
        if (
                bullet.rect.x <= m.left_boundary_x or bullet.rect.x >= m.right_boundary_x or bullet.rect.y <= m.top_boundary_y or
                bullet.rect.y >= m.bottom_boundary_y):
            # removes bullets if they go out of the map boundaries
            if bullet in bullets:
                bullets.remove(bullet)

    if sk.health <= 0:
        # removes the skeleton king if they are at or below zero health
        sk.felled = True
        sk.activate = False
        sk.rect = None

    # for bat in bats:
    #     if bat.bulletValid:
    #         if bat.bulletRect.colliderect(p.rect):
    #             print("YEPPPPPPPPPPPPPPPPPPP")
    for bat in bats:
        # pygame.draw.circle(screen, (167,28,111), (bat.bulletRect.x, bat.bulletRect.y), 12)
        bat.decide_action()

    # pygame.draw.rect(screen, (0,255,0), p.rect)
    # for bat in bats:
        # pygame.draw.rect(screen, (0,255,0), bat.bulletRect)
        # pygame.draw.rect(screen, (0,255,0), bat.rect)

        # if bat.bulletRect.colliderect(p.rect):
        #     print("HIT!")
    b.bullet_counter += 1
    ba.attack()
    m.update_boundary()
    display_timer(gameTimeStr, timer_font, (0, 0, 0))
    display_fps(fps, fps_font, (0, 255, 0))
    p.display_health()
    xpB.show_xp_bar()
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
