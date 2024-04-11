import sys, pygame, csv, os, numpy, random, math, player

# initializes the pygame library
pygame.init()

# creates the window and dimensions for the game
screen_size_stuff = pygame.display.Info()
screen_size_height, screen_size_width = screen_size_stuff.current_h, screen_size_stuff.current_w
screen = pygame.display.set_mode((screen_size_width / 2, screen_size_height/ 1.25))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
transparent_surface = pygame.Surface((800, 800), pygame.SRCALPHA)
# sets the window caption at the top
pygame.display.set_caption("Rogue Survival")
pygame.key.set_repeat()

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

level_scroll = pygame.image.load("./images/level_scroll.png").convert_alpha()

crit_img = pygame.image.load("./images/crit.png").convert_alpha()
dodge_img = pygame.image.load("./images/dodge.png").convert_alpha()
gold_img = pygame.image.load("./images/gold.png").convert_alpha()
lifesteal_img = pygame.image.load("./images/lifesteal.png").convert_alpha()
maxhealth_img = pygame.image.load("./images/maxhealth.png").convert_alpha()
regen_img = pygame.image.load("./images/regen.png").convert_alpha()
revive_img = pygame.image.load("./images/revive2.png").convert_alpha()
movementspeed_img = pygame.image.load("./images/speed.png").convert_alpha()


# instantiating pause and gameTime function for later
screen_height = 800
screen_width = 800
isFullscreen = False
gameTime = 0
pause = True
# instantiating the XP arrays
xp = []
xp_hit = []


input_csv = './game-data/profile-data.csv'
output_csv = './game-data/new-profile-data.csv'


class ProfileData:

    def __init__(self):
        self.empty = True
        self.new_file_data = []

        self.upgrade1_level = 0
        self.upgrade2_level = 0
        self.upgrade3_level = 0
        self.upgrade4_level = 0
        self.upgrade5_level = 0
        self.upgrade6_level = 0
        self.upgrade7_level = 0
        self.upgrade8_level = 0

        self.balance = 0
        self.profile_id = 0

    def check_empty(self):
        csv_file = './game-data/profile-data.csv'
        game_data_folder = './game-data'
        exists_file = os.path.exists(csv_file)
        exists_folder = os.path.exists(game_data_folder)
        # print(exists_file)
        # print(exists_folder)
        if not exists_folder:
            os.mkdir("./game-data")
        if not exists_file:
            open("./game-data/profile-data.csv", "x")
        with open('./game-data/profile-data.csv', 'r') as p_data:
            p_reader = csv.reader(p_data)

            count = 0
            for line in p_reader:
                self.empty = False
                count += 1
            if count <= 1:
                self.empty = True
            if self.empty:
                # print("EMPTY")
                self.create_csv()

    def create_csv(self):
        if self.empty:
            with open('./game-data/profile-data.csv', 'w') as p_data:
                p_writer = csv.writer(p_data, lineterminator= '\n')
                data0 = ["profile_id", "currency", "selected_profile", "upgrade1_level", "upgrade2_level", "upgrade3_level", "upgrade4_level", "upgrade5_level", "upgrade6_level", "upgrade7_level", "upgrade8_level"]
                data1 = [1, 0, "not-selected", 0, 0, 0, 0, 0, 0, 0, 0]
                data2 = [2, 0, "not-selected", 0, 0, 0, 0, 0, 0, 0, 0]
                data3 = [3, 0, "selected", 0, 0, 0, 0, 0, 0, 0, 0]
                data4 = [4, 0, "not-selected", 0, 0, 0, 0, 0, 0, 0, 0]
                data5 = [5, 0, "not-selected", 0, 0, 0, 0, 0, 0, 0, 0]
                p_writer.writerow(data0)
                p_writer.writerow(data1)
                p_writer.writerow(data2)
                p_writer.writerow(data3)
                p_writer.writerow(data4)
                p_writer.writerow(data5)
                # print("file created")

    def add_gold(self):

        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[2] == 'selected':
                    current_gold = int(float(line[1]))
                    gold_earned = p.gold
                    line[1] = f'{current_gold + gold_earned}'
                p_writer.writerow(line)

        with open(output_csv, 'r') as p_data_read, open(input_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')
            for line in p_reader: # append everything from the updated file so we can later use it to write over the original file
                self.new_file_data.append(line)

            for g in self.new_file_data: # write data from updated file to original file
                p_writer.writerow(g)
            self.new_file_data.clear()


    def load_skill_tree(self):
        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[2] == 'selected':
                    st.upgrade1_level = int(line[3])
                    st.upgrade2_level = int(line[4])
                    st.upgrade3_level = int(line[5])
                    st.upgrade4_level = int(line[6])
                    st.upgrade5_level = int(line[7])
                    st.upgrade6_level = int(line[8])
                    st.upgrade7_level = int(line[9])
                    st.upgrade8_level = int(line[10])

                    st.balance = int(float(line[1]))

    def subtract_gold(self, purchase_price):
        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[2] == 'selected':
                    current_gold = int(float(line[1]))
                    line[1] = f'{current_gold - purchase_price}'
                    st.balance = int(float(line[1]))
                p_writer.writerow(line)

        with open(output_csv, 'r') as p_data_read, open(input_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')
            for line in p_reader: # append everything from the updated file so we can later use it to write over the original file
                self.new_file_data.append(line)

            for g in self.new_file_data: # write data from updated file to original file
                p_writer.writerow(g)
            self.new_file_data.clear()

    def increase_upgrade_level(self, column):
        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[2] == 'selected':
                    current_level = int(line[column])
                    line[column] = f'{current_level + 1}'
                p_writer.writerow(line)

        with open(output_csv, 'r') as p_data_read, open(input_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')
            for line in p_reader: # append everything from the updated file so we can later use it to write over the original file
                self.new_file_data.append(line)

            for g in self.new_file_data: # write data from updated file to original file
                p_writer.writerow(g)
            self.new_file_data.clear()

    def load_upgrades_into_game(self):
        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[2] == 'selected':
                    self.upgrade1_level = int(line[3])
                    self.upgrade2_level = int(line[4])
                    self.upgrade3_level = int(line[5])
                    self.upgrade4_level = int(line[6])
                    self.upgrade5_level = int(line[7])
                    self.upgrade6_level = int(line[8])
                    self.upgrade7_level = int(line[9])
                    self.upgrade8_level = int(line[10])
                    self.balance = int(float(line[1]))
                    self.profile_id = int(line[0])

    def change_profile(self, profile):
        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[2] == 'selected':
                    line[2] = "not-selected"
                p_writer.writerow(line)

        with open(output_csv, 'r') as p_data_read, open(input_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')
            for line in p_reader: # append everything from the updated file so we can later use it to write over the original file
                self.new_file_data.append(line)

            for g in self.new_file_data: # write data from updated file to original file
                p_writer.writerow(g)
            self.new_file_data.clear()




        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[0] == str(profile):
                    line[2] = "selected"
                p_writer.writerow(line)

        with open(output_csv, 'r') as p_data_read, open(input_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')
            for line in p_reader: # append everything from the updated file so we can later use it to write over the original file
                self.new_file_data.append(line)

            for g in self.new_file_data: # write data from updated file to original file
                p_writer.writerow(g)
            self.new_file_data.clear()

    def reset_profile(self, profile):
        with open(input_csv, 'r') as p_data_read, open(output_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')

            for line in p_reader:
                if line[0] == str(profile) and line[2] == 'selected':
                    line[1] = '0'
                    line[3] = '0'
                    line[4] = '0'
                    line[5] = '0'
                    line[6] = '0'
                    line[7] = '0'
                    line[8] = '0'
                    line[9] = '0'
                    line[10] = '0'
                p_writer.writerow(line)

        with open(output_csv, 'r') as p_data_read, open(input_csv, 'w', newline='') as p_data_write:
            p_reader = csv.reader(p_data_read, delimiter=',')
            p_writer = csv.writer(p_data_write, delimiter=',')
            for line in p_reader: # append everything from the updated file so we can later use it to write over the original file
                self.new_file_data.append(line)

            for g in self.new_file_data: # write data from updated file to original file
                p_writer.writerow(g)
            self.new_file_data.clear()



pd = ProfileData()
pd.check_empty()

# pd.add_gold()


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
        self.speed = 4 + (.05 * pd.upgrade4_level)
        self.max_health = 5000000 + (10 * pd.upgrade1_level)
        self.current_health = self.max_health
        self.generated_health = False
        self.revive_available = True
        self.dodge_chance = 0.02 * pd.upgrade5_level
        self.critial_chance = 0.03 * pd.upgrade6_level
        self.life_steal_chance = 0.02 * pd.upgrade8_level
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
        # print(self.gold)
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
        # displays health to the screen
        health_string = f"HP: {str(int(self.current_health))}"
        health_display = self.health_font.render(health_string, True, (255, 0, 0))
        screen.blit(health_display, ((tempwidth/2)-50, 20))

    def check_dodge_chance(self):
        if self.dodge_chance:
            random_number = random.randint(0, 100)
            if random_number <= (100 * self.dodge_chance):
                return True
        return False

    def check_critical_chance(self):
        if self.critial_chance:
            random_number = random.randint(0, 100)
            if random_number <= (100 * self.critial_chance):
                return True
        return False

    def check_life_steal_chance(self):
        if self.life_steal_chance:
            random_number = random.randint(0, 100)
            if random_number <= (100 * self.life_steal_chance):
                return True
        return False

    def add_life_steal_health(self):
        if self.life_steal_chance:
            if self.current_health + (100 * self.life_steal_chance) <= self.max_health:
                self.current_health += (100 * self.life_steal_chance)
            else:
                self.current_health = self.max_health

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

                bat.bullet_rect.x += self.speed
                if bat.bullet_valid:
                    bat.player_pos[0] += self.speed
                    bat.starting_point[0] += self.speed
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
            if com.activate and not com.felled:
                com.rect.x += self.speed
                com.north_rect.x = com.rect.x + com.north_x_val
                com.east_rect.x = com.rect.x + com.east_x_val
                com.south_rect.x = com.rect.x + com.south_x_val
                com.west_rect.x = com.rect.x - com.west_x_val
            if ma.activate and not ma.felled:
                ma.rect.x += self.speed
                ma.px += self.speed
                ma.seekerx += self.speed
                ma.north_rect.x = ma.rect.x + ma.north_x_val
                ma.east_rect.x = ma.rect.x + ma.east_x_val
                ma.south_rect.x = ma.rect.x + ma.south_x_val
                ma.west_rect.x = ma.rect.x - ma.west_x_val

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

                bat.bullet_rect.x -= self.speed
                if bat.bullet_valid:
                    bat.player_pos[0] -= self.speed
                    bat.starting_point[0] -= self.speed
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
            if com.activate and not com.felled:
                com.rect.x -= self.speed
                com.north_rect.x = com.rect.x + com.north_x_val
                com.east_rect.x = com.rect.x + com.east_x_val
                com.south_rect.x = com.rect.x + com.south_x_val
                com.west_rect.x = com.rect.x - com.west_x_val
            if ma.activate and not ma.felled:
                ma.rect.x -= self.speed
                ma.px -= self.speed
                ma.seekerx -= self.speed
                ma.north_rect.x = ma.rect.x + ma.north_x_val
                ma.east_rect.x = ma.rect.x + ma.east_x_val
                ma.south_rect.x = ma.rect.x + ma.south_x_val
                ma.west_rect.x = ma.rect.x - ma.west_x_val

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

                bat.bullet_rect.y += self.speed
                if bat.bullet_valid:
                    bat.player_pos[1] += self.speed
                    bat.starting_point[1] += self.speed
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
            if com.activate and not com.felled:
                com.rect.y += self.speed
                com.north_rect.y = com.rect.y - com.north_y_val
                com.east_rect.y = com.rect.y + com.east_y_val
                com.south_rect.y = com.rect.y + com.south_y_val
                com.west_rect.y = com.rect.y + com.west_y_val
            if ma.activate and not ma.felled:
                ma.rect.y += self.speed
                ma.py += self.speed
                ma.seekery += self.speed
                ma.north_rect.y = ma.rect.y - ma.north_y_val
                ma.east_rect.y = ma.rect.y + ma.east_y_val
                ma.south_rect.y = ma.rect.y + ma.south_y_val
                ma.west_rect.y = ma.rect.y + ma.west_y_val

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

                bat.bullet_rect.y -= self.speed
                if bat.bullet_valid:
                    bat.player_pos[1] -= self.speed
                    bat.starting_point[1] -= self.speed
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
            if com.activate and not com.felled:
                com.rect.y -= self.speed
                com.north_rect.y = com.rect.y - com.north_y_val
                com.east_rect.y = com.rect.y + com.east_y_val
                com.south_rect.y = com.rect.y + com.south_y_val
                com.west_rect.y = com.rect.y + com.west_y_val
            if ma.activate and not ma.felled:
                ma.rect.y -= self.speed
                ma.py -= self.speed
                ma.seekery -= self.speed


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
        # print(pd.upgrade7_level)
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
            if ee.activate and not ee.felled:
                ee.melee_attack_collisions.clear()
            if com.activate and not com.felled:
                com.melee_attack_collisions.clear()
            if ma.activate and not ma.felled:
                ma.melee_attack_collisions.clear()
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

    def generate_entity(self):
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

    def check_collisions(self):
        self.upgrade_out = False
        self.upgrade_active = True
        b.shooting = True


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
        self.maxhealth = 50
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
        self.edamage = 15
        self.wasbuffed = False
        self.death = False

    def generate_enemy(self):
        if not self.spawned:
            pygame.draw.circle(screen, (128, 0, 32), (self.rect.x, self.rect.y), 16)
            self.spawn_timer += 1
            if self.spawn_timer >= 75:
                self.spawned.append(1)
                self.spawn_indicator = None
        else:
            # if enemy has spawned, go through the animations and collision detection
            if self.animation <= 15:
                screen.blit(pygame.transform.scale(enemy4, (45, 40)), (self.rect.x - 6, self.rect.y - 6))
                self.animation += 1

            elif self.animation <= 30:
                screen.blit(pygame.transform.scale(enemy3, (45, 40)), (self.rect.x - 6, self.rect.y - 6))
                self.animation += 1

            elif self.animation <= 45:
                screen.blit(pygame.transform.scale(enemy2, (45, 40)), (self.rect.x - 6, self.rect.y - 6))
                self.animation += 1

            elif self.animation <= 60:
                screen.blit(pygame.transform.scale(enemy1, (45, 40)), (self.rect.x - 6, self.rect.y - 6))
                self.animation += 1

            elif self.animation > 60:
                screen.blit(pygame.transform.scale(enemy4, (45, 40)), (self.rect.x - 6, self.rect.y - 6))
                self.animation = 1

            # screen.blit(pygame.transform.scale(enemyOriginal, (45, 40)), (enemy.rect.x, enemy.rect.y))
            self.circle_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                   (self.rect.x + 18, self.rect.y + 17), 10)
            self.middot_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                   (self.rect.x + 16, self.rect.y + 16), 8)
            self.follow_mc()

    def check_collisions(self):
        if b.shooting:
            for bullet in bullets:
                # for each active bullet, if the bullet hits an enemy, deal damage if appropriate conditions met.
                if self.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                    if not self.bullet_collisions:
                        # if the enemy has encountered it's first bullet, add to the list and take damage
                        self.bullet_collisions.append(bullet)
                        critical = p.check_critical_chance()
                        if critical:
                            self.health -= (b.damage * 1.5)
                        else:
                            self.health -= b.damage
                        life_steal = p.check_life_steal_chance()
                        if life_steal:
                            p.add_life_steal_health()
                    elif self.bullet_collisions:
                        # if the list of bullets the enemy has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in self.bullet_collisions:
                            if bullet.rect.x == self.bullet_collisions[i].rect.x and bullet.rect.y == \
                                    self.bullet_collisions[i].rect.y:
                                pass
                            elif bullet not in self.bullet_collisions and bullet.bullet_valid:
                                self.bullet_collisions.append(bullet)
                                critical = p.check_critical_chance()
                                if critical:
                                    self.health -= (b.damage * 1.5)
                                else:
                                    self.health -= b.damage
                                life_steal = p.check_life_steal_chance()
                                if life_steal:
                                    p.add_life_steal_health()
                            i += 1
        for bullet in bullets:
            # for each active bullet, if the bullet hits an enemy, deal damage if appropriate conditions met.
            if self.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                if not self.bullet_collisions:
                    # if the enemy has encountered it's first bullet, add to the list and take damage
                    self.bullet_collisions.append(bullet)
                    critical = p.check_critical_chance()
                    if critical:
                        self.health -= (b.damage * 1.5)
                    else:
                        self.health -= b.damage
                    life_steal = p.check_life_steal_chance()
                    if life_steal:
                        p.add_life_steal_health()
                elif self.bullet_collisions:
                    # if the list of bullets the enemy has collided with is greater than 0,
                    # make sure it is a different bullet in order to deal damage
                    i = 0
                    for l in self.bullet_collisions:
                        if (bullet.rect.x == self.bullet_collisions[i].rect.x and
                                bullet.rect.y == self.bullet_collisions[i].rect.y):
                            pass
                        elif bullet not in self.bullet_collisions and bullet.bullet_valid:
                            self.bullet_collisions.append(bullet)
                            critical = p.check_critical_chance()
                            if critical:
                                self.health -= (b.damage * 1.5)
                            else:
                                self.health -= b.damage
                            life_steal = p.check_life_steal_chance()
                            if life_steal:
                                p.add_life_steal_health()
                        i += 1

        if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
            # Reduce enemy health from the Players basic attack if not hit by that same attack swing
            critical = p.check_critical_chance()
            if critical:
                self.health -= (ba.damage * 1.5)
            else:
                self.health -= ba.damage
            life_steal = p.check_life_steal_chance()
            if life_steal:
                p.add_life_steal_health()

            self.melee_attack_collisions.append(1)

        if (self.rect.colliderect(p.rect) or self.north_rect.colliderect(p.rect) or
                self.east_rect.colliderect(p.rect) or self.south_rect.colliderect(p.rect) or
                self.west_rect.colliderect(p.rect)):
            # activates if the player collides with any of the slimes directional hitboxes
            if self.player_collide_counter >= 17:
                # measures how fast the player should take damage after entering collision with slime
                dodge = p.check_dodge_chance()
                if not dodge:
                    # have the player take damage
                    p.current_health -= self.edamage
                    self.player_collide_counter = 0
                else:
                    self.player_collide_counter = 0
            else:
                # increase counter if player is still colliding with enemy
                self.player_collide_counter += 1
        else:
            # reset counter
            self.player_collide_counter = 0

    def activate_death(self):
        if self.health <= 0:
            self.death = True
            # despawns the enemy if their health is 0 or below
            xp.append(XP(self.rect.x + 18, self.rect.y + 17))
            if self in enemies:
                enemies.remove(self)
            chance = random.randint(1, 10)
            if chance <= 3:
                # chance for the player to get gold
                p.gold += 1 + (1 * pd.upgrade6_level)

    def spawn(self):
        # allows programmer to know if this enemy has spawned
        self.spawned.append(1)

    def clean_dictionaries(self):
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
        self.health = 55
        self.speed = random.uniform(.6, .8)
        self.follow_mc()
        self.travel_north()
        self.travel_east()
        self.travel_south()
        self.travel_west()
        self.bat = True
        self.player_pos = ()
        self.found = False
        self.bullet_rect = pygame.draw.circle(transparent_surface, (128,12,128), (self.rect.x, self.rect.y), 12)
        self.bullet_speed = 25/3
        self.spawned2 = []
        self.position_reached = False
        self.go_fourth_a = False
        self.go_third_a = False
        self.go_second_a = False
        self.go_first_a = False
        self.angle = 0
        self.counter = 0
        self.target_x = 0
        self.target_y = 0
        self.starting_point = []
        self.shoot_timer = 0
        self.bullet_valid = False
        self.hit_counter = 0
        self.spawned = False

    def generate_enemy(self):
        if not self.spawned:
            pygame.draw.circle(screen, (160, 85, 150), (self.rect.x, self.rect.y), 16)
            self.spawn_timer += 1
            if self.spawn_timer >= 75:
                # self.spawned.append(1)
                self.spawned = True
                self.spawn_indicator = None
        else:
            # go through bat animations and collision detection
            if self.animation <= 15:
                screen.blit(pygame.transform.scale(batImg1, (45, 40)), (self.rect.x - 2, self.rect.y + 5))
                self.animation += 1

            elif self.animation <= 30:
                screen.blit(pygame.transform.scale(batImg2, (45, 40)), (self.rect.x - 2, self.rect.y + 5))
                self.animation += 1

            elif self.animation > 30:
                screen.blit(pygame.transform.scale(batImg1, (45, 40)), (self.rect.x - 2, self.rect.y + 5))
                self.animation = 1

            self.circle_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                 (self.rect.x + 18, self.rect.y + 17), 10)
            self.middot_rect = pygame.draw.circle(transparent_surface, (0, 50, 0, 100),
                                                 (self.rect.x + 16, self.rect.y + 16), 1)

    def check_collisions(self):
        if b.shooting:
            for bullet in bullets:
                # for each active bullet, if the bullet hits a bat, deal damage if appropriate conditions met.
                if self.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                    if not self.bullet_collisions:
                        # if the bat has encountered it's first bullet, add to the list and take damage
                        self.bullet_collisions.append(bullet)
                        critical = p.check_critical_chance()
                        if critical:
                            self.health -= (b.damage * 1.5)
                        else:
                            self.health -= b.damage
                        life_steal = p.check_life_steal_chance()
                        if life_steal:
                            p.add_life_steal_health()
                    elif self.bullet_collisions:
                        # if the list of bullets the bat has collided with is greater than 0, make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in self.bullet_collisions:
                            if bullet.rect.x == self.bullet_collisions[i].rect.x and bullet.rect.y == \
                                    self.bullet_collisions[i].rect.y:
                                pass
                            elif bullet not in self.bullet_collisions and bullet.bullet_valid:
                                self.bullet_collisions.append(bullet)
                                critical = p.check_critical_chance()
                                if critical:
                                    self.health -= (b.damage * 1.5)
                                else:
                                    self.health -= b.damage
                                life_steal = p.check_life_steal_chance()
                                if life_steal:
                                    p.add_life_steal_health()
                            i += 1

        for bullet in bullets:
            # for each active bullet, if the bullet hits a bat, deal damage if appropriate conditions met.
            if self.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                if not self.bullet_collisions:
                    # if the bat has encountered it's first bullet, add to the list and take damage
                    self.bullet_collisions.append(bullet)
                    critical = p.check_critical_chance()
                    if critical:
                        self.health -= (b.damage * 1.5)
                    else:
                        self.health -= b.damage
                    life_steal = p.check_life_steal_chance()
                    if life_steal:
                        p.add_life_steal_health()
                elif self.bullet_collisions:
                    # if the list of bullets the bat has collided with is greater than 0,
                    # make sure it is a different bullet in order to deal damage
                    i = 0
                    for l in self.bullet_collisions:
                        if (bullet.rect.x == self.bullet_collisions[i].rect.x and bullet.rect.y ==
                                self.bullet_collisions[i].rect.y):
                            pass
                        elif bullet not in self.bullet_collisions and bullet.bullet_valid:
                            self.bullet_collisions.append(bullet)
                            critical = p.check_critical_chance()
                            if critical:
                                self.health -= (b.damage * 1.5)
                            else:
                                self.health -= b.damage
                            life_steal = p.check_life_steal_chance()
                            if life_steal:
                                p.add_life_steal_health()
                        i += 1

        if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
            # Reduce bat health from the Players basic attack if not hit by that same attack swing
            critical = p.check_critical_chance()
            if critical:
                self.health -= (ba.damage * 1.5)
            else:
                self.health -= ba.damage
            life_steal = p.check_life_steal_chance()
            if life_steal:
                p.add_life_steal_health()
            self.melee_attack_collisions.append(1)

        if (self.rect.colliderect(p.rect) or self.north_rect.colliderect(p.rect) or
                self.east_rect.colliderect(p.rect) or self.south_rect.colliderect(p.rect) or
                self.west_rect.colliderect(p.rect)):
            # activates if the player collides with any of the bats directional hitboxes
            if self.player_collide_counter >= 17:
                # measures how fast the player should take damage after entering collision with bats
                dodge = p.check_dodge_chance()
                if not dodge:
                    # have the player take damage
                    p.current_health -= self.edamage + 1
                    self.player_collide_counter = 0
                else:
                    self.player_collide_counter = 0
            else:
                # increase counter if player is still colliding with enemy
                self.player_collide_counter += 1
        else:
            # reset counter
            self.player_collide_counter = 0

    def clean_dictionaries(self):
        if b.shooting:
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

    def activate_death(self):
        if self.health <= 0:
            # despawns the bat if their health is 0 or below
            xp.append(XP(self.rect.x + 18, self.rect.y + 17))
            if self in bats:
                bats.remove(self)
            chance = random.randint(1, 10)
            if chance <= 3:
                # chance for the player to get gold
                p.gold += 1 + (1 * pd.upgrade6_level)

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
                self.target_x = p.rect.x+18
                self.target_y = p.rect.y+17
                self.starting_point = [self.rect.x, self.rect.y]
                self.player_pos = [self.target_x, self.target_y]
                self.bullet_rect.x = self.rect.x
                self.bullet_rect.y = self.rect.y

                if self.target_x > self.starting_point[0] and self.target_y < self.starting_point[1]:
                    # first quadrant
                    newTriangle = pygame.math.Vector2(self.target_x - self.starting_point[0], self.target_y - self.starting_point[1])
                    self.angle = -(numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
                elif self.target_x > self.starting_point[0] and self.target_y > self.starting_point[1]:
                    # fourth quadrant
                    newTriangle = pygame.math.Vector2(self.target_x - self.starting_point[0], self.target_y - self.starting_point[1])
                    self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
                elif self.target_x < self.starting_point[0] and self.target_y < self.starting_point[1]:
                    # second quadrant
                    newTriangle = pygame.math.Vector2(self.starting_point[0] - self.target_x, self.starting_point[1] - self.target_y)
                    self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))
                elif self.target_x < self.starting_point[0] and self.target_y > self.starting_point[1]:
                    # third quadrant
                    newTriangle = pygame.math.Vector2(self.starting_point[0] - self.target_x, self.starting_point[1] - self.target_y)
                    self.angle = (numpy.rad2deg(numpy.arctan(newTriangle[1]/newTriangle[0])))

                self.found = True
                self.shoot()

    def shoot(self):
        if self.spawned:
            if not self.found:
                self.find_angle()
            if self.counter >= 150:
                self.bullet_rect.x = self.rect.x
                self.bullet_rect.y = self.rect.y
                self.bullet_rect = pygame.draw.circle(transparent_surface, (128,12,128), (self.rect.x, self.rect.y), 12)
                self.bullet_valid = False
                self.position_reached = False
                self.go_fourth_a = False
                self.go_third_a = False
                self.go_second_a = False
                self.go_first_a = False
                self.found = False
                self.counter = 0
                self.shoot_timer = 0
                self.player_pos = ()
                self.angle = 0
                self.hit_counter = 0
                # print("RESET")

            else:
                self.bullet_valid = True

                if self.bullet_rect.x <= self.player_pos[0] and self.bullet_rect.y <= self.player_pos[1] and not self.go_first_a and not self.go_second_a and not self.go_third_a or self.go_fourth_a:
                    # fourth quadrant - travels to mouse position
                    self.bullet_rect.y += math.sin(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.bullet_rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.go_fourth_a = True
                    # print(self.angle)
                    # print("YUHH")
                    # self.bullet_rect.y += self.bullet_speed
                    # self.bullet_rect.x += self.bullet_speed

                elif self.bullet_rect.x >= self.player_pos[0] and self.bullet_rect.y <= self.player_pos[1] and not self.go_first_a and not self.go_second_a and not self.go_fourth_a or self.go_third_a:
                    # third quadrant - travels to mouse position
                    self.bullet_rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.bullet_rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.go_third_a = True
                    # print("OOOOOOO")
                    # self.bullet_rect.y -= self.bullet_speed
                    # self.bullet_rect.x -= self.bullet_speed

                elif self.bullet_rect.x >= self.player_pos[0] and self.bullet_rect.y >= self.player_pos[1] and not self.go_first_a and not self.go_third_a and not self.go_fourth_a or self.go_second_a:
                    # second quadrant - travels to mouse position
                    self.bullet_rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.bullet_rect.x -= math.cos(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.go_second_a = True
                    # print("AHHHHHH")
                    # self.bullet_rect.y -= self.bullet_speed
                    # self.bullet_rect.x -= self.bullet_speed

                elif self.bullet_rect.x <= self.player_pos[0] and self.bullet_rect.y >= self.player_pos[1] and not self.go_second_a and not self.go_third_a and not self.go_fourth_a or self.go_first_a:
                    # first quadrant - travels to mouse position
                    self.bullet_rect.y -= math.sin(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.bullet_rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bullet_speed
                    self.go_first_a = True
                    # print("EEEEEEE")
                    # self.bullet_rect.y -= self.bullet_speed
                    # self.bullet_rect.x += self.bullet_speed

                # else:
                #     print("NUUUUUU")
                #     # if self.player_pos[1] == self.starting_point
                #     if self.player_pos[1] >= self.starting_point[1] and (abs(self.player_pos[0]) - self.starting_point[0]) < 15:
                #         self.bullet_rect.y += math.sin(90 * (2*math.pi/360)) * self.bullet_speed
                #     elif self.player_pos[1] <= self.starting_point[1] and (abs(self.player_pos[0]) - self.starting_point[0]) < 15:
                #         self.bullet_rect.y -= math.sin(90 * (2*math.pi/360)) * self.bullet_speed
                #     elif abs(self.player_pos[1] - self.starting_point[1]) <= 5 and self.player_pos[0] >= self.starting_point[0]:
                #         self.bullet_rect.x += math.cos(self.angle * (2*math.pi/360)) * self.bullet_speed
                # self.bullet_rect = pygame.draw.circle(screen, (128,12,128), (self.bullet_rect.x, self.bullet_rect.y), 12)

                pygame.draw.circle(screen, (167,28,111), (self.bullet_rect.x+12, self.bullet_rect.y+12), 12)



                # pygame.draw.rect(screen, (100,0,255), self.bullet_rect)
                if self.bullet_rect.colliderect(p.rect) and not self.hit_counter:
                    dodge = p.check_dodge_chance()
                    if not dodge:
                        p.current_health -= self.edamage
                        self.hit_counter += 1
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
        self.health = 5
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
        self.attackcounter = 0.0

    def generate_enemy(self):
        self.attack_timer = (pygame.time.get_ticks() / 1000)
        self.aoe_hit()
        bup.rect.x = self.rect.x
        bup.rect.y = self.rect.y
        if self.animation <= 15:
            screen.blit(pygame.transform.scale(minibee1, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 30:
            screen.blit(pygame.transform.scale(minibee2, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 45:
            screen.blit(pygame.transform.scale(minibee3, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 60:
            screen.blit(pygame.transform.scale(minibee4, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        if self.animation == 60:
            self.animation = 0
        if self.not_attacking:
            self.follow_mc()
            self.auto_hit_player()

    def check_collisions(self):
        if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
            # Reduce health from the mini boss from Players basic attack if not hit by that same attack swing
            critical = p.check_critical_chance()
            if critical:
                self.health -= (ba.damage * 1.5)
            else:
                self.health -= ba.damage
            life_steal = p.check_life_steal_chance()
            if life_steal:
                p.add_life_steal_health()
            self.melee_attack_collisions.append(1)

    def activate_death(self):
        if self.health <= 0:
            p.gold += 20
            # Makes sure ee is actually dead
            self.felled = True
            self.activate = False

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
        if self.is_attacking and self.attackcounter < 3.0:
            self.attackcounter +=.03
            self.attack_area = pygame.draw.circle(screen, (252, 161, 3), (self.rect.x + 18, self.rect.y + 20), 240, 1)
            self.rumble_area = pygame.draw.circle(screen, (209, 10, 10), (self.rect.x + 18, self.rect.y + 20),
                                                  ((self.attackcounter) * 80), 1)
            if p.rect.colliderect(self.rumble_area):
                p.speed = self.rumble_speed
            else:
                p.speed = p.orspeed
            if self.attackcounter >= 3.0:
                self.attacrect = self.attack_area = pygame.draw.circle(screen, (209, 10, 10),
                                                                       (self.rect.x + 18, self.rect.y + 20), 240, 1)
                if p.rect.colliderect(self.attacrect):
                    dodge = p.check_dodge_chance()
                    if not dodge:
                        p.current_health -= 50
                        # print("Player hit")
                        # print(p.health)
            if self.attackcounter >= 3.0:
                self.not_attacking = True
                self.is_attacking = False
                self.attack_area = None
                self.attack_rect = None
                p.speed = p.orspeed
                self.attackcounter = 0

    def auto_hit_player(self):
        if self.rect.colliderect(p.rect) and (self.attack_timer - self.last_auto) >= self.attack_speed:
            dodge = p.check_dodge_chance()
            if not dodge:
                self.last_auto = self.attack_timer
                p.current_health -= self.hit_damage

class Commander(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = minibee1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 20
        self.health = 1000
        self.speed = 2
        self.travel_north()
        self.travel_east()
        self.travel_south()
        self.travel_west()
        self.felled = False
        self.not_attacking = True
        self.hit_damage = 50
        self.last_auto = 0
        self.attack_speed = 5
        self.speed = 1
        self.buffarea = None
        self.orspeed = 0
        self.shouttimer = 15
        self.shoutarea = None
        self.shout = False
        self.activate = False
        self.shoutcounter = 0
    def activate_death(self):
        if self.health <= 0:
            p.gold += 25
            # Makes sure Comander is actually dead
            self.felled = True

    def check_collisions(self):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                if not self.bullet_collisions:
                    self.bullet_collisions.append(bullet)
                    critical = p.check_critical_chance()
                    if critical:
                        self.health -= (b.damage * 1.5)
                    else:
                        self.health -= b.damage
                    life_steal = p.check_life_steal_chance()
                    if life_steal:
                        p.add_life_steal_health()
                elif self.bullet_collisions:
                    i = 0
                    for l in self.bullet_collisions:
                        if (bullet.rect.x == self.bullet_collisions[i].rect.x and bullet.rect.y ==
                                self.bullet_collisions[i].rect.y):
                            pass
                        elif bullet not in self.bullet_collisions and bullet.bullet_valid:
                            self.bullet_collisions.append(bullet)
                            critical = p.check_critical_chance()
                            if critical:
                                self.health -= (b.damage * 1.5)
                            else:
                                self.health -= b.damage
                            life_steal = p.check_life_steal_chance()
                            if life_steal:
                                p.add_life_steal_health()
                        i += 1
            for bullet in bullets:
                # removes expired bullets
                if bullet in self.bullet_collisions and not self.rect.colliderect(bullet.rect):
                    self.bullet_collisions.remove(bullet)
                    # print("BULLET REMOVED")
            if self.bullet_collisions:
                # backup to remove expired bullets
                for g in self.bullet_collisions:
                    if not g.rect.colliderect(self.rect):
                        # removes collided bullet
                        self.bullet_collisions.remove(g)
            if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
                critical = p.check_critical_chance()
                if critical:
                    self.health -= (ba.damage * 1.5)
                else:
                    self.health -= ba.damage
                life_steal = p.check_life_steal_chance()
                if life_steal:
                    p.add_life_steal_health()
                self.melee_attack_collisions.append(1)
        if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
            # Reduce health from the mini boss from Players basic attack if not hit by that same attack swing
            critical = p.check_critical_chance()
            print("Hit")
            if critical:
                self.health -= (ba.damage * 1.5)
            else:
                self.health -= ba.damage
            life_steal = p.check_life_steal_chance()
            if life_steal:
                p.add_life_steal_health()
            self.melee_attack_collisions.append(1)

    def follow_mc(self):
        if self.rect.x < p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_east()
        if self.rect.x > p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_west()
        if self.rect.y < p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_south()
        if self.rect.y > p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_north()

    def generate_enemy(self):
        self.attack_timer = (pygame.time.get_ticks() / 1000)
        self.x = random.randint(-340, 990)
        self.y = random.randint(-340, 990)
        if self.animation <= 15:
            screen.blit(pygame.transform.scale(minibee1, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 30:
            screen.blit(pygame.transform.scale(minibee2, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 45:
            screen.blit(pygame.transform.scale(minibee3, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 60:
            screen.blit(pygame.transform.scale(minibee4, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        if self.animation == 60:
            self.animation = 0
        if self.not_attacking:
            self.follow_mc()
            self.auto_hit_player()

    def auto_hit_player(self):
        if self.rect.colliderect(p.rect) and (self.attack_timer - self.last_auto) >= self.attack_speed:
            dodge = p.check_dodge_chance()
            if not dodge:
                self.last_auto = self.attack_timer
                p.current_health -= self.hit_damage

    def buff_aura(self): #Speed and healing aura
        self.buffarea = pygame.draw.circle(screen, (100,100,100),(self.rect.x+15, self.rect.y+15),90,1 )
        for enemy in enemies:
            if enemy.rect.colliderect(self.buffarea):
                enemy.speed = 3
                if enemy.health > enemy.maxhealth:
                    enemy.health += .5
                enemy.wasbuffed = True
            if not enemy.rect.colliderect(self.buffarea) and enemy.wasbuffed == True:
                enemy.speed = random.randint(1,2)
                enemy.wasbuffed = False


    def buff_shout(self): #damage and max health/heal buff
        if self.shoutcounter <= self.shouttimer:
            self.shoutcounter += .1
        if self.shoutcounter >= self.shouttimer:
            self.shout = True
        if self.shout:
            self.shoutarea = pygame.draw.circle(screen, (100,0,255), (self.rect.x+15,self.rect.y+15), 400, 3)
            for enemy in enemies:
                if enemy.rect.colliderect(self.shoutarea):
                    enemy.maxhealth += 15
                    enemy.health += 15
                    enemy.edamage += 10
                    self.shout = False
                    self.shoutcounter = 0
    def comactive(self):
        if self.activate:
            self.buff_aura()
            self.buff_shout()






com = Commander(random.randint(-340, 990), random.randint(-340, 990))


class Mage(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = minibee1.get_rect().scale_by(1, 1)
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 20
        self.maxhealth = 1000
        self.health = 1000
        self.speed = 2.5
        self.travel_north()
        self.travel_east()
        self.travel_south()
        self.travel_west()
        self.felled = False
        self.not_attacking = True
        self.hit_damage = 45
        self.last_auto = 0
        self.attack_speed = 5
        self.speed = 1
        self.meteorimpact = None
        self.orspeed = 0
        self.meteorcd = 15
        self.shoutarea = None
        self.calling = False
        self.activate = False
        self.meteorcounter = 0
        self.seekercd = 20
        self.seekercounter = 0
        self.meteor = None
        self.px = 0
        self.py = 0
        self.summon = False
        self.o = 1000
        self.seeker = None
        self.seekerx = self.rect.x + 15
        self.seekery = self.rect.y + 15
        self.seekspeed = 3
        self.seekeractive = False
        self.seekdur = 8
        self.seekacdur = 0

    def auto_hit_player(self):
        if self.rect.colliderect(p.rect) and (self.attack_timer - self.last_auto) >= self.attack_speed:
            dodge = p.check_dodge_chance()
            if not dodge:
                self.last_auto = self.attack_timer
                p.current_health -= self.hit_damage

    def generate_enemy(self):
        self.attack_timer = (pygame.time.get_ticks() / 1000)
        self.x = random.randint(-340, 990)
        self.y = random.randint(-340, 990)
        if self.animation <= 15:
            screen.blit(pygame.transform.scale(minibee1, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 30:
            screen.blit(pygame.transform.scale(minibee2, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 45:
            screen.blit(pygame.transform.scale(minibee3, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        elif self.animation <= 60:
            screen.blit(pygame.transform.scale(minibee4, (40, 45)), (self.rect.x, self.rect.y))
            self.animation += 1
        if self.animation == 60:
            self.animation = 0
        if self.not_attacking:
            self.follow_mc()
            self.auto_hit_player()

    def follow_mc(self):
        if self.rect.x < p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_east()
        if self.rect.x > p.rect.x and not self.rect.colliderect(p.rect):
            self.travel_west()
        if self.rect.y < p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_south()
        if self.rect.y > p.rect.y and not self.rect.colliderect(p.rect):
            self.travel_north()

    def activate_death(self):
        if self.health <= 0:
            p.gold += 25
            # Makes sure Comander is actually dead
            self.felled = True

    def check_collisions(self):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                if not self.bullet_collisions:
                    self.bullet_collisions.append(bullet)
                    critical = p.check_critical_chance()
                    if critical:
                        self.health -= (b.damage * 1.5)
                    else:
                        self.health -= b.damage
                    life_steal = p.check_life_steal_chance()
                    if life_steal:
                        p.add_life_steal_health()
                elif self.bullet_collisions:
                    i = 0
                    for l in self.bullet_collisions:
                        if (bullet.rect.x == self.bullet_collisions[i].rect.x and bullet.rect.y ==
                                self.bullet_collisions[i].rect.y):
                            pass
                        elif bullet not in self.bullet_collisions and bullet.bullet_valid:
                            self.bullet_collisions.append(bullet)
                            critical = p.check_critical_chance()
                            if critical:
                                self.health -= (b.damage * 1.5)
                            else:
                                self.health -= b.damage
                            life_steal = p.check_life_steal_chance()
                            if life_steal:
                                p.add_life_steal_health()
                        i += 1
            for bullet in bullets:
                # removes expired bullets
                if bullet in self.bullet_collisions and not self.rect.colliderect(bullet.rect):
                    self.bullet_collisions.remove(bullet)
                    # print("BULLET REMOVED")
            if self.bullet_collisions:
                # backup to remove expired bullets
                for g in self.bullet_collisions:
                    if not g.rect.colliderect(self.rect):
                        # removes collided bullet
                        self.bullet_collisions.remove(g)
            if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
                critical = p.check_critical_chance()
                if critical:
                    self.health -= (ba.damage * 1.5)
                else:
                    self.health -= ba.damage
                life_steal = p.check_life_steal_chance()
                if life_steal:
                    p.add_life_steal_health()
                self.melee_attack_collisions.append(1)
        if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
            # Reduce health from the mini boss from Players basic attack if not hit by that same attack swing
            critical = p.check_critical_chance()
            if critical:
                self.health -= (ba.damage * 1.5)
            else:
                self.health -= ba.damage
            life_steal = p.check_life_steal_chance()
            if life_steal:
                p.add_life_steal_health()
            self.melee_attack_collisions.append(1)

    def summon_meteor(self):
        #Summons meteor to fall where the player was standing at the time of the summon
        if self.meteorcounter >= self.meteorcd:
            if not self.summon:
                self.px = p.rect.x +15
                self.py = p.rect.y + 15
                self.summon = True
            if self.summon:
                pygame.draw.circle(screen, (255, 0, 0), (self.px, self.py), 350, 3)
                if self.o > 0:
                    self.meteor = pygame.draw.circle(screen, (255,0,0),(self.px,self.py - self.o),40)
                    self.o -= 10
                if self.o <= 0:
                    self.meteorcounter = 0
                    self.meteor = pygame.draw.circle(screen, (255, 0, 0), (self.px, self.py), 350, 1)
                    self.summon = False
                    self.o = 1000
                    if self.meteor.colliderect(p.rect):
                        p.current_health -= 200



    def fire_seeker(self):
        if self.seekercounter >= self.seekercd:
            if not self.seekeractive:
                self.seekerx = ma.rect.x
                self.seekery = ma.rect.y
                self.seekeractive = True
            if self.seekeractive:
                self.seeker = pygame.draw.circle(screen, (1,1,1), (self.seekerx,self.seekery), 10, 4)
                if self.seekacdur >= self.seekdur:
                    self.seeker = None
                    self.seekacdur = 0
                    self.seekercounter = 0
                    self.seekeractive = False
                    self.seekerx = ma.rect.x
                    self.seekery = ma.rect.y
                if self.seekeractive and self.seeker.colliderect(p.rect):
                    p.current_health -= 30
                    self.seeker = None
                    self.seekercounter = 0
                    self.seekerx = ma.rect.x
                    self.seekery = ma.rect.y
                    self.seekeractive = False
    def seeker_seeks(self):
        if self.seekeractive:
            if self.seekery >= p.rect.y:
                self.seekery -= self.seekspeed
            if self.seekery <= p.rect.y:
                self.seekery += self.seekspeed
            if self.seekerx >= p.rect.x:
                self.seekerx -= self.seekspeed
            if self.seekerx <= p.rect.x:
                self.seekerx += self.seekspeed


    def active(self):
        if self.activate:
            self.fire_seeker()
            self.summon_meteor()
            self.seeker_seeks()
            self.meteorcounter += .03
            if not self.seekeractive:
                self.seekercounter += .03
            if self.seekeractive:
                self.seekacdur += .03

ma = Mage(random.randint(-340, 990), random.randint(-340, 990))

class CalcTargets:
    def calc_closest(t1, o1, n1):
        closest_targets = []
        close = []
        # Iterate through the enemies and checks their distances then adds them to the list
        for t1 in o1:
            xcor = t1.rect.x - p.rect.x
            ycor = t1.rect.y - p.rect.y
            distance = math.sqrt(xcor ** 2 + ycor ** 2)
            xcor = abs(t1.rect.x - p.rect.x)
            ycor = abs(t1.rect.y - p.rect.y)
            if close == []:
                close.append((t1, xcor, ycor, distance))
            if close[0][3] > distance:
                close.insert(0,(t1,xcor,ycor,distance))
            else:
                close.append((t1, xcor, ycor, distance))


        # Sorts and condenses the list to n closest targets.
        closest_targets = close[:n1]
        for i in closest_targets:
            pygame.draw.line(screen, (0, 100, 0), (p.rect.x, p.rect.y), (closest_targets[1],closest_targets[2]),10)
        return closest_targets

    def calc_farthest(t1, o1, n1):
        farthest_target = []
        for t1 in o1:
            # itterates through the enemies and checks thier distances then adds them to the list
            xcor = t1.rect.x - p.rect.x
            ycor = t1.rect.y - p.rect.y
            distance = math.sqrt(xcor ** 2 + ycor ** 2)
            farthest_target.append((t1, xcor, ycor))

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

    def check_collisions(self):
        if b.shooting:
            for bullet in bullets:
                # for each active bullet, if the bullet hits the skeleton king boss,
                # deal damage if appropriate conditions met.
                if self.rect.colliderect(bullet.rect) and bullet.bullet_valid:
                    if not self.bullet_collisions:
                        # if the skeleton king boss has encountered it's first bullet, add to the list and take damage
                        self.bullet_collisions.append(bullet)
                        critical = p.check_critical_chance()
                        if critical:
                            self.health -= (b.damage * 1.5)
                        else:
                            self.health -= b.damage
                        life_steal = p.check_life_steal_chance()
                        if life_steal:
                            p.add_life_steal_health()
                    elif self.bullet_collisions:
                        # if the list of bullets the skeleton king boss has collided with is greater than 0,
                        # make sure it is a different bullet in order to deal damage
                        i = 0
                        for l in self.bullet_collisions:
                            if (bullet.rect.x == self.bullet_collisions[i].rect.x and
                                    bullet.rect.y == self.bullet_collisions[i].rect.y):
                                pass
                            elif bullet not in self.bullet_collisions and bullet.bullet_valid:
                                # have the skeleton king take damage if hit with a bullet they havent been hit by
                                self.bullet_collisions.append(bullet)
                                critical = p.check_critical_chance()
                                if critical:
                                    self.health -= (b.damage * 1.5)
                                else:
                                    self.health -= b.damage
                                life_steal = p.check_life_steal_chance()
                                if life_steal:
                                    p.add_life_steal_health()
                            i += 1
        for bullet in bullets:
            # removes expired bullets from the skeleton king boss bullet collision list
            if bullet in self.bullet_collisions and not self.rect.colliderect(bullet.rect):
                self.bullet_collisions.remove(bullet)
                # print("BULLET REMOVED")
        if self.bullet_collisions:
            # backup to remove expired bullets from the skeleton king boss bullet collision list
            for g in self.bullet_collisions:
                if not g.rect.colliderect(self.rect):
                    # removes collided bullet from skeleton kings bullet collisions list
                    self.bullet_collisions.remove(g)
        if self.rect.colliderect(ba.hitbox_rect) and ba.running and not self.melee_attack_collisions:
            critical = p.check_critical_chance()
            if critical:
                self.health -= (ba.damage * 1.5)
            else:
                self.health -= ba.damage
            life_steal = p.check_life_steal_chance()
            if life_steal:
                p.add_life_steal_health()
            self.melee_attack_collisions.append(1)

    def activate_death(self):
        if self.health <= 0:
            p.gold += 250
            # removes the skeleton king if they are at or below zero health
            self.felled = True
            self.activate = False
            self.rect = None

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
                dodge = p.check_dodge_chance()
                if not dodge:
                    # have the player take damage
                    p.current_health -= 24
                    self.player_collide_counter = 0
                else:
                    self.player_collide_counter = 0
            else:
                # increase counter if player is still colliding with enemy
                self.player_collide_counter += 1
        else:
            # reset counter
            self.player_collide_counter = 0


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

    def travel_to_player(self):
        # for every xp the player has gone near, have the XP fly to the player
        if abs(self.rect.x - p.rect.x) < 35 and abs(self.rect.y - p.rect.y) < 35:
            # remove the XP from the world and increase player XP
            if self in xp:
                xp.remove(self)
                xpB.xp += 1
            if self in xp_hit:
                xp_hit.remove(self)
        else:
            # have the XP fly to the Player
            if self.rect.x + 18 < p.rect.x:
                self.x += p.speed
            if self.rect.x + 18 > p.rect.x:
                self.x -= p.speed
            if self.rect.y + 18 < p.rect.y:
                self.y += p.speed
            if self.rect.y + 18 > p.rect.y:
                self.y -= p.speed


speed_item_visible = True
gameTimerOn = False
class Laser:
    def __init__(self): #Simple laser attack.
        self.targets = 3
        self.closest_enemy = [1000, 1000]
        self.damage = 5
        self.cd = 10
        self.shoot = 0
        self.target = []
        self.dmgtype = "Laser"
        self.laser_aquired = False
    def fire(self):
        for enemy in enemies:
            if enemy.spawned:
                self.x_distance = abs(p.rect.x - enemy.rect.x)
                self.y_distance = abs(p.rect.y - enemy.rect.y)
                smallest_x = abs(self.closest_enemy[0] - p.rect.x)
                smallest_y = abs(self.closest_enemy[1] - p.rect.y)
                if self.x_distance + self.y_distance < smallest_x + smallest_y:
                    self.closest_enemy[0] = enemy.rect.x
                    self.closest_enemy[1] = enemy.rect.y
        for enemy in enemies:
            if enemy.rect.x == self.closest_enemy[0] and enemy.rect.y == self.closest_enemy[1]:
                self.target.append(enemy)
                pygame.draw.line(screen, (255, 0, 100),(p.rect.x + 10,p.rect.y + 10), (self.closest_enemy[0] + 15, self.closest_enemy[1] + 15), 10)
                enemy.health -= self.damage
        self.closest_enemy = [1000,1000]

    def laser_timer(self):
        if self.shoot <=self.cd:
            self.shoot+=.1
            if self.shoot >= self.cd:
                lz.fire()
                self.shoot = 0





lz = Laser()


# gameTime = 0
class ChainLightning:

    def __init__(self):
        self.closest_enemy = [1000,1000]
        self.x_distance = 1000
        self.y_distance = 1000
        self.next_closest_enemy = [1000, 1000]
        self.enemies_hit = 0
        self.targeted_enemies = []
        self.target_cords = []
        self.cooldown = 30
        self.shoot = 0
        self.damage = 100

    def target_enemy(self): # targets first enemy
        for enemy in enemies:
            if enemy.spawned:
                self.x_distance = abs(p.rect.x - enemy.rect.x)
                self.y_distance = abs(p.rect.y - enemy.rect.y)
                smallest_x = abs(self.closest_enemy[0] - p.rect.x)
                smallest_y = abs(self.closest_enemy[1] - p.rect.y)
                if self.x_distance + self.y_distance < smallest_x + smallest_y: # closest enemy so far
                    self.closest_enemy[0] = enemy.rect.x
                    self.closest_enemy[1] = enemy.rect.y

        for enemy in enemies:
            if enemy.rect.x == self.closest_enemy[0] and enemy.rect.y == self.closest_enemy[1]: # if enemy is not itself
                self.targeted_enemies.append(enemy) # stores targeted enemy in list
                pygame.draw.line(screen, (252, 202, 63), (p.rect.x,p.rect.y),(self.closest_enemy[0]+15,self.closest_enemy[1]+15), 4)
                critical = p.check_critical_chance()
                if critical:
                    enemy.health -= (self.damage * 1.5)
                else:
                    enemy.health -= self.damage
                self.enemies_hit += 1

        self.target_next_enemy()

    def target_next_enemy(self):
        if self.enemies_hit >= 2:
            self.closest_enemy = self.next_closest_enemy
            self.next_closest_enemy = [1000, 1000]
        for enemy in enemies:
            if enemy.spawned:
                if not enemy.rect.x == self.closest_enemy[0] and not enemy.rect.y == self.closest_enemy[1]: # if enemy is not itself
                    self.x_distance = abs(self.closest_enemy[0] - enemy.rect.x)
                    self.y_distance = abs(self.closest_enemy[1] - enemy.rect.y)
                    smallest_x = abs(self.next_closest_enemy[0] - self.closest_enemy[0])
                    smallest_y = abs(self.next_closest_enemy[1] - self.closest_enemy[1])

                    if self.x_distance + self.y_distance < smallest_x + smallest_y:  # closest enemy so far
                        if enemy not in self.targeted_enemies:
                            self.next_closest_enemy[0] = enemy.rect.x
                            self.next_closest_enemy[1] = enemy.rect.y

        for enemy in enemies:
            if enemy.rect.x == self.next_closest_enemy[0] and enemy.rect.y == self.next_closest_enemy[1]:
                if self.enemies_hit == 1:
                    self.targeted_enemies.append(enemy)
                    pygame.draw.line(screen, (252, 202, 63), (self.closest_enemy[0]+18,self.closest_enemy[1]+18),(self.next_closest_enemy[0]+15,self.next_closest_enemy[1]+15), 4)
                    self.target_cords = [self.next_closest_enemy[0]+15,self.next_closest_enemy[1]+15]
                    critical = p.check_critical_chance()
                    if critical:
                        enemy.health -= (self.damage * 1.5)
                    else:
                        enemy.health -= self.damage
                if self.enemies_hit == 2:
                    self.targeted_enemies.append(enemy)
                    pygame.draw.line(screen, (252, 202, 63), (self.target_cords[0],self.target_cords[1]),(self.next_closest_enemy[0]+18,self.next_closest_enemy[1]+18), 4)
                    critical = p.check_critical_chance()
                    if critical:
                        enemy.health -= (self.damage * 1.5)
                    else:
                        enemy.health -= self.damage
                self.enemies_hit += 1

        if self.enemies_hit >= 3: # reset stats when done looping
            self.next_closest_enemy = [1000,1000]
            self.closest_enemy = [1000,1000]
            self.x_distance = 1000
            self.y_distance = 1000
            self.enemies_hit = 0
            self.targeted_enemies.clear()
        else:
            self.target_next_enemy()
    def cl_timer(self):
        if self.shoot <=self.cooldown:
            self.shoot+=.05
            if self.shoot >= self.cooldown:
                cl.target_enemy()
                self.shoot = 0



cl = ChainLightning()


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
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
        self.xp_bar_border_rect = pygame.draw.line(screen, (0, 0, 0), (90 - self.offset, tempheight-50),
                                                   (710 - self.offset, tempheight-50), 45)
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
                    screen.blit(mediumScroll, (tempwidth-385, 225))
                    upgrade_title1_render = self.upgrade_title_font.render('OPTION 1', True, (0, 0, 0))
                    screen.blit(upgrade_title1_render, (202, 330))
                    upgrade_title2_render = self.upgrade_title_font.render('OPTION 2', True, (0, 0, 0))
                    screen.blit(upgrade_title2_render, (tempwidth-285, 330))

                    self.button_rect1 = pygame.Rect(100, 222, 285, 370)
                    self.button_rect2 = pygame.Rect(tempwidth-385, 222, 285, 370)

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
                        self.button_rect2 = pygame.Rect(tempwidth-385, 222, 285, 370)

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
                    self.xp_bar_rect = pygame.draw.line(screen, (28, 36, 192), (100 - self.offset, tempheight-50),
                                                        (self.leftover_size + 100 - self.offset, tempheight-50), 25)
                    self.leftover = 0
            else:
                # if player has XP but not enough for a full XP level, display the xp bar
                self.xp_bar_rect = pygame.draw.line(screen, (28, 36, 192), (100 - self.offset, tempheight-50),
                                                    ((self.total_length * self.length) + self.leftover_size
                                                     + 100 - self.offset, tempheight-50), 25)
                self.xp_bar_empty_rect = pygame.draw.line(screen, (255, 255, 255),
                                                          ((self.total_length * self.length) +
                                                           self.leftover_size + 100 - self.offset, tempheight-50),
                                                          (700 - self.offset, tempheight-50), 25)
        else:
            # Displays if player has zero XP
            self.xp_bar_rect = pygame.draw.line(screen, (28, 36, 192), (100 - self.offset, tempheight-50),
                                                (self.leftover_size + 100 - self.offset, tempheight-50), 25)
            self.xp_bar_empty_rect = pygame.draw.line(screen, (255, 255, 255),
                                                      (self.leftover_size + 100 - self.offset, tempheight-50),
                                                      (700 - self.offset, tempheight-50), 25)
        if tempwidth != 800:
        # Displays level number
            self.connector = pygame.draw.line(screen, (0, 0, 0), (710 - self.offset, tempheight-50),
                                              (740 - self.offset, tempheight-50), 5)
            self.left = pygame.draw.line(screen, (0, 0, 0), (740 - self.offset, tempheight-30), (740 - self.offset, tempheight-70), 6)
            self.top = pygame.draw.line(screen, (0, 0, 0), (738 - self.offset, tempheight-70), (785 - self.offset, tempheight-70), 6)
            self.bottom = pygame.draw.line(screen, (0, 0, 0), (738 - self.offset, tempheight-30), (785 - self.offset, tempheight-30), 6)
            self.right = pygame.draw.line(screen, (0, 0, 0), (785 - self.offset, tempheight-27), (785 - self.offset, tempheight-72), 6)
            self.level_background = pygame.draw.line(screen, (255, 255, 255), (744 - self.offset, tempheight-50),
                                                     (782 - self.offset, tempheight-50), 33)
        else :
            self.connector = pygame.draw.line(screen, (0, 0, 0), (710 - self.offset, tempheight - 50),
                                              (740 - self.offset, tempheight - 50), 5)
            self.left = pygame.draw.line(screen, (0, 0, 0), (740 - self.offset, 790), (740 - self.offset, 750), 6)
            self.top = pygame.draw.line(screen, (0, 0, 0), (738 - self.offset, 750), (785 - self.offset, 750), 6)
            self.bottom = pygame.draw.line(screen, (0, 0, 0), (738 - self.offset, 790), (785 - self.offset, 790), 6)
            self.right = pygame.draw.line(screen, (0, 0, 0), (785 - self.offset, 793), (785 - self.offset, 748), 6)
            self.level_background = pygame.draw.line(screen, (255, 255, 255), (744 - self.offset, 770),
                                                     (782 - self.offset, 770), 33)
        level_render = self.level_font.render(str(self.level), True, (0, 0, 0))
        if self.level < 10:
            screen.blit(level_render, (756 - self.offset, tempheight-63))
        else:
            # moves the level number to the left to better accommodate another value fitting into the box
            screen.blit(level_render, (747 - self.offset, tempheight-63))

    def basic_attack_damage_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_ba_damage1_render, (tempwidth-335, 365))
            upgrade_ba_damage2_render = self.upgrade_desc_font.render('Damage by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_damage2_render, (tempwidth-335, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            ba.damage *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def basic_attack_range_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_ba_range1_render, (tempwidth-335, 365))
            upgrade_ba_range2_render = self.upgrade_desc_font.render('Range by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_range2_render, (tempwidth-335, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            ba.range_increase += 10
            ba.hitbox_radius += 14
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def basic_attack_speed_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_ba_speed1_render, (tempwidth-335, 365))
            upgrade_ba_speed2_render = self.upgrade_desc_font.render('Speed by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_ba_speed2_render, (tempwidth-335, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            ba.timer_target *= .9
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def move_speed_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_move_speed1_render, (tempwidth-335, 365))
            upgrade_move_speed2_render = self.upgrade_desc_font.render('Speed by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_move_speed2_render, (tempwidth-335, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            p.speed *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def dodge_chance_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_dodge1_render, (tempwidth-335, 365))
            upgrade_dodge2_render = self.upgrade_desc_font.render('Chance by 2%.', True, (0, 0, 0))
            screen.blit(upgrade_dodge2_render, (tempwidth-335, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            p.dodgeChance += 2
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def bullet_damage_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_bul_damage1_render, (tempwidth-335, 365))
            upgrade_bul_damage2_render = self.upgrade_desc_font.render('Damage by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_damage2_render, (tempwidth-335, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            b.damage *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def bullet_range_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_bul_range1_render, (tempwidth-335, 365))
            upgrade_bul_range2_render = self.upgrade_desc_font.render('Range by 10%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_range2_render, (tempwidth-335, 390))

        elif not option:
            # upgrade this ability due to the user selecting this upgrade
            b.bullet_distance *= 1.1
            self.selected_upgrade_choices = False
            self.level_menu = False
            self.selected = True

    def bullet_speed_upgrade(self, option):
        info = pygame.display.Info()
        tempwidth, tempheight = info.current_w, info.current_h
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
            screen.blit(upgrade_bul_speed1_render, (tempwidth-335, 365))
            upgrade_bul_speed2_render = self.upgrade_desc_font.render('Speed by 5%.', True, (0, 0, 0))
            screen.blit(upgrade_bul_speed2_render, (tempwidth-335, 390))

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


class SkillTree:
    def __init__(self):
        self.active = True
        self.offset = 35
        self.box1 = pygame.Rect(85, 225, 115, 115)
        self.box1_border = pygame.Rect(78, 218, 129, 129)
        self.box2 = pygame.Rect(260, 225, 115, 115)
        self.box2_border = pygame.Rect(253, 218, 129, 129)
        self.box3 = pygame.Rect(435, 225, 115, 115)
        self.box3_border = pygame.Rect(428, 218, 129, 129)
        self.box4 = pygame.Rect(610, 225, 115, 115)
        self.box4_border = pygame.Rect(603, 218, 129, 129)

        self.box5 = pygame.Rect(85, 465, 115, 115)
        self.box5_border = pygame.Rect(78, 458, 129, 129)
        self.box6 = pygame.Rect(260, 465, 115, 115)
        self.box6_border = pygame.Rect(253, 458, 129, 129)
        self.box7 = pygame.Rect(435, 465, 115, 115)
        self.box7_border = pygame.Rect(428, 458, 129, 129)
        self.box8 = pygame.Rect(610, 465, 115, 115)
        self.box8_border = pygame.Rect(603, 458, 129, 129)

        self.description_box = pygame.Rect(120, 670, 575, 800)
        self.description_border = pygame.Rect(110, 660, 595, 820)

        self.buy_box = pygame.Rect(580, 715, 90, 47)
        self.buy_border = pygame.Rect(575, 710, 100, 57)

        self.box1_level = pygame.Rect(158, 375, 25, 25)
        self.box2_level = pygame.Rect(158, 375, 25, 25)

        self.level_font = pygame.font.SysFont('Garamond', 22)
        self.level2_font = pygame.font.SysFont('Garamond', 18, bold=1)
        self.title_font = pygame.font.SysFont('Garamond', 82, bold=1)
        self.back_font = pygame.font.SysFont('Garamond', 36, bold=1)
        self.description_title_font = pygame.font.SysFont('Garamond', 32, bold=1)
        self.description_font = pygame.font.SysFont('Garamond', 24, bold=1)
        self.buy_font = pygame.font.SysFont('Garamond', 36, bold=2)
        self.feedback_message_font = pygame.font.SysFont('Garamond', 22, bold=1)

        self.title_background_border = pygame.Rect(225, 40, 358, 115)
        self.title_background = pygame.Rect(235, 50, 337, 95)

        self.back_background_border = pygame.Rect(15, 15, 143, 68)
        self.back_background = pygame.Rect(23, 23, 127, 52)
        self.selected = False
        self.selected_option = []
        self.selected_cost = 0

        self.upgrade1_level = 0
        self.upgrade2_level = 0
        self.upgrade3_level = 0
        self.upgrade4_level = 0
        self.upgrade5_level = 0
        self.upgrade6_level = 0
        self.upgrade7_level = 0
        self.upgrade8_level = 0

        self.upgrade1_cost = 425
        self.upgrade2_cost = 475
        self.upgrade3_cost = 1250
        self.upgrade4_cost = 375
        self.upgrade5_cost = 175
        self.upgrade6_cost = 300
        self.upgrade7_cost = 615
        self.upgrade8_cost = 750

        self.balance = 0

        self.feedback = False
        self.feedback_option = 0
        self.feedback_box = pygame.Rect(640, 23, 130, 50)
        self.message_timer = False
        self.message_timer_counter = 0
        # self.feedback_box_border = pygame.Rect(78, 218, 129, 129)

        self.column = 0

    def load_data(self):

        if self.upgrade1_level:
            if self.upgrade1_level >= 5:
                self.upgrade1_cost = 999999999
                if self.selected_option:
                    if self.selected_option[0] == 'box1':
                        self.selected_cost = 999999999

            else:
                self.upgrade1_cost = (425 * 1.25**self.upgrade1_level)

        if self.upgrade2_level:
            if self.upgrade2_level >= 5:
                self.upgrade2_cost = 999999999
                if self.selected_option:
                    if self.selected_option[0] == 'box2':
                        self.selected_cost = 999999999

            else:
                self.upgrade2_cost = (475 * 1.25**self.upgrade2_level)

        if self.upgrade3_level:
            self.upgrade3_cost = 999999999
            if self.selected_option:
                    if self.selected_option[0] == 'box3':
                        self.selected_cost = 999999999

        if self.upgrade4_level:
            if self.upgrade4_level >= 5:
                self.upgrade4_cost = 999999999
                if self.selected_option:
                    if self.selected_option[0] == 'box4':
                        self.selected_cost = 999999999

            else:
                self.upgrade4_cost = (375 * 1.25**self.upgrade4_level)

        if self.upgrade5_level:
            if self.upgrade5_level >= 5:
                self.upgrade5_cost = 999999999
                if self.selected_option:
                    if self.selected_option[0] == 'box5':
                        self.selected_cost = 999999999

            else:
                self.upgrade5_cost = (175 * 1.25**self.upgrade5_level)

        if self.upgrade6_level:
            if self.upgrade6_level >= 5:
                self.upgrade6_cost = 999999999
                if self.selected_option:
                    if self.selected_option[0] == 'box6':
                        self.selected_cost = 999999999

            else:
                self.upgrade6_cost = (300 * 1.25**self.upgrade6_level)

        if self.upgrade7_level:
            if self.upgrade7_level >= 5:
                self.upgrade7_cost = 999999999
                if self.selected_option:
                    if self.selected_option[0] == 'box7':
                        self.selected_cost = 999999999
            else:
                self.upgrade7_cost = (615 * 1.25**self.upgrade7_level)

        if self.upgrade8_level:
            if self.upgrade8_level >= 5:
                self.upgrade8_cost = 999999999
                if self.selected_option:
                    if self.selected_option[0] == 'box8':
                        self.selected_cost = 999999999

            else:
                self.upgrade8_cost = (425 * 1.25**self.upgrade8_level)


    def skill_tree(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    global game
                    game = False
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.box1.collidepoint(event.pos) or self.box1_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box1']
                        self.selected_cost = self.upgrade1_cost
                    if self.box2.collidepoint(event.pos) or self.box2_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box2']
                        self.selected_cost = self.upgrade2_cost
                    if self.box3.collidepoint(event.pos) or self.box3_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box3']
                        self.selected_cost = self.upgrade3_cost
                    if self.box4.collidepoint(event.pos) or self.box4_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box4']
                        self.selected_cost = self.upgrade4_cost
                    if self.box5.collidepoint(event.pos) or self.box5_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box5']
                        self.selected_cost = self.upgrade5_cost
                    if self.box6.collidepoint(event.pos) or self.box6_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box6']
                        self.selected_cost = self.upgrade6_cost
                    if self.box7.collidepoint(event.pos) or self.box7_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box7']
                        self.selected_cost = self.upgrade7_cost
                    if self.box8.collidepoint(event.pos) or self.box8_border.collidepoint(event.pos):
                        self.selected = True
                        self.selected_option = ['box8']
                        self.selected_cost = self.upgrade8_cost
                    if self.back_background.collidepoint(event.pos) or self.back_background_border.collidepoint(event.pos):
                        global st
                        st = SkillTree()
                        self.active = False
                        main_menu()
                    if (self.buy_box.collidepoint(event.pos) or self.buy_border.collidepoint(event.pos)) and self.selected:
                        if self.selected_cost == 999999999: # if upgrade is maxed out
                            self.feedback_option = 3
                            self.message_timer = 0
                            self.message_timer = True
                        elif self.balance < self.selected_cost: # if user cannot afford to purchase upgrade
                            self.feedback = True
                            self.feedback_option = 2
                            self.message_timer = 0
                            self.message_timer = True
                        else: # if user is able to purchase upgrade
                            self.purchase_upgrade()

                            self.feedback = True
                            self.feedback_option = 1
                            self.message_timer = True

            self.load_data()
            screen.blit(dungeonBackground, (0, 0))
            if not self.selected:
                pygame.draw.rect(screen, (0,0,0), self.box1_border)
                pygame.draw.rect(screen, (47,79,79), self.box1)
                pygame.draw.rect(screen, (0,0,0), self.box2_border)
                pygame.draw.rect(screen, (47,79,79), self.box2)
                pygame.draw.rect(screen, (0,0,0), self.box3_border)
                pygame.draw.rect(screen, (47,79,79), self.box3)
                pygame.draw.rect(screen, (0,0,0), self.box4_border)
                pygame.draw.rect(screen, (47,79,79), self.box4)
                pygame.draw.rect(screen, (0,0,0), self.box5_border)
                pygame.draw.rect(screen, (47,79,79), self.box5)
                pygame.draw.rect(screen, (0,0,0), self.box6_border)
                pygame.draw.rect(screen, (47,79,79), self.box6)
                pygame.draw.rect(screen, (0,0,0), self.box7_border)
                pygame.draw.rect(screen, (47,79,79), self.box7)
                pygame.draw.rect(screen, (0,0,0), self.box8_border)
                pygame.draw.rect(screen, (47,79,79), self.box8)
            else:
                if self.selected_option[0] == 'box1':
                    pygame.draw.rect(screen, (255,255,255), self.box1_border)
                    pygame.draw.rect(screen, (47,79,79), self.box1)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box1_border)
                    pygame.draw.rect(screen, (47,79,79), self.box1)
                if self.selected_option[0] == 'box2':
                    pygame.draw.rect(screen, (255,255,255), self.box2_border)
                    pygame.draw.rect(screen, (47,79,79), self.box2)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box2_border)
                    pygame.draw.rect(screen, (47,79,79), self.box2)
                if self.selected_option[0] == 'box3':
                    pygame.draw.rect(screen, (255,255,255), self.box3_border)
                    pygame.draw.rect(screen, (47,79,79), self.box3)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box3_border)
                    pygame.draw.rect(screen, (47,79,79), self.box3)
                if self.selected_option[0] == 'box4':
                    pygame.draw.rect(screen, (255,255,255), self.box4_border)
                    pygame.draw.rect(screen, (47,79,79), self.box4)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box4_border)
                    pygame.draw.rect(screen, (47,79,79), self.box4)
                if self.selected_option[0] == 'box5':
                    pygame.draw.rect(screen, (255,255,255), self.box5_border)
                    pygame.draw.rect(screen, (47,79,79), self.box5)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box5_border)
                    pygame.draw.rect(screen, (47,79,79), self.box5)
                if self.selected_option[0] == 'box6':
                    pygame.draw.rect(screen, (255,255,255), self.box6_border)
                    pygame.draw.rect(screen, (47,79,79), self.box6)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box6_border)
                    pygame.draw.rect(screen, (47,79,79), self.box6)
                if self.selected_option[0] == 'box7':
                    pygame.draw.rect(screen, (255,255,255), self.box7_border)
                    pygame.draw.rect(screen, (47,79,79), self.box7)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box7_border)
                    pygame.draw.rect(screen, (47,79,79), self.box7)
                if self.selected_option[0] == 'box8':
                    pygame.draw.rect(screen, (255,255,255), self.box8_border)
                    pygame.draw.rect(screen, (47,79,79), self.box8)
                else:
                    pygame.draw.rect(screen, (0,0,0), self.box8_border)
                    pygame.draw.rect(screen, (47,79,79), self.box8)

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (80, 350))
            if self.upgrade1_cost == 999999999:
                level_render1 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render1, (105, 368))
            else:
                level_render1 = self.level_font.render(f'Level: {self.upgrade1_level}', True, (0, 0, 0))
                screen.blit(level_render1, (105, 366))

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (255, 350))
            if self.upgrade2_cost == 999999999:
                level_render2 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render2, (280, 368))
            else:
                level_render2 = self.level_font.render(f'Level: {self.upgrade2_level}', True, (0, 0, 0))
                screen.blit(level_render2, (280, 366))

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (430, 350))
            if self.upgrade3_cost == 999999999:
                level_render3 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render3, (455, 368))
            else:
                level_render3 = self.level_font.render(f'Level: {self.upgrade3_level}', True, (0, 0, 0))
                screen.blit(level_render3, (455, 366))

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (605, 350))
            if self.upgrade4_cost == 999999999:
                level_render4 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render4, (630, 368))
            else:
                level_render4 = self.level_font.render(f'Level: {self.upgrade4_level}', True, (0, 0, 0))
                screen.blit(level_render4, (630, 366))

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (80, 590))
            if self.upgrade5_cost == 999999999:
                level_render5 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render5, (105, 608))
            else:
                level_render5 = self.level_font.render(f'Level: {self.upgrade5_level}', True, (0, 0, 0))
                screen.blit(level_render5, (105, 606))

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (255, 590))
            if self.upgrade6_cost == 999999999:
                level_render6 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render6, (280, 608))
            else:
                level_render6 = self.level_font.render(f'Level: {self.upgrade6_level}', True, (0, 0, 0))
                screen.blit(level_render6, (280, 606))

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (430, 590))
            if self.upgrade7_cost == 999999999:
                level_render7 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render7, (455, 608))
            else:
                level_render7 = self.level_font.render(f'Level: {self.upgrade7_level}', True, (0, 0, 0))
                screen.blit(level_render7, (455, 606))

            screen.blit(pygame.transform.scale(level_scroll, (115, 55)), (605, 590))
            if self.upgrade8_cost == 999999999:
                level_render8 = self.level2_font.render(f'MAXED', True, (0, 0, 0))
                screen.blit(level_render8, (630, 608))
            else:
                level_render8 = self.level_font.render(f'Level: {self.upgrade8_level}', True, (0, 0, 0))
                screen.blit(level_render8, (630, 606))

            pygame.draw.rect(screen, (0,0,0), self.title_background_border)
            pygame.draw.rect(screen, (47,79,79), self.title_background)
            title_render = self.title_font.render('Skill Tree', True, (225, 255, 255))
            screen.blit(title_render, (240, 50))

            pygame.draw.rect(screen, (0,0,0), self.back_background_border, border_radius=15)
            pygame.draw.rect(screen, (255,0,0), self.back_background, border_radius=15)
            back_render = self.back_font.render('Back', True, (225, 255, 255))
            screen.blit(back_render, (45, 26))

            screen.blit(pygame.transform.scale(maxhealth_img, (100,100)), (self.box1.x+7, self.box1.y+3))
            screen.blit(pygame.transform.scale(regen_img, (100,100)), (self.box2.x+8, self.box2.y+6))
            screen.blit(pygame.transform.scale(revive_img, (100,100)), (self.box3.x+7, self.box3.y+8))
            screen.blit(pygame.transform.scale(movementspeed_img, (100,100)), (self.box4.x+7, self.box4.y+6))
            screen.blit(pygame.transform.scale(dodge_img, (100,100)), (self.box5.x+7, self.box5.y+7))
            screen.blit(pygame.transform.scale(gold_img, (100,100)), (self.box6.x+10, self.box6.y+5))
            screen.blit(pygame.transform.scale(crit_img, (100,100)), (self.box7.x+7, self.box7.y+8))
            screen.blit(pygame.transform.scale(lifesteal_img, (100,100)), (self.box8.x+7, self.box8.y+3))

            if self.selected:
                self.display_information(self.selected_option[0])

            if self.message_timer:
                self.message_timer_counter += 1

            clock.tick(15)
            pygame.display.update()

    def purchase_upgrade(self):

        if self.selected_option[0] == 'box1':
            self.selected_cost = self.upgrade1_cost
        if self.selected_option[0] == 'box2':
            self.selected_cost = self.upgrade2_cost
        if self.selected_option[0] == 'box3':
            self.selected_cost = self.upgrade3_cost
        if self.selected_option[0] == 'box4':
            self.selected_cost = self.upgrade4_cost
        if self.selected_option[0] == 'box5':
            self.selected_cost = self.upgrade5_cost
        if self.selected_option[0] == 'box6':
            self.selected_cost = self.upgrade6_cost
        if self.selected_option[0] == 'box7':
            self.selected_cost = self.upgrade7_cost
        if self.selected_option[0] == 'box8':
            self.selected_cost = self.upgrade8_cost

        pd.subtract_gold(self.selected_cost)

        self.load_data()

        if self.selected_option[0] == "box1":
            self.selected_cost = self.upgrade1_cost
            self.column = 3
        elif self.selected_option[0] == "box2":
            self.selected_cost = self.upgrade2_cost
            self.column = 4
        elif self.selected_option[0] == "box3":
            self.selected_cost = self.upgrade3_cost
            self.column = 5
        elif self.selected_option[0] == "box4":
            self.selected_cost = self.upgrade4_cost
            self.column = 6
        elif self.selected_option[0] == "box5":
            self.selected_cost = self.upgrade5_cost
            self.column = 7
        elif self.selected_option[0] == "box6":
            self.selected_cost = self.upgrade6_cost
            self.column = 8
        elif self.selected_option[0] == "box7":
            self.selected_cost = self.upgrade7_cost
            self.column = 9
        elif self.selected_option[0] == "box8":
            self.selected_cost = self.upgrade8_cost
            self.column = 10

        if self.column == 3:
            self.upgrade1_level += 1
        elif self.column == 4:
            self.upgrade2_level += 1
        elif self.column == 5:
            self.upgrade3_level += 1
        elif self.column == 6:
            self.upgrade4_level += 1
        elif self.column == 7:
            self.upgrade5_level += 1
        elif self.column == 8:
            self.upgrade6_level += 1
        elif self.column == 9:
            self.upgrade7_level += 1
        elif self.column == 10:
            self.upgrade8_level += 1

        pd.increase_upgrade_level(self.column)


    def give_feedback(self):
        if self.feedback_option == 1:
            pygame.draw.rect(screen, (50,205,50), self.feedback_box, border_radius=15)
            feedback_message_render = self.feedback_message_font.render('Purchased!', True, (0,0,0))
            screen.blit(feedback_message_render, (653, 36))
        if self.feedback_option == 2:
            pygame.draw.rect(screen, (255,191,0), self.feedback_box, border_radius=15)
            feedback_message_render = self.feedback_message_font.render('Not Enough', True, (0,0,0))
            screen.blit(feedback_message_render, (645, 26))
            feedback_message2_render = self.feedback_message_font.render('Gold!', True, (0,0,0))
            screen.blit(feedback_message2_render, (678, 48))
        if self.feedback_option == 3:
            pygame.draw.rect(screen, (255,191,0), self.feedback_box, border_radius=15)
            feedback_message_render = self.feedback_message_font.render('Limit', True, (0,0,0))
            screen.blit(feedback_message_render, (677, 26))
            feedback_message2_render = self.feedback_message_font.render('Reached!', True, (0,0,0))
            screen.blit(feedback_message2_render, (662, 48))

    def display_information(self, option):
        pygame.draw.rect(screen, (0,0,0), self.description_border)
        pygame.draw.rect(screen, (47,79,79), self.description_box)
        pygame.draw.rect(screen, (255,255,0), self.buy_box, border_radius=25)
        if option == 'box1':
            description_title_render = self.description_title_font.render('Max Health Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Increases max health by 10', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade1_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade1_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if option == 'box2':
            description_title_render = self.description_title_font.render('Health Regeneration Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Restores 2 health every 30 seconds', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade2_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade2_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if option == 'box3':
            description_title_render = self.description_title_font.render('Revive Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Get one extra life if you drop to 0 health', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade3_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade3_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if option == 'box4':
            description_title_render = self.description_title_font.render('Movement Speed Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Increases player movement speed by 2%', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade4_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade4_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if option == 'box5':
            description_title_render = self.description_title_font.render('Dodge Chance Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Increases dodge chance by 2%', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade5_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade5_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if option == 'box6':
            description_title_render = self.description_title_font.render('Gold Chance Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Increases chance of gold dropped by 5%', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade6_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade6_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if option == 'box7':
            description_title_render = self.description_title_font.render('Critical Chance Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Increases critical chance by 5%', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade7_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade7_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if option == 'box8':
            description_title_render = self.description_title_font.render('Life Steal Upgrade', True, (225, 255, 255))
            screen.blit(description_title_render, (135, 685))
            description_render = self.description_font.render('Increases life steal chance by 5%', True, (225, 255, 255))
            screen.blit(description_render, (135, 730))
            if self.upgrade8_cost == 999999999:
                description_cost_render = self.description_font.render(f'Cost: MAXED  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            else:
                description_cost_render = self.description_font.render(f'Cost: {int(self.upgrade8_cost)} gold  |  Balance: {self.balance} gold', True, (225, 255, 255))
                screen.blit(description_cost_render, (135, 765))
            buy_render = self.buy_font.render('BUY', True, (0, 0, 0))
            screen.blit(buy_render, (588, 718))
        if self.message_timer and self.message_timer_counter <= 15:
            self.give_feedback()
        else:
            self.message_timer_counter = 0
            self.message_timer = False

        clock.tick(15)
        pygame.display.update()


st = SkillTree()










class userProfile:
    def __init__(self):
        self.active = True
        self.offset1 = 50
        self.offset2 = 50

        self.profile_box1 = pygame.Rect(85, 225-self.offset1, 130, 45)
        self.profile_border_box1 = pygame.Rect(78, 218-self.offset1, 144, 59)
        self.reset_profile1 = pygame.Rect(300, 220-self.offset1, 115, 55)
        self.reset_profile1_border = pygame.Rect(293, 213-self.offset1, 129, 69)

        self.profile_box2 = pygame.Rect(85, 322-self.offset1+25, 130, 45)
        self.profile_border_box2 = pygame.Rect(78, 315-self.offset1+25, 144, 59)
        self.reset_profile2 = pygame.Rect(300, 317-self.offset1+25, 115, 55)
        self.reset_profile2_border = pygame.Rect(293, 310-self.offset1+25, 129, 69)

        self.profile_box3 = pygame.Rect(85, 419, 130, 45)
        self.profile_border_box3 = pygame.Rect(78, 412, 144, 59)
        self.reset_profile3 = pygame.Rect(300, 414, 115, 55)
        self.reset_profile3_border = pygame.Rect(293, 407, 129, 69)

        self.profile_box4 = pygame.Rect(85, 516+self.offset1-25, 130, 45)
        self.profile_border_box4 = pygame.Rect(78, 509+self.offset1-25, 144, 59)
        self.reset_profile4 = pygame.Rect(300, 511+self.offset1-25, 115, 55)
        self.reset_profile4_border = pygame.Rect(293, 504+self.offset1-25, 129, 69)

        self.profile_box5 = pygame.Rect(85, 613+self.offset1, 130, 45)
        self.profile_border_box5 = pygame.Rect(78, 606+self.offset1, 144, 59)
        self.reset_profile5 = pygame.Rect(300, 608+self.offset1, 115, 55)
        self.reset_profile5_border = pygame.Rect(293, 601+self.offset1, 129, 69)
        self.info_background = pygame.Rect(500, 75, 275, 715)

        self.back_background_border = pygame.Rect(15, 15, 143, 68)
        self.back_background = pygame.Rect(23, 23, 127, 52)

        self.down_offset = 75

        self.profile_font = pygame.font.SysFont('Garamond', 32, bold=1)
        self.reset_font = pygame.font.SysFont('Garamond', 26, bold=1)
        self.balance_font = pygame.font.SysFont('Garamond', 30, bold=1)
        self.info_font = pygame.font.SysFont('Garamond', 36, bold=1)
        self.back_font = pygame.font.SysFont('Garamond', 36, bold=1)
        self.reset_confirmation_font = pygame.font.SysFont('Garamond', 32, bold=1)

        self.info_font.set_underline(True)
        self.info_font.set_italic(True)

        self.reset_confirm_border1_box = pygame.Rect(35, 260, 430, 230)
        self.reset_confirm_border2_box = pygame.Rect(40, 265, 420, 220)
        self.reset_confirm_border3_box = pygame.Rect(45, 270, 410, 210)
        self.reset_confirm_box = pygame.Rect(50, 275, 400, 200)
        self.awaiting_confirmation = False
        self.reset_negative_box = pygame.Rect(115, 400, 95, 55)
        self.reset_negative_border_box = pygame.Rect(110, 395, 105, 65)
        self.reset_affirmative_box = pygame.Rect(310, 400, 95, 55)
        self.reset_affirmative_border_box = pygame.Rect(305, 395, 105, 65)

        self.reset = False

    def user_profile_menu(self):
        pd.load_upgrades_into_game()
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    global game
                    game = False
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.profile_box1.collidepoint(event.pos) or self.profile_border_box1.collidepoint(event.pos):
                        if pd.profile_id != 1:
                            pd.change_profile(1)
                            pd.load_upgrades_into_game()
                    if self.reset_profile1.collidepoint(event.pos) or self.reset_profile1_border.collidepoint(event.pos):
                        self.confirm_reset()
                        if self.reset:
                            pd.reset_profile(1)
                            pd.load_upgrades_into_game()
                            self.reset = False
                    if self.profile_box2.collidepoint(event.pos) or self.profile_border_box2.collidepoint(event.pos):
                        if pd.profile_id != 2:
                            pd.change_profile(2)
                            pd.load_upgrades_into_game()
                    if self.reset_profile2.collidepoint(event.pos) or self.reset_profile2_border.collidepoint(event.pos):
                        self.confirm_reset()
                        if self.reset:
                            pd.reset_profile(2)
                            pd.load_upgrades_into_game()
                            self.reset = False
                    if self.profile_box3.collidepoint(event.pos) or self.profile_border_box3.collidepoint(event.pos):
                        if pd.profile_id != 3:
                            pd.change_profile(3)
                            pd.load_upgrades_into_game()
                    if self.reset_profile3.collidepoint(event.pos) or self.reset_profile3_border.collidepoint(event.pos):
                        self.confirm_reset()
                        if self.reset:
                            pd.reset_profile(3)
                            pd.load_upgrades_into_game()
                            self.reset = False
                    if self.profile_box4.collidepoint(event.pos) or self.profile_border_box4.collidepoint(event.pos):
                        if pd.profile_id != 4:
                            pd.change_profile(4)
                            pd.load_upgrades_into_game()
                    if self.reset_profile4.collidepoint(event.pos) or self.reset_profile4_border.collidepoint(event.pos):
                        self.confirm_reset()
                        if self.reset:
                            pd.reset_profile(4)
                            pd.load_upgrades_into_game()
                            self.reset = False
                    if self.profile_box5.collidepoint(event.pos) or self.profile_border_box5.collidepoint(event.pos):
                        if pd.profile_id != 5:
                            pd.change_profile(5)
                            pd.load_upgrades_into_game()
                    if self.reset_profile5.collidepoint(event.pos) or self.reset_profile5_border.collidepoint(event.pos):
                        self.confirm_reset()
                        if self.reset:
                            pd.reset_profile(5)
                            pd.load_upgrades_into_game()
                            self.reset = False
                    if self.back_background.collidepoint(event.pos) or self.back_background_border.collidepoint(event.pos):
                        global up
                        up = userProfile()
                        self.active = False
                        main_menu()

            screen.blit(dungeonBackground, (0, 0))

            pygame.draw.rect(screen, (0,0,0), self.back_background_border, border_radius=15)
            pygame.draw.rect(screen, (255,0,0), self.back_background, border_radius=15)
            back_render = self.back_font.render('Back', True, (225, 255, 255))
            screen.blit(back_render, (45, 26))

            if pd.profile_id == 1:
                pygame.draw.rect(screen, (80,83,241), self.profile_border_box1)
            else:
                pygame.draw.rect(screen, (137,137,137), self.profile_border_box1)

            pygame.draw.rect(screen, (134,214,216), self.profile_box1)
            pygame.draw.ellipse(screen, (137,137,137), self.reset_profile1_border)
            pygame.draw.ellipse(screen, (134,214,216), self.reset_profile1)
            profile1_render = self.profile_font.render(f'Profile 1', True, (0, 0, 0))
            screen.blit(profile1_render, (92, 230-self.offset1))
            reset1_render = self.reset_font.render(f'RESET', True, (0, 0, 0))
            screen.blit(reset1_render, (315, 233-self.offset1))

            if pd.profile_id == 2:
                pygame.draw.rect(screen, (80,83,241), self.profile_border_box2)
            else:
                pygame.draw.rect(screen, (137,137,137), self.profile_border_box2)

            pygame.draw.rect(screen, (134,214,216), self.profile_box2)
            pygame.draw.ellipse(screen, (137,137,137), self.reset_profile2_border)
            pygame.draw.ellipse(screen, (134,214,216), self.reset_profile2)
            profile2_render = self.profile_font.render(f'Profile 2', True, (0, 0, 0))
            screen.blit(profile2_render, (92, 327-self.offset1+25))
            reset2_render = self.reset_font.render(f'RESET', True, (0, 0, 0))
            screen.blit(reset2_render, (315, 330-self.offset1+25))

            if pd.profile_id == 3:
                pygame.draw.rect(screen, (80,83,241), self.profile_border_box3)
            else:
                pygame.draw.rect(screen, (137,137,137), self.profile_border_box3)

            pygame.draw.rect(screen, (134,214,216), self.profile_box3)
            pygame.draw.ellipse(screen, (137,137,137), self.reset_profile3_border)
            pygame.draw.ellipse(screen, (134,214,216), self.reset_profile3)
            profile3_render = self.profile_font.render(f'Profile 3', True, (0, 0, 0))
            screen.blit(profile3_render, (92, 424))
            reset3_render = self.reset_font.render(f'RESET', True, (0, 0, 0))
            screen.blit(reset3_render, (315, 427))

            if pd.profile_id == 4:
                pygame.draw.rect(screen, (80,83,241), self.profile_border_box4)
            else:
                pygame.draw.rect(screen, (137,137,137), self.profile_border_box4)

            pygame.draw.rect(screen, (134,214,216), self.profile_box4)
            pygame.draw.ellipse(screen, (137,137,137), self.reset_profile4_border)
            pygame.draw.ellipse(screen, (134,214,216), self.reset_profile4)
            profile4_render = self.profile_font.render(f'Profile 4', True, (0, 0, 0))
            screen.blit(profile4_render, (92, 521+self.offset1-25))
            reset4_render = self.reset_font.render(f'RESET', True, (0, 0, 0))
            screen.blit(reset4_render, (315, 524+self.offset1-25))

            if pd.profile_id == 5:
                pygame.draw.rect(screen, (80,83,241), self.profile_border_box5)
            else:
                pygame.draw.rect(screen, (137,137,137), self.profile_border_box5)

            pygame.draw.rect(screen, (134,214,216), self.profile_box5)
            pygame.draw.ellipse(screen, (137,137,137), self.reset_profile5_border)
            pygame.draw.ellipse(screen, (134,214,216), self.reset_profile5)
            profile5_render = self.profile_font.render(f'Profile 5', True, (0, 0, 0))
            screen.blit(profile5_render, (92, 618+self.offset1))
            reset5_render = self.reset_font.render(f'RESET', True, (0, 0, 0))
            screen.blit(reset5_render, (315, 621+self.offset1))

            pygame.draw.rect(screen, (186,166,142), self.info_background)

            balance_render = self.balance_font.render(f'Balance: {pd.balance} gold', True, (0, 0, 0))
            screen.blit(balance_render, (515, 150))

            info_render = self.info_font.render(f'User Info:', True, (0, 0, 0))
            screen.blit(info_render, (552, 100))

            levels = [1, 2, 3, 4, 5, 6, 7, 8]

            for c in levels:
                level_list = []
                selected_level = 0
                full = 0
                empty = 0
                if c == 1:
                    selected_level = 1
                    full = int(pd.upgrade1_level)
                    empty = int(5 - pd.upgrade1_level)
                if c == 2:
                    selected_level = 2
                    full = int(pd.upgrade2_level)
                    empty = int(5 - pd.upgrade2_level)
                if c == 3:
                    selected_level = 3
                    full = int(pd.upgrade3_level)
                    empty = int(5 - pd.upgrade3_level)
                if c == 4:
                    selected_level = 4
                    full = int(pd.upgrade4_level)
                    empty = int(5 - pd.upgrade4_level)
                if c == 5:
                    selected_level = 5
                    full = int(pd.upgrade5_level)
                    empty = int(5 - pd.upgrade5_level)
                if c == 6:
                    selected_level = 6
                    full = int(pd.upgrade6_level)
                    empty = int(5 - pd.upgrade6_level)
                if c == 7:
                    selected_level = 7
                    full = int(pd.upgrade7_level)
                    empty = int(5 - pd.upgrade7_level)
                if c == 8:
                    selected_level = 8
                    full = int(pd.upgrade8_level)
                    empty = int(5 - pd.upgrade8_level)

                if full:
                    i = 0
                    while i <= full - 1:
                        level_list.append('full')
                        i += 1
                if empty:
                    i = 0
                    while i <= empty - 1:
                        level_list.append('empty')
                        i += 1
                registered_level1 = False
                registered_level2 = False
                registered_level3 = False
                registered_level4 = False
                registered_level5 = False


                pygame.draw.line(screen, (0,0,0), (514, 170+(self.down_offset * selected_level)), (567,170+(self.down_offset * selected_level)), width=6) # base
                pygame.draw.line(screen, (0,0,0), (515, 170+(self.down_offset * selected_level)), (540,126+(self.down_offset * selected_level)), width=6) # left
                pygame.draw.line(screen, (0,0,0), (566, 172+(self.down_offset * selected_level)), (540,126+(self.down_offset * selected_level)), width=6) # right

                for g in level_list:
                    if not selected_level == 3:
                        if not registered_level1:
                            if g == 'full':
                                pygame.draw.circle(screen, (0,0,0), (595,148+(self.down_offset * selected_level)), 16)
                                registered_level1 = True
                                continue
                            else:
                                pygame.draw.circle(screen, (0,0,0), (595,148+(self.down_offset * selected_level)), 16, width=5)
                                registered_level1 = True
                                continue
                        if not registered_level2:
                            if g == 'full':
                                pygame.draw.circle(screen, (0,0,0), (632,148+(self.down_offset * selected_level)), 16)
                                registered_level2 = True
                                continue
                            else:
                                pygame.draw.circle(screen, (0,0,0), (632,148+(self.down_offset * selected_level)), 16, width=5)
                                registered_level2 = True
                                continue
                        if not registered_level3:
                            if g == 'full':
                                pygame.draw.circle(screen, (0,0,0), (669,148+(self.down_offset * selected_level)), 16)
                                registered_level3 = True
                                continue
                            else:
                                pygame.draw.circle(screen, (0,0,0), (669,148+(self.down_offset * selected_level)), 16, width=5)
                                registered_level3 = True
                                continue
                        if not registered_level4:
                            if g == 'full':
                                pygame.draw.circle(screen, (0,0,0), (706,148+(self.down_offset * selected_level)), 16)
                                registered_level4 = True
                                continue
                            else:
                                pygame.draw.circle(screen, (0,0,0), (706,148+(self.down_offset * selected_level)), 16, width=5)
                                registered_level4 = True
                                continue
                        if not registered_level5:
                            if g == 'full':
                                pygame.draw.circle(screen, (0,0,0), (743,148+(self.down_offset * selected_level)), 16)
                                registered_level5 = True
                                level_list.clear()
                                continue
                            else:
                                pygame.draw.circle(screen, (0,0,0), (743,148+(self.down_offset * selected_level)), 16, width=5)
                                registered_level5 = True
                                level_list.clear()
                                continue
                    else:
                        if g == 'full':
                            pygame.draw.circle(screen, (0,0,0), (595,148+(self.down_offset * selected_level)), 16)
                            registered_level1 = True
                            continue
                        else:
                            pygame.draw.circle(screen, (0,0,0), (595,148+(self.down_offset * selected_level)), 16, width=5)
                            registered_level1 = True
                            continue

            clock.tick(15)
            pygame.display.update()

    def confirm_reset(self):
        self.awaiting_confirmation = True
        while self.awaiting_confirmation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    global game
                    game = False
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.reset_affirmative_box.collidepoint(event.pos) or self.reset_affirmative_border_box.collidepoint(event.pos):
                        self.reset = True
                        self.awaiting_confirmation = False
                    if self.reset_negative_box.collidepoint(event.pos) or self.reset_negative_border_box.collidepoint(event.pos):
                        self.reset = False
                        self.awaiting_confirmation = False


            pygame.draw.rect(screen, (0,0,0), self.reset_confirm_border1_box)
            pygame.draw.rect(screen, (255,0,0), self.reset_confirm_border2_box)
            pygame.draw.rect(screen, (0,0,0), self.reset_confirm_border3_box)
            pygame.draw.rect(screen, (150,150,150), self.reset_confirm_box)
            pygame.draw.rect(screen, (0,0,0), self.reset_affirmative_border_box)
            pygame.draw.rect(screen, (255,253,208), self.reset_affirmative_box)
            pygame.draw.rect(screen, (0,0,0), self.reset_negative_border_box)
            pygame.draw.rect(screen, (255,253,208), self.reset_negative_box)
            reset_confirmation_render = self.reset_confirmation_font.render('Delete Data For:', True, (225, 255, 255))
            screen.blit(reset_confirmation_render, (135, 290))
            reset_confirmation2_render = self.reset_confirmation_font.render(f'Profile {pd.profile_id} ?', True, (225, 255, 255))
            screen.blit(reset_confirmation2_render, (185, 325))
            reset_negative_render = self.reset_confirmation_font.render(f'No', True, (0,0,0))
            screen.blit(reset_negative_render, (140, 410))
            reset_affirmative_render = self.reset_confirmation_font.render(f'Yes', True, (0,0,0))
            screen.blit(reset_affirmative_render, (335, 410))
            clock.tick(15)
            pygame.display.update()


up = userProfile()


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
        if click[0] == 1 and action is not None:
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
                pd.load_upgrades_into_game()
                reset_stats()
                pause = False
                game = True
                activate_bullet = True
                bullet_timer1 = 2
                bullet_timer2 = 0
            elif action == "main_menu":
                main_menu()
            elif action == "skilltree":
                pd.load_skill_tree()
                st.load_data()
                st.skill_tree()
            elif action == "profile":
                up.user_profile_menu()
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
timer_font = pygame.font.SysFont('Garamond', 64, bold=True)
fps_font = pygame.font.SysFont('Garamond', 28, bold=True)

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
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    gametimer = font.render(str(text), True, text_color).convert_alpha()
    if isFullscreen:
        screen.blit(gametimer, ((screen_width - 150), 20))
    else:
        screen.blit(gametimer, (675, 15))


# function to show the frames per second in the corner
def display_fps(text, font, text_color):
    text = str(int(text))
    # print(text)
    fps_display = font.render(text, True, text_color).convert_alpha()
    # print(fps_display)
    screen.blit(fps_display, (20, 20))



# adds the ability to fullscreen the game
def fullscreen_toggle():
    global isFullscreen, screen_width, screen_height
    info = pygame.display.Info()
    tempwidth, tempheight = info.current_w, info.current_h
    if tempwidth != 800:
        window = pygame.display.set_mode((800, 800))
        screen_width = 800
        screen_height = 800
        isFullscreen = False
    else:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        isFullscreen = True
    pygame.display.update()


# function to show the credits menu, which will contain the credits to all resources used
def credits():
    start_time = pygame.time.get_ticks()
    global pause, screen_width, screen_height
    pause = True

    while pause:
        global gameTimerStr
        global gameTime
        temp_timer = pygame.time.get_ticks() - gameTime
        xpB.pauseTimer = temp_timer
        # if you press escape, you go back to the settings menu
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and (pygame.time.get_ticks() - start_time >= 300):
            main_menu()
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
    global pause, screen_width, screen_height
    while pause:
        global gameTime
        temp_timer = pygame.time.get_ticks() - gameTime
        xpB.pauseTimer = temp_timer
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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
        button("Play!", (screen_width / 4) - 100, (screen_height / 1.5), 200, 100, (219, 68, 68), (181, 47, 47),
               "Play")
        button("Close :(", (screen_width / 1.3) - 100, (screen_height / 1.5), 200,
               100, (247, 167, 82),
               (184, 120, 51), "Quit")
        button("Profiles", (screen_width / 4) - 100, (screen_height / 2), 200, 100, (247, 167, 82), (184, 120, 51),
               "profile")
        button("Skilltree", (screen_width / 1.3) - 100, (screen_height / 2), 200,
               100, (247, 167, 82),
               (184, 120, 51), "skilltree")
        button("Credits", (screen_width / 2) - 92.5, (screen_height / 1.5), 200, 100, (247, 167, 82), (184, 120, 51),
               "Credits")
        button("Settings", (screen_width / 2) - 92.5, (screen_height / 2), 200,
               100, (247, 167, 82),
               (184, 120, 51), "Settings")
        # puts all of the text on the screen
        screen.blit(text_surf, text_rect)
        screen.blit(text_surf2, text_rect2)
        pygame.display.update()
        clock.tick(15)


def death_screen():
    # displays a death screen if the player dies
    global pause, screen_width, screen_height, game
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
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and (pygame.time.get_ticks() - start_time >= 300):
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
        if pygame.key.get_pressed()[pygame.K_ESCAPE] and (pygame.time.get_ticks() - start_time >= 300):
            main_menu()
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
    if p.current_health <= 0:
        if pd.upgrade3_level and p.revive_available:
            p.current_health = int(p.max_health * 0.75)
            p.revive_available = False
        else:
            prevGameTime = gameTime
            p.death = True
            # print(p.gold)
            pd.add_gold()
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
        x.travel_to_player()

    # makes the main character visible
    screen.blit(pygame.transform.scale(mc_img, (40, 35)), (p.rect.x, p.rect.y))

    bullet_timer2 = gameTime / 1000
    if b.shooting:
        activate_bullet = True
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
        # spawns the slime, checks for all collisions of the slime, and kills the slime
        enemy.generate_enemy()
        if enemy.spawned:
            enemy.check_collisions()
        enemy.activate_death()

    for bat in bats:
        # spawns the bat, checks for all collisions of the bat, and kills the bat
        bat.generate_enemy()
        if bat.spawned:
            bat.check_collisions()
        bat.activate_death()

    if int(minutes) == 1 and int(seconds) == 30:
        ee.activate = True

    if ee.activate and not ee.felled:
        ee.generate_enemy()
        ee.check_collisions()
    ee.activate_death()

    if ee.felled and not bup.upgrade_active:
        bup.generate_entity()

    if p.rect.colliderect(bup.rect) and not bup.upgrade_active and ee.felled:
        bup.check_collisions()

    if int(minutes) == 5 and int(seconds) == 00:
        com.activate = True

    if com.activate and not com.felled:
        com.generate_enemy()
        com.comactive()
        com.check_collisions()
    com.activate_death()

    if int(minutes) == 0 and int(seconds) == 3:
        ma.activate = True

    if ma.activate and not ma.felled:
        ma.generate_enemy()
        ma.active()
        ma.check_collisions()
    ma.activate_death()
    #print(ma.health)

    if int(minutes) == 10 and int(seconds) == 00:
        # skeleton king spawns once the game time reaches a minute and thirty seconds
        sk.activate = True

    if sk.activate and not sk.felled:
        # if the skeleton king has spawned and not been killed, have them follow around the player
        sk.generate_enemy()
        sk.check_collisions()
        sk.follow_mc()
        sk.attack()
    sk.activate_death()

    for enemy in enemies:
        enemy.clean_dictionaries()

    for bat in bats:
        bat.clean_dictionaries()
        bat.decide_action()
    if lz.laser_aquired == True:
        lz.laser_timer()
    counter = 0
    if len(enemies) > 6:
        for enemy in enemies:
            if enemy.spawned:
                    counter += 1
    if counter >= 6:
        cl.cl_timer()

    # print(pd.upgrade2_level)

    if (seconds == 30 or seconds == 00) and not p.generated_health:
        if p.current_health + (2 * pd.upgrade2_level) <= p.max_health:
            if pd.upgrade2_level:
                p.current_health += (2 * pd.upgrade2_level)
                p.generated_health = True
        elif p.current_health != p.max_health:
            p.current_health = p.max_health
            p.generated_health = True
    if seconds == 31 or seconds == 1:
        p.generated_health = False


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
