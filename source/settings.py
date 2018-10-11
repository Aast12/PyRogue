from random import randint

import pyglet

import source.resources as res

scenes = {
    'menu_batch' : pyglet.graphics.Batch(),
    'game_batch' : pyglet.graphics.Batch(),
    'enemies' : pyglet.graphics.Batch(),
    'gameover_batch' : pyglet.graphics.Batch()
}

SETTINGS = {
    'Title' : 'PyRogue',
    'Font' : 'Source Code Pro Light',
    'Width' : 1400,
    'Height' : 680
}

TEXTURES = {
    '+': res.dungeon_texture[3],
    '*': res.dungeon_texture[4],
    '-': res.dungeon_texture[8],
    '|': res.dungeon_texture[5],
    '#': res.dungeon_texture[7],
    '.': res.dungeon_texture[6],
    'S': res.stairs,
    'A': res.entities_texture[7],
    'B': res.entities_texture[8],
    'C': res.entities_texture[3],
    'D': res.entities_texture[4],
    'E': res.entities_texture[5],
    'F': res.entities_texture[0],
    'G': res.entities_texture[1],
    'H': res.entities_texture[2],
    '@': res.entities_texture[6]
}

class Person:
    def __init__(self, char, hp, atk, x, y, batch = None):
        self.alive = True
        self.char = char
        self.hp = hp
        self.atk = atk
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(TEXTURES[char], x, y, batch = batch)

    def set_x(self, x):
        self.sprite.x = x * (16) + 32

    def set_y(self, y):
        self.sprite.y = SETTINGS['Height'] - 16 * (y + 1) - 16

    def set_visible(self, bool):
        self.sprite.visible = bool

    def make_damage(self, target):
        dmg = randint(1, self.atk)
        target.hp -= dmg
        print(self.char, "made", dmg, "points of damage to", target.char)
        if target.hp <= 0:
            target.alive = False
            self.set_visible(False)
            print(self.char, "killed", target.char)

    def update(self):
        self.set_x(self.x)
        self.set_y(self.y)
        if self.hp <= 0:
            self.alive = False

class Player(Person):
    def __init__(self, name, char, hp, atk, x, y, batch = None):
        super().__init__(char, hp, atk, x, y, batch)
        self.name = name

class Tile:
    def __init__(self, char, x, y, batch, visited = False, visible = False):
        self.char = char
        self.x = x
        self.y = y
        self.batch = batch
        self.object = None
        self.visited = visited
        self.sprite = pyglet.sprite.Sprite(TEXTURES[char], x, y, batch = batch)
        self.sprite.visible = visible
        if char == '+':
            self.opened = False

    def set_visible(self, bool):
        self.sprite.visible = bool

    def set_texture(self, texture):
        self.sprite = pyglet.sprite.Sprite(texture, self.x,
                                           self.y, batch = self.batch)

player = Player('ROGUE', '@', 100, 50, 2, 2)

enemies = { # 3 23
    'A' : Person('A', 100, 5, 3, 3, batch = scenes["enemies"]),
    'B' : Person('B', 100, 5, 15, 24, batch = scenes["enemies"]),
    'C' : Person('C', 100, 5, 18, 26, batch = scenes["enemies"]),
    'D' : Person('D', 100, 5, 29, 10, batch = scenes["enemies"]),
    'E' : Person('E', 100, 5, 29, 15, batch = scenes["enemies"]),
    'F' : Person('F', 100, 5, 29, 20, batch = scenes["enemies"]),
    'G' : Person('G', 100, 5, 46, 13, batch = scenes["enemies"]),
    'H' : Person('G', 100, 5, 47, 22, batch = scenes["enemies"])
}
