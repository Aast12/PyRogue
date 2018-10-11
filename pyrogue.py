from random import randint

import pyglet

from source.settings import SETTINGS, player, enemies, Tile, TEXTURES, scenes
from source.dungeons import dungeon
import source.resources as res

#   Utility Functions
def map_x(x):
    return x * (16) + 32

def map_y(y):
    return SETTINGS['Height'] - 16 * (y + 1) - 16

def convert_index(c, f):
    return len(dungeon[0]) * f + c

def check_exist(x, y):
    if not zone[convert_index(x, y)]:
        return False
    if x < 0 or y < 0:
        return False
    if x >= len(dungeon[0]) or y >= len(dungeon):
        return False
    return True

enemy_movs = [(0,1), (0,-1), (1,0), (-1,0)]

def enemyMove(index):
    mov = randint(0, 3)
    newX = enemies[index].x + enemy_movs[mov][0]
    newY = enemies[index].y + enemy_movs[mov][1]
    newIndex = convert_index(newX, newY)
    if check_exist(newX, newY) and zone[newIndex].char != '|' and zone[newIndex].char != '-' and zone[newIndex].char != '+':
        if newX == player.x and newY == player.y:
            dmg = randint(1, enemies[index].atk)
            player.hp -= dmg
            print("You received", dmg, "points of damage")
            return enemies[index].x, enemies[index].y
        return newX, newY
    else:
        return enemies[index].x, enemies[index].y

def makeDamage(index):
    dmg = randint(1, player.atk)
    enemies[index].hp -= dmg
    print("You made", dmg, "points of damage to", enemies[index].char)
    if enemies[index].hp <= 0:
        enemies[index].alive = False
        enemies[index].set_visible(False)
        print("You killed", enemies[index].char)

def game_over():
    pyglet.app.exit()

def visit(x, y):
    if(check_exist(x, y)):
        zone[convert_index(x, y)].visited = True
        zone[convert_index(x, y)].set_visible(True)

window = pyglet.window.Window(SETTINGS['Width'], SETTINGS['Height'], visible = False)
window.set_location(50, 50)

#-------------------------------------------------------------------------------------------------
#   Main Menu
#-------------------------------------------------------------------------------------------------
menu_items = {
    'Title' : pyglet.text.Label(SETTINGS['Title'],
                                font_name = SETTINGS['Font'],
                                font_size = 150,
                                x = 450, y = 550,
                                anchor_x='center', anchor_y='center',
                                color = (255, 255, 255, 255),
                                batch = scenes["menu_batch"]),
    'New Game' : pyglet.text.Label("New Game",
                                font_name = SETTINGS['Font'],
                                font_size = 40,
                                x = 235, y = 250,
                                anchor_x='center', anchor_y='center',
                                color = (255, 255, 255, 100),
                                batch = scenes["menu_batch"]),
    'Load Game' : pyglet.text.Label("Load Game",
                                font_name = SETTINGS['Font'],
                                font_size = 40,
                                x = 250, y = 150,
                                anchor_x='center', anchor_y='center',
                                color = (255, 255, 255, 100),
                                batch = scenes["menu_batch"]),
    'active_index' : 'New Game'
}


def menu_on_draw():
    window.clear()
    if menu_items['active_index'] == 'New Game':
            menu_items['New Game'].color = (255, 255, 255, 255)
            menu_items['Load Game'].color = (255, 255, 255, 100)
    else:
        menu_items['Load Game'].color = (255, 255, 255, 255)
        menu_items['New Game'].color = (255, 255, 255, 100)
    scenes['menu_batch'].draw()

def menu_on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.DOWN and menu_items['active_index'] == 'New Game':
        menu_items['active_index'] = 'Load Game'
    elif symbol == pyglet.window.key.UP and menu_items['active_index'] == 'Load Game':
        menu_items['active_index'] = 'New Game'

def menu_on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.ENTER:
        if menu_items['active_index'] == 'New Game':
            #input_name()
            new_game()
        else:
            print("under maintenance")

def begin_main_menu():
    window.set_visible()
    window.push_handlers(on_key_press = menu_on_key_press,
                        on_key_release = menu_on_key_release,
                        on_draw = menu_on_draw)

#-------------------------------------------------------------------------------------------------
#   Game
#-------------------------------------------------------------------------------------------------

player.sprite = pyglet.sprite.Sprite(TEXTURES['@'], map_x(2), map_y(2))

ui_items = {
    'Name Label' : pyglet.text.Label(player.name,
                                font_name = SETTINGS['Font'],
                                font_size = 30,
                                x = 16, y = map_y(len(dungeon)) - 40,
                                anchor_x='left', anchor_y='baseline',
                                color = (255, 255, 255, 255),
                                batch = scenes["game_batch"]),
    'HP' : pyglet.text.Label("HP:",
                                font_name = SETTINGS['Font'],
                                font_size = 30,
                                x = 16, y = map_y(len(dungeon)) - 80,
                                anchor_x='left', anchor_y='baseline',
                                color = (255, 255, 255, 255),
                                batch = scenes["game_batch"]),
    'HP Counter' : pyglet.text.Label(str(player.hp) + " % ",
                                font_name = SETTINGS['Font'],
                                font_size = 30,
                                x = 250, y = map_y(len(dungeon)) - 80,
                                anchor_x='right', anchor_y='baseline',
                                color = (255, 255, 255, 255),
                                batch = scenes["game_batch"])
}
#zone Wrapper
dr = [map_x(len(dungeon[0])), map_y(len(dungeon))]
dl = [16, map_y(len(dungeon))]
ur = [map_x(len(dungeon[0])), map_y(0) + 16]
ul = [16, map_y(0) + 16]
vertex_list = pyglet.graphics.vertex_list_indexed(8,
[0, 3, 4, 3, 4, 7, 3, 7, 2, 2, 7, 6, 2, 6, 5, 5, 2, 1, 5, 1, 0, 0, 4, 5],
('v2i', (dl[0], dl[1],               #0
         dr[0], dr[1],               #1
         ur[0], ur[1],               #2
         ul[0], ul[1],               #3
         dl[0] + 4, dl[1] + 4,       #4
         dr[0] - 4, dr[1] + 4,       #5
         ur[0] - 4, ur[1] - 4,       #6
         ul[0] + 4, ul[1] - 4,       #7
         )))

zone = []

def generateMap():
    for i in range(len(dungeon)):
        for j in range(len(dungeon[i])):
            tile = None
            char = dungeon[i][j]
            if char != " ":
                tile = Tile(char, map_x(j), map_y(i), scenes["game_batch"])
            zone.append(tile)

    for i in enemies.keys():
        #enemies[i].sprite =  pyglet.sprite.Sprite(TEXTURES[i], map_x(enemies[i].x), map_y(enemies[i].y), batch = scenes["enemies"])
        enemies[i].set_visible(False)

generateMap()

def update():
    #player.sprite.x = map_x(player.x)
    #player.sprite.y = map_y(player.y)
    player.update()
    tx = player.x
    ty = player.y
    visit(tx, ty)
    visit(tx, ty - 1)
    visit(tx, ty + 1)
    visit(tx - 1, ty)
    visit(tx - 1, ty - 1)
    visit(tx - 1, ty + 1)
    visit(tx + 1, ty)
    visit(tx + 1, ty - 1)
    visit(tx + 1, ty + 1)
    if player.hp < 0:
        player.hp = 0
        game_over()
    if(player.hp < 25):
        ui_items['HP Counter'].color  = (255, 0, 0, 255)
    ui_items['HP Counter'].text = str(player.hp) + " % "
    for i in enemies.keys():
        if enemies[i].alive:
            enemies[i].x, enemies[i].y = enemyMove(i)
            enemies[i].update()
            #enemies[i].sprite.x = map_x(enemies[i].x)
            #enemies[i].sprite.y = map_y(enemies[i].y)
            if zone[convert_index(enemies[i].x, enemies[i].y)].visited:
                enemies[i].set_visible(True)
            else:
                enemies[i].set_visible(False)

def game_on_draw():
    window.clear()
    scenes['game_batch'].draw()
    player.sprite.draw()
    scenes['enemies'].draw()
    #HP Bar
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 0, 2, 3],
    ('v2i', (250, map_y(len(dungeon)) - 80,                                               #DOWN-LEFT
             max(0, 250 + 500 - 5 * (100 - player.hp)), map_y(len(dungeon)) - 80,      #DOWN rIGHT
             max(0, 250 + 500 - 5 * (100 - player.hp)), map_y(len(dungeon)) - 50,      #UP RIGHT
             250, map_y(len(dungeon)) - 50)))                                             #UP LEFT
    vertex_list.draw(pyglet.gl.GL_TRIANGLES)

def game_on_key_press(symbol, modifiers):
    pass

def game_on_key_release(symbol, modifiers):
    newY = player.y
    newX = player.x
    x_mov = 0
    if symbol == pyglet.window.key.UP:
        newY -= 1
    elif symbol == pyglet.window.key.RIGHT:
        newX += 1
    elif symbol == pyglet.window.key.DOWN:
        newY += 1
    elif symbol == pyglet.window.key.LEFT:
        newX -= 1
    newIndex = convert_index(newX, newY)
    if check_exist(newX, newY) and zone[newIndex].char != '|' and zone[newIndex].char != '-':
        if zone[newIndex].char == '+':
            if not zone[newIndex].opened:
                zone[newIndex].opened = True
                zone[newIndex].set_texture(TEXTURES['*'])
            else:
                player.x = newX
                player.y = newY
        else:
            for i in enemies.keys():
                if newX == enemies[i].x and newY == enemies[i].y:
                    makeDamage(i)
                    if enemies[i].alive:
                        newX = player.x
                        newY = player.y
            player.x = newX
            player.y = newY
        update()

def input_name():
    window.pop_handlers()
    window.push_handlers(on_key_press = game_on_key_press,
                        on_key_release = game_on_key_release,
                        on_draw = game_on_draw)

def new_game():
    window.pop_handlers()
    window.push_handlers(on_key_press = game_on_key_press,
                        on_key_release = game_on_key_release,
                        on_draw = game_on_draw)

begin_main_menu()

pyglet.app.run()
