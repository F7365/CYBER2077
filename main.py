import pygame
import random
import sys
import os
import pymysql


all_sprites = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
map_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
cracks_group = pygame.sprite.Group()
particles_group = pygame.sprite.Group()
sell_point = pygame.sprite.Group()


def render_map(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            Tile(map[y][x], x, y)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def generate_map():
    map_list = ['g' * 10, 'd' * 10]#2
    for i in range(2):#2
        empty_string = ''
        for j in range(10):
            empty_string+=random.choice(['d','s'])
        map_list.append(empty_string)
    for i in range(2):#2
        map_list.append('s' * 10)
    for i in range(4):#4
        empty_string = ''
        for j in range(10):
            empty_string+=random.choice(['s','a','s','a','s'])
        map_list.append(empty_string)
    map_list.append('s' * 10)#1
    for i in range(14):#14
        empty_string = ''
        for j in range(10):
            empty_string+=random.choice(['i','s','i','s','s','s','s'])
        map_list.append(empty_string)
    for i in range(5):#5
        empty_string = ''
        for j in range(10):
            empty_string+=random.choice(['z','b','z','b','b','b','i'])
        map_list.append(empty_string)
    for i in range(2):#2
        map_list.append('b' * 10)
    for i in range(4):#4
        empty_string = ''
        for j in range(10):
            empty_string+=random.choice(['l','b','l','b','b','n','r','b','b'])
        map_list.append(empty_string)
    for i in range(2):#2
        map_list.append('b' * 10)
    for i in range(4):#4
        empty_string = ''
        for j in range(10):
            empty_string+=random.choice(['e','b','e','b','n','b','r','r','b'])
        map_list.append(empty_string)
    for i in range(3):#3
        map_list.append('b' * 10)
    for i in range(4):#4
        empty_string = ''
        for j in range(10):
            empty_string+=random.choice(['w','b','b','b','b','b','n'])
        map_list.append(empty_string)
    map_list.append('b' * 10)#1
    return map_list


def start_screen():
    global load
    fon = pygame.transform.scale(load_image('start_fone.png'), (1000, 700))
    screen.blit(fon, (0, 0))
    lines = {"Cyberminer 2077": (500, 200, 140),
             "Click to Play": (500, 260, 50), 
             "New Game": (500, 420, 60), 
             "Load Game": (500, 520, 60) }
    red = 255
    clock = pygame.time.Clock()
    fontl = pygame.font.Font(None, 100)
    str_loading = fontl.render('Loading...', 1, (255, 255, 255))
    str_loading_rect = str_loading.get_rect()
    str_loading_rect.centerx = 500
    str_loading_rect.centery = 620
    to_return=False
    while True:
        if to_return:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 370<event.pos[0]<630 and 380<event.pos[1]<460: # New
                    screen.blit(str_loading, str_loading_rect)
                    to_return=True
                    load=False
                if 370<event.pos[0]<630 and 480<event.pos[1]<560: # Load
                    screen.blit(str_loading, str_loading_rect)
                    to_return=True
                    load=True
        pygame.draw.rect(screen, (0, 0, 0), (370,380,260,80))
        pygame.draw.rect(screen, (0, 0, 0), (370,480,260,80))
        for line in lines:
            font = pygame.font.Font(None, lines[line][2])
            string_rendered = font.render(line, 1, (red, 0, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.centerx = lines[line][0]
            intro_rect.centery = lines[line][1]
            screen.blit(string_rendered, intro_rect)
        
        if red <= 5:
            a = 2
        if red >= 250:
            a = -2
        red = int(red + a)
        pygame.display.flip()
        clock.tick(60)


def world_borders(width):
    Border(0, 0, width, 0)
    Border(0, 5400, width, 5400)
    Border(0, 0, 0, 5400)
    Border(width, 0, width, 5400)


def create_particles(position, material):
    for i in range(20):
        Particle(position, material)


def score_table(score_now, inventory):
    score_dict = {
            'g': 10,
            'd': 10,
            's': 20,
            'b': 60,
            'a': 40,
            'i': 80,
            'z': 200,
            'l': 500,
            'e': 450,
            'r': 400,
            'w': 1000,
            'n': 50
        }
    score = score_now
    for i in inventory:
        score+=(inventory[i]*score_dict[i])
    return score


def save_to_db(power,coef,capacity,cover,score,map,levels):
    DB_HOST = 'ildarg0a.beget.tech'
    DB_USER = 'ildarg0a_guala'
    DB_PASSWORD = 'QWERasdf0192'
    DB_NAME = 'ildarg0a_guala'
    conn = pymysql.connect(
            host=DB_HOST, port=3306, user=DB_USER, password=DB_PASSWORD, db=DB_NAME
        )
    with conn.cursor() as cur:
        try:
            sql = f"""SELECT `user` FROM miner2077"""
            cur.execute(sql)
            if (os.environ['COMPUTERNAME'],) in list(cur.fetchall()):
                sql = f"""UPDATE miner2077 SET `power`={power},`coef`={coef},`capacity`={capacity},`cover`={cover},`score`={score},`map`="{str(map)}",`levels`="{str(levels)}" WHERE `user` = '{os.environ['COMPUTERNAME']}'"""
                cur.execute(sql)
            else:
                sql = f"""INSERT INTO miner2077(`user`, `power`, `coef`, `capacity`, `cover`, `score`, `map`, `levels`) VALUES ('{os.environ['COMPUTERNAME']}', {power}, {coef}, {capacity}, {cover}, {score}, "{str(map)}", "{str(levels)}")"""
                cur.execute(sql)
            conn.commit()
        except Exception as ex:
            print(ex)


def load_from_db():
    DB_HOST = 'ildarg0a.beget.tech'
    DB_USER = 'ildarg0a_guala'
    DB_PASSWORD = 'QWERasdf0192'
    DB_NAME = 'ildarg0a_guala'
    conn = pymysql.connect(
            host=DB_HOST, port=3306, user=DB_USER, password=DB_PASSWORD, db=DB_NAME
        )
    with conn.cursor() as cur:
        try:
            sql = f"""SELECT `user` FROM miner2077"""
            cur.execute(sql)
            if (os.environ['COMPUTERNAME'],) in list(cur.fetchall()):
                sql = f"""SELECT `power`,`coef`,`capacity`,`cover`,`score`,`map`,`levels` FROM `miner2077` WHERE `user`='{os.environ['COMPUTERNAME']}'"""
                cur.execute(sql)
                return cur.fetchone()
            else:
                return
        except Exception as ex:
            print(ex)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(map_group, all_sprites)
        tile_width = 100
        tile_images = {
            'g': load_image('dirt_under_base.png'),
            'd': load_image('dirt.png'),
            's': load_image('stone.png'),
            'b': load_image('stone.png'),
            'a': load_image('amber.png'),
            'i': load_image('iron.png'),
            'z': load_image('gold.png'),
            'l': load_image('diamond.png'),
            'e': load_image('emerald.png'),
            'r': load_image('ruby.png'),
            'w': load_image('rainbow.png'),
            'n': load_image('barrel.png'),
        }
        stength_dict = {
            'g': 180,
            'd': 180,
            's': 360,
            'b': 1200,
            'a': 120,
            'i': 500,
            'z': 800,
            'l': 1440,
            'e': 1000,
            'r': 1000,
            'w': 2000,
            'n': 7200
        }
        self.destruction = 0
        self.material=tile_type
        self.xc=pos_x
        self.yc=pos_y
        self.strength = stength_dict[tile_type]
        self.image=pygame.transform.scale(tile_images[tile_type], (tile_width, tile_width))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_width * pos_y + 400)

    def animate(self, target):
        if self.destruction == 0:
            cracks_group.empty()
            for block in map_group:
                block.destruction = 0
        self.destruction += target.power
        Cracks(int(self.destruction // (self.strength / 7) + 1), self.rect.centerx, self.rect.centery)
        if self.destruction >= self.strength - target.power:
            target.add_tile(self.material)
            cracks_group.empty()
            create_particles(self.rect.center, self.material)
            self.kill()


class Miner(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.score = 0
        self.inventory={}
        self.coef = 1
        self.power = 1
        self.capacity = 5
        self.leftimage = pygame.transform.scale(load_image('miner.png', -1), (80, 80))
        self.rightimage = pygame.transform.flip(self.leftimage, True, False)
        self.downimage = pygame.transform.rotate(self.leftimage, 90)
        self.image = self.leftimage
        self.rect = self.image.get_rect().move(460, 330)
    
    def add_tile(self, material):
        if material in self.inventory:
            self.inventory[material]+=1
        else:
            self.inventory[material]=1

    def update(self):
        if pygame.sprite.spritecollideany(miner, sell_point) and len(self.inventory) != 0:
            self.score = score_table(self.score, self.inventory)
            self.inventory = {}
            save_to_db(self.power,self.coef,self.capacity,COVER,self.score,list(map(lambda x: (x.material, x.xc, x.yc),map_group)),list(map(lambda x: x.level ,ShopList)))
        score_font = pygame.font.Font(None, 50)
        str_score = score_font.render(f'Points: {self.score}$', 1, (255, 255, 255))
        str_score_rect = str_score.get_rect()
        str_score_rect.x = 740
        str_score_rect.y = 15
        screen.blit(str_score, str_score_rect)


class Camera:
    def __init__(self):
        self.dy = 0

    def apply(self, obj):
        obj.rect.y += self.dy

    def update(self, target):
        self.dy = 350 - target.rect.centery
        background.Y += self.dy


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif y1 == y2:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        else:
            self.add(sell_point)
            self.image = pygame.Surface([x2 - x1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)


class Cracks(pygame.sprite.Sprite):
    def __init__(self, stage, cx, cy):
        super().__init__(cracks_group)
        self.destruction = 0
        tile_width = 100
        self.image = pygame.transform.scale(load_image(f'crack{stage}.png', -1), (tile_width, tile_width))
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy


class Background:
    def __init__(self):
        self.base = pygame.transform.scale(load_image('base.png'), (1000, 650))
        self.dirt_fon = pygame.transform.scale(load_image('dirt_fone.png'), (1000, 400))
        self.stone_fone = pygame.transform.scale(load_image('stone_fone.png'), (1000, 4600))
        self.end = pygame.transform.scale(load_image('end.png'), (1000, 400))
        self.Y = -250

    def update(self):
        screen.blit(self.base, (0, self.Y))
        screen.blit(self.dirt_fon, (0, 650 + self.Y))
        screen.blit(self.stone_fone, (0, 1050 + self.Y))
        screen.blit(self.end, (0, 5650 + self.Y))


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, material):
        super().__init__(particles_group)
        self.fire = []
        for scale in (5, 8, 11):
            if material=='d' or material=='g':
                self.fire.append(pygame.transform.scale(load_image("dirt.png"), (scale, scale)))
            else:
                self.fire.append(pygame.transform.scale(load_image("stone.png"), (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [random.choice(range(-5, 6)), random.choice(range(-5, 6))]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, 1000, 700)):
            self.kill()


class Shop:
    def __init__(self, x, image_file, mode):
        prices = {0:[250,500,900,1550,2000,0],
        1:[200,400,700,1500,2000,0],
        2:[200,450,800,1600,2000,0]}
        self.x = x
        self.level = 0
        self.prices = prices[mode]
        self.icon = pygame.transform.scale(load_image(image_file), (40, 40))
        self.mode = mode

    def clicked(self, pos, target):
        data = {0:[1,3,5,7,9,11],
        1:[5,8,11,14,17,20],
        2:[1,1.2,1.4,1.6,1.8,2]}
        if self.x+3<pos[0]<self.x+147 and 8<pos[1]<52 and self.level!=5 and target.score - self.prices[self.level] >=0:
            target.score = target.score - self.prices[self.level]
            self.level+=1
            if self.mode == 0:
                target.power = data[0][self.level]
            elif self.mode == 1:
                target.capacity = data[1][self.level]
            else:
                target.coef = data[2][self.level]

    def update(self):
        level_color = {0:(200,200,200),
                1:(0,200,0),
                2:(0,200,230),
                3:(175,30,255),
                4:(220,0,0),
                5:(240,240,0)}
        pygame.draw.rect(screen, level_color[self.level], (self.x, 5, 150, 50))
        pygame.draw.rect(screen, (0,0,0), (self.x, 5, 150, 50), 3)
        if self.prices[self.level] != 0:
            cost_font = pygame.font.Font(None, 40)
            str_cost = cost_font.render(f'{self.prices[self.level]}$', 1, (0, 0, 0))
            str_cost_rect = str_cost.get_rect()
            str_cost_rect.centerx = self.x+90
            str_cost_rect.centery = 30
            screen.blit(str_cost, str_cost_rect)
        screen.blit(self.icon, (self.x+5, 10))


if __name__ == '__main__':

    pygame.init()
    size = 1000, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Cyberminer 2077')

    start_screen()
    if not load:
        render_map(generate_map())
    world_borders(size[0])
    background = Background()
    miner = Miner()
    camera = Camera()
    Border(465, 323, 535, 333)
    ShopList = []
    for d in range(3):
        image_cats = {0:'mine_cat.png',
        1:'box_cat.png',
        2:'speed_cat.png'}
        ShopList.append(Shop(d*180+(d+1)*50, image_cats[d], d))
    
    running = True
    clock = pygame.time.Clock()
    if not load:    
        COVER = map_group.sprites()[0].rect.y

    if load:
        data_db = load_from_db()
        if data_db is not None:
            COVER = data_db[3]
            miner.power = data_db[0]
            miner.coef = data_db[1]
            miner.capacity = data_db[2]
            miner.score = data_db[4]
            for tile_data in str(data_db[5]).lstrip('[').rstrip(']').split('), '):
                tile_data_f = tile_data.lstrip('(').rstrip(')').split(', ')
                Tile(tile_data_f[0].strip("'"),int(tile_data_f[1]),int(tile_data_f[2]))
            for i in range(3):
                ShopList[i].level=int(data_db[6][3*i+1])


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for mmenu in ShopList:
                    mmenu.clicked(event.pos, miner)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            state = True
            miner.image = miner.leftimage
            if not pygame.sprite.spritecollideany(miner, vertical_borders) and not pygame.sprite.spritecollideany(miner,
                                                                                                                  map_group):
                miner.rect = miner.rect.move(-4*miner.coef, 0)
            for border in vertical_borders:
                if pygame.sprite.collide_rect(miner, border):
                    if border.rect.centerx > miner.rect.centerx:
                        miner.rect = miner.rect.move(-4*miner.coef, 0)
                        state = True
                        break
                    else:
                        state = False
            if state:
                for block in map_group:
                    if pygame.sprite.collide_rect(miner, block):
                        if block.rect.y + 100 < miner.rect.centery:
                            continue
                        if abs(block.rect.y - miner.rect.y) < 50:
                            if miner.rect.x - block.rect.x >= 80:
                                if sum(miner.inventory.values())<miner.capacity:
                                    block.animate(miner)
                                break
                            else:
                                miner.rect = miner.rect.move(-4*miner.coef, 0)
                                break
                        else:
                            miner.rect = miner.rect.move(-4*miner.coef, 0)
                            break
        if keys[pygame.K_d]:
            state = True
            miner.image = miner.rightimage
            if not pygame.sprite.spritecollideany(miner, vertical_borders) and not pygame.sprite.spritecollideany(miner, map_group):
                miner.rect = miner.rect.move(4*miner.coef, 0)
            for border in vertical_borders:
                if pygame.sprite.collide_rect(miner, border):
                    if border.rect.centerx < miner.rect.centerx:
                        miner.rect = miner.rect.move(4*miner.coef, 0)
                        state = True
                        break
                    else:
                        state = False
            if state:
                for block in map_group:
                    if pygame.sprite.collide_rect(miner, block):
                        if block.rect.y + 100 < miner.rect.centery:
                            continue
                        if abs(block.rect.y - miner.rect.y) < 61:
                            if block.rect.x - miner.rect.x <= 80 and block.rect.x - miner.rect.x >= 0:
                                if sum(miner.inventory.values())<miner.capacity:
                                    block.animate(miner)
                                break
                            else:
                                miner.rect = miner.rect.move(4*miner.coef, 0)
                                break
                        else:
                            miner.rect = miner.rect.move(4*miner.coef, 0)
                            break
        if keys[pygame.K_s]:
            state=True
            miner.image = miner.downimage
            for block in map_group:
                if pygame.sprite.collide_rect(miner, block) and block.rect.centery >= miner.rect.centery:
                    state=False
                    if miner.rect.centerx - block.rect.x <= 100:
                        if sum(miner.inventory.values())<miner.capacity:
                            block.animate(miner)
                        break
                    else:
                        continue
            if state and not pygame.sprite.spritecollideany(miner, horizontal_borders):
                miner.rect=miner.rect.move(0,4*miner.coef)
        if keys[pygame.K_w]:
            state = True
            miner.image = miner.leftimage
            for block in map_group:
                if pygame.sprite.collide_rect(miner, block):
                    if block.rect.y + 80 <= miner.rect.y:
                        state = False
                        break
                else:
                    if COVER - 70 >= miner.rect.y:
                        state = False
                        break
            if state:
                miner.v = 0
                miner.dv = 0
                miner.rect = miner.rect.move(0, -2*miner.coef)
        if not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
            miner.image = miner.leftimage
            cracks_group.empty()
            for block in map_group:
                block.destruction = 0
        
        camera.update(miner)
        background.update()
        COVER+=350-miner.rect.centery
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in cracks_group:
            camera.apply(sprite)
        all_sprites.update()
        particles_group.update()
        map_group.draw(screen)
        cracks_group.draw(screen)
        player_group.draw(screen)
        particles_group.draw(screen)

        miner.update()
        for mmenu in ShopList:
            mmenu.update()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()