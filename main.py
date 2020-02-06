import pygame, os, random
from math import cos, sin, pi

width, height = 800, 500
screen = pygame.display.set_mode((800, 600))
pygame.init()
screen.fill((255, 255, 255))
civs_territory = [set(), set()]
trees_territory = set()
helicopter = True

def get_near(x, y):
    a = []
    if x % 2 == 0:
        if tiles[x - 1][y]:
            a.append([x - 1, y])
        if tiles[x - 1][y - 1]:
            a.append([x - 1, y - 1])
        if tiles[x][y - 1]:
            a.append([x, y - 1])
        if tiles[x][y + 1]:
            a.append([x, y + 1])
        if tiles[x + 1][y]:
            a.append([x + 1, y])
        if tiles[x + 1][y - 1]:
            a.append([x + 1, y - 1])
        a.append([x, y])
    else:
        if tiles[x - 1][y]:
            a.append([x - 1, y])
        if tiles[x - 1][y + 1]:
            a.append([x - 1, y + 1])
        if tiles[x][y - 1]:
            a.append([x, y - 1])
        if tiles[x][y + 1]:
            a.append([x, y + 1])
        if tiles[x + 1][y]:
            a.append([x + 1, y])
        if tiles[x + 1][y + 1]:
            a.append([x + 1, y + 1])
        a.append([x, y])
    return a

def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        if not helicopter:
            image = pygame.transform.scale(image, (40, 40))
    else:
        image = image.convert_alpha()
    return image



def start_screen():
    global helicopter
    intro_text = ["Antiyoy", "Любая клавиша чтобы продолжить..."]
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon.png'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 500
    string_rendered = font.render(intro_text[1], 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 100
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    text_coord = 100
    string_rendered = font.render(intro_text[0], 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 330
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                helicopter = False
                return  # начинаем игру

        pygame.display.flip()

pygame.mixer.music.load('fon_music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.01)
start_screen()

def win_screen(n):
    global helicopter, running
    helicopter = True
    intro_text = ["Победа игрока " + str(n)]
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon.png'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    string_rendered = font.render(intro_text[0], 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 330
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                running = False
                return
            helicopter = False
        pygame.display.flip()

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        f30 = pi / 6
        f60 = pi / 3
        f = 0
        color = (200, 200, 200)
        for j in range(len(level[0])):
            for i in range(len(level)):
                if level[j][i] == ".":
                    continue
                if level[j][i] == "1":
                    if (i, j) in can_place:
                        color = (255, 160, 160)
                    else:
                        color = (255, 200, 200)
                elif level[j][i] == "2":
                    if (i, j) in can_place:
                        color = (160, 160, 255)
                    else:
                        color = (200, 200, 255)
                else:
                    if (i, j) in can_place and who_turn_is_it == 1:
                        color = (255, 230, 230)
                    elif (i, j) in can_place and who_turn_is_it == 2:
                        color = (230, 230, 255)
                    else:
                        color = (200, 200, 200)
                if level[j][i] == str(who_turn_is_it) and tiles[j][i].unit == "C":
                    color = (255, 215, 0)
                f = 20 if j % 2 == 1 else 0
                a = []
                for k in range(6):
                    x = 20 * cos(f30 + k * f60) + self.left + 40 * i + f
                    y = 20 * sin(f30 + k * f60) + self.top + 35 * j
                    a.append([x, y])
                pygame.draw.polygon(screen, color, a, 0)
        color = (0, 255, 0)
        for j in range(len(level[0])):
            for i in range(len(level)):
                if level[j][i] == ".":
                    continue
                f = 20 if j % 2 == 1 else 0
                a = []
                for k in range(6):
                    x = 20 * cos(f30 + k * f60) + self.left + 40 * i + f
                    y = 20 * sin(f30 + k * f60) + self.top + 35 * j
                    a.append([x, y])
                pygame.draw.polygon(screen, color, a, 2)

    def get_left_click(self, mouse_pos):
        global carring
        if mouse_pos[1] < h - 140:
            cell = self.get_cell(mouse_pos)
            self.on_click(cell)
        else:
            x, y = mouse_pos
            if 230 < x < 310 and h - 140 < y < h - 60 and workers_prices[item1.n][0] <= money[who_turn_is_it]:
                carring = True
                carry.bought = True
                carry.update_img(item1.image, x, y, 1)
                color_pole()
            if 460 < x < 740 and h - 140 < y < h - 60 and houses_prices[item2.n] <= money[who_turn_is_it]:
                carring = True
                carry.bought = True
                carry.update_img(item2.image, x, y, 2)
                color_pole()



    def get_right_click(self, mouse_pos):
        global carring, can_place
        x, y = mouse_pos
        if 230 < x < 310 and h - 140 < y < h - 60:
            item1.update_img()
            return
        if 460 < x < 740 and h - 140 < y < h - 60:
            item2.update_img()
            return
        carring = False
        carry.bought = False
        carry.update_img(tile_images['worker1'], -100, -100, 1)
        carry.current_id = 0
        can_place = set()

    def get_cell(self, pos):
        x, y = pos
        if y >= h - 140:
            return None
        x3, y3 = 0, 0
        for j in range(len(level[0])):
            for i in range(len(level)):
                if level[j][i] == ".":
                    continue
                f = 20 if j % 2 == 1 else 0
                x2 = self.left + 40 * i + f
                y2 = self.top + 35 * j
                d = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
                if d < 20:
                    x3, y3 = j, i

        return (x3, y3) if x3 + y3 else None

    def on_click(self, cell):
        global carring, civs_territory, can_place
        #print(civs_territory)
        #print(cell)
        if not cell:
            return
        f = False
        f2 = False
        max_wor = -1
        cas = [False, False, False]
        a = get_near(cell[0], cell[1])
        for i in a:
            if tiles[i[0]][i[1]].kingdom == who_turn_is_it:
                f = True
            if (tiles[i[0]][i[1]].unit == "S" and tiles[i[0]][i[1]].unit_id == 0) or tiles[i[0]][i[1]].unit == "C":
                f2 = True
            if tiles[i[0]][i[1]].kingdom != who_turn_is_it and tiles[i[0]][i[1]].unit in "WS":
                max_wor = max(max_wor, tiles[i[0]][i[1]].unit_id)
        if f and carring:
            if tiles[cell[0]][cell[1]].unit not in "#PT" and tiles[cell[0]][cell[1]].kingdom == who_turn_is_it:
                return
            if carry.current_type == 1:
                if carry.current_id <= max_wor:
                    return
                if tiles[cell[0]][cell[1]].kingdom != who_turn_is_it and tiles[cell[0]][cell[1]].kingdom != None:
                    civs_territory[(1 if who_turn_is_it == 1 else 0)].remove((cell[1], cell[0]))
                tiles[cell[0]][cell[1]].set_img(tile_images[workers_list[carry.current_id]])
                tiles[cell[0]][cell[1]].unit = "W"
                tiles[cell[0]][cell[1]].unit_id = carry.current_id
                if carry.bought:
                    money[who_turn_is_it] -= workers_prices[item1.n][0]
            elif carry.current_type == 2:
                if tiles[cell[0]][cell[1]].kingdom != who_turn_is_it or (not f2 and carry.current_id == 0):
                    return
                tiles[cell[0]][cell[1]].set_img(tile_images[houses_list[carry.current_id]])
                tiles[cell[0]][cell[1]].unit = "S"
                tiles[cell[0]][cell[1]].unit_id = item2.n
                if carry.bought:
                    money[who_turn_is_it] -= houses_prices[item2.n]
            if carry.bought:
                if tiles[cell[0]][cell[1]].kingdom != who_turn_is_it:
                    tiles[cell[0]][cell[1]].used = True
                else:
                    tiles[cell[0]][cell[1]].used = False

            else:
                tiles[cell[0]][cell[1]].used = True
            tiles[cell[0]][cell[1]].kingdom = who_turn_is_it
            civs_territory[who_turn_is_it - 1].add((cell[1], cell[0]))
            level[cell[0]][cell[1]] = str(who_turn_is_it)

            carring = False
            tiles[cell[0]][cell[1]].activated = True
            can_place = set()
        else:
            if tiles[cell[0]][cell[1]].unit == "W" and not tiles[cell[0]][cell[1]].used and tiles[cell[0]][cell[1]].kingdom == who_turn_is_it:
                tiles[cell[0]][cell[1]].unit = "#"
                tiles[cell[0]][cell[1]].activated = False
                tiles[cell[0]][cell[1]].rect = tiles[cell[0]][cell[1]].image.get_rect().move(-100, -100)
                carring = True
                carry.bought = False
                carry.update_img(tiles[cell[0]][cell[1]].image, -100, -100, 1)
                carry.current_id = tiles[cell[0]][cell[1]].unit_id
                color_pole()




def load_level(filename):
    filename = "data/" + filename

    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))

tile_images = {'worker': load_image('man0.png'), 'house': load_image('house.png'), 'worker1': load_image('man1.png'),
               'worker2': load_image('man2.png'), 'worker3': load_image('man3.png'), 'house1': load_image('tower.png'),
               'house2': load_image('strong_tower.png'), 'palm': load_image('palm.png'), 'pine': load_image('pine.png'),
               'grave': load_image('grave.png'), "castle": load_image('castle.png')}

workers_list = ['worker', 'worker1', 'worker2', 'worker3']
houses_list = ['house', 'house1', 'house2']
workers_prices = [(10, 2), (20, 6), (30, 20), (40, 36)]
houses_prices = [12, 15, 35]
tile_width, tile_height = 40, 35
can_place = set()

level = load_level("civs_level.txt")
board = Board(len(level[0]), len(level))
board.set_view(200, 100, 40)

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, kingdom=None, unit="#"):
        super().__init__(all_sprites)
        self.type = tile_type
        self.kingdom = kingdom
        self.image = tile_images["worker"]
        self.rect = self.image.get_rect().move(-10000, -10000)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.activated = False
        self.unit = unit
        self.used = False
        self.unit_id = None
        if unit == "W":
            self.set_img(tile_images["worker"])
            self.activated = True
            self.unit_id = 0
        if unit == "C":
            self.set_img(tile_images["castle"])
            self.activated = True
            self.unit = "C"
        if unit == "T":
            self.set_img(tile_images["pine"])
            self.activated = True
        if unit == "P":
            self.set_img(tile_images["palm"])
            self.activated = True

    def set_img(self, img):
        self.image = img
        self.activated = True
        self.update()

    def update(self):
        if not self.activated:
            return
        if not self.pos_y % 2:
            self.rect = self.image.get_rect().move(board.left + tile_width * self.pos_x - 20,
                                                   board.top + tile_height * self.pos_y - 20)
        else:
            self.rect = self.image.get_rect().move(board.left + tile_width * self.pos_x,
                                                   board.top + tile_height * self.pos_y - 20)


player = None

all_sprites = pygame.sprite.Group()
shop_sprites = pygame.sprite.Group()
carry_sprites = pygame.sprite.Group()



tiles = [[0] * 100 for i in range(100)]

def generate_level(level, level2):
    global playerX, playerY, tiles, civs_territory
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                tiles[y][x] = Tile('none', x, y)
            elif level[y][x] == '#' or level2[y][x] == 'P' or level2[y][x] == 'T':
                tiles[y][x] = Tile('empty', x, y, unit=level2[y][x])
                if level2[y][x] == 'P' or level2[y][x] == 'T':
                    trees_territory.add((y, x))
            elif level[y][x] in '12':
                tiles[y][x] = Tile('territory', x, y, int(level[y][x]), level2[y][x])
                if level[y][x] == "1":
                    civs_territory[0].add((x, y))
                if level[y][x] == "2":
                    civs_territory[1].add((x, y))

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y
w, h = pygame.display.get_surface().get_size()

def draw_shop():
    pygame.draw.rect(screen, (100, 100, 100), [[0, h - 150], [w, h]], 0)

class Item(pygame.sprite.Sprite):
    def __init__(self, name, n):
        super().__init__(shop_sprites)
        self.id = n
        self.n = 0
        self.image = pygame.transform.scale(tile_images[name], (80, 80))
        self.rect = self.image.get_rect().move(230 * self.id, h - 140)

    def update_img(self):
        self.n = (self.n + 1) % (4 if self.id == 1 else 3)
        self.image = pygame.transform.scale(tile_images[(workers_list[self.n] if self.id == 1 else houses_list[self.n])], (80, 80))
        self.rect = self.image.get_rect().move(230 * self.id, h - 140)

level = load_level("civs_level.txt")
level2 = load_level("items_level.txt")
player, level_x, level_y = generate_level(level, level2)
#camera = Camera()
running = True

money = [-1, 25, 25, -1]
f1 = pygame.font.Font(None, 50)



item1 = Item("worker", 1)
item2 = Item("house", 2)

class Carry(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(carry_sprites)
        self.image = None
        self.rect = None
        self.current_type = 0
        self.current_id = 0
        self.bought = False

    def update_img(self, img, x, y, type):
        self.image = pygame.transform.scale(img, (60, 60))
        self.rect = self.image.get_rect().move(x - 30, y - 30)
        self.current_type = type
        self.current_id = item1.n if type == 1 else item2.n

    def update(self, pos):
        self.rect = self.image.get_rect().move(pos[0] - 30, pos[1] - 30)

carry = Carry()

carring = False
def count_money():
    n = 0
    for i in civs_territory[who_turn_is_it - 1]:
        a = -1
        if tiles[i[1]][i[0]].unit == "W":
            a = tiles[i[1]][i[0]].unit_id
        if a == 0:
            n -= 2
        elif a == 1:
            n -= 6
        elif a == 2:
            n -= 20
        elif a == 3:
            n -= 36
    for i in civs_territory[who_turn_is_it - 1]:
        if tiles[i[1]][i[0]].unit not in "PT":
            n += 1
        if tiles[i[1]][i[0]].unit == "S" and tiles[i[1]][i[0]].unit_id == 0:
            n += 2
    return n


def color_pole():
    global can_place
    can_place = set()
    if carry.current_type == 1:
        for x, y in civs_territory[who_turn_is_it - 1]:
            for j in get_near(y, x):
                f = True
                for k in get_near(j[0], j[1]):
                    if tiles[k[0]][k[1]].kingdom != who_turn_is_it and tiles[k[0]][k[1]].unit in "SW" and tiles[k[0]][k[1]].unit_id >= carry.current_id:
                        f = False
                if f and tiles[k[0]][k[1]].unit in "#TP":
                    can_place.add((j[1], j[0]))
    else:
        if carry.current_id == 0:
            for x, y in civs_territory[who_turn_is_it - 1]:
                j = y, x
                f = False
                for k in get_near(j[0], j[1]):
                    if tiles[k[0]][k[1]].kingdom == who_turn_is_it and ((tiles[k[0]][k[1]].unit == "S" and tiles[k[0]][k[1]].unit_id == 0) or tiles[k[0]][k[1]].unit == "C"):
                        f = True
                if f and tiles[k[0]][k[1]].unit == "#":
                    can_place.add((j[1], j[0]))
        else:
            for x, y in civs_territory[who_turn_is_it - 1]:
                if tiles[y][x].unit == "#":
                    can_place.add((x, y))



def make_trees_turn():
    b = []
    for i in trees_territory:
        a = get_near(i[0], i[1])
        for x, y in a:
            ran = random.randint(1, 5)
            if ran != 1:
                continue
            if tiles[x][y].type != "none" and tiles[x][y].unit == "#":
                if tiles[i[0]][i[1]].unit == "T":
                    tiles[x][y].set_img(tile_images["pine"])
                    tiles[x][y].unit = "T"
                if tiles[i[0]][i[1]].unit == "P":
                    tiles[x][y].set_img(tile_images['palm'])
                    tiles[x][y].unit = "P"
                b.append((x, y))
    for i in b:
        if (i[0], i[1]) not in trees_territory:
            trees_territory.add((i[0], i[1]))


def skip_turn():
    global who_turn_is_it, money, can_place
    can_place = set()
    money[who_turn_is_it] += count_money()
    who_turn_is_it = 1 if who_turn_is_it == 2 else 2
    for i in civs_territory[who_turn_is_it - 1]:
        tiles[i[1]][i[0]].used = False
    if who_turn_is_it == 1:
        make_trees_turn()


who_turn_is_it = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == 4 and event.buttons[1]:
            board.top += event.rel[1]
            board.left += event.rel[0]
            all_sprites.update()
        if event.type == 4:
            if carring:
                carry_sprites.update(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_left_click(event.pos)
            elif event.button == 3:
                board.get_right_click(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                skip_turn()

    screen.fill((255, 255, 255))

    board.render()
    all_sprites.draw(screen)
    draw_shop()
    shop_sprites.draw(screen)
    text1 = f1.render("Player " + str(who_turn_is_it) + " $" + str(money[who_turn_is_it]) + ", " + str(count_money()) + "p/m", 1, (255, 215, 0))
    screen.blit(text1, (10, 10))
    text1 = f1.render("$" + str(workers_prices[item1.n][0]) + ", -" + str(workers_prices[item1.n][1]) + " p/m", 1, (255, 215, 0))
    screen.blit(text1, (200, h - 50))
    text1 = f1.render("$" + str(houses_prices[item2.n]), 1, (255, 215, 0))
    screen.blit(text1, (470, h - 50))
    if carring:
        carry_sprites.draw(screen)
    pygame.display.flip()
    if len(civs_territory[0]) == 0:
        print("Победа игрока 2")
        win_screen(2)
    if len(civs_territory[1]) == 0:
        print("Победа игрока 1")
        win_screen(1)
pygame.quit()