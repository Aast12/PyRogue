import pyglet
from random import randint

from source.settings import SETTINGS, player, Tiles, enemies
from source.dungeons import dungeon
import source.resources as res

#   Utility Functions
def X(x):
    return x * (16) + 32

def Y(y):
    return SETTINGS['Height'] - 16 * (y + 1) - 16

def convertIndex(c, f):
    return len(dungeon[0]) * f + c

def checkExist(x, y):
    if not Map[convertIndex(x, y)]:
        return False
    if x < 0 or y < 0:
        return False
    if x >= len(dungeon[0]) or y >= len(dungeon):
        return False
    return True

enemyMovs = [(0,1), (0,-1), (1,0), (-1,0)]

def enemyMove(index):
    mov = randint(0, 3)
    newX = enemies[index]['X'] + enemyMovs[mov][0]
    newY = enemies[index]['Y'] + enemyMovs[mov][1]
    newIndex = convertIndex(newX, newY)
    if checkExist(newX, newY) and Map[newIndex]['Char'] != '|' and Map[newIndex]['Char'] != '-' and Map[newIndex]['Char'] != '+':
        if newX == player['X'] and newY == player['Y']:
            dmg = randint(1, enemies[index]['Atk'])
            player['HP'] -= dmg
            print("You received", dmg, "points of damage")
            return enemies[index]['X'], enemies[index]['Y']
        return newX, newY
    else:
        return enemies[index]['X'], enemies[index]['Y']

def makeDamage(index):
    dmg = randint(1, player['Atk'])
    enemies[index]['HP'] -= dmg
    print("You made", dmg, "points of damage to", enemies[index]['Char'])
    if enemies[index]['HP'] <= 0:
        enemies[index]['Alive'] = False
        enemies[index]['Sprite'].visible = False
        print("You killed", enemies[index]['Char'])

def game_over():
    pyglet.app.exit()

def visit(x, y):
    if(checkExist(x, y)):
        Map[convertIndex(x, y)]['Visited'] = True
        Map[convertIndex(x, y)]['Sprite'].visible = True

window = pyglet.window.Window(SETTINGS['Width'], SETTINGS['Height'], visible = False)
window.set_location(50, 50)
scenes = {
    'menu_batch' : pyglet.graphics.Batch(),
    'game_batch' : pyglet.graphics.Batch(),
    'enemies' : pyglet.graphics.Batch(),
    'gameover_batch' : pyglet.graphics.Batch()
}
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

player['Sprite'] = pyglet.sprite.Sprite(player['Texture'], X(2), Y(2))

ui_items = {
    'Name Label' : pyglet.text.Label(player['Name'],
                                font_name = SETTINGS['Font'],
                                font_size = 30,
                                x = 16, y = Y(len(dungeon)) - 40,
                                anchor_x='left', anchor_y='baseline',
                                color = (255, 255, 255, 255),
                                batch = scenes["game_batch"]),
    'HP' : pyglet.text.Label("HP:",
                                font_name = SETTINGS['Font'],
                                font_size = 30,
                                x = 16, y = Y(len(dungeon)) - 80,
                                anchor_x='left', anchor_y='baseline',
                                color = (255, 255, 255, 255),
                                batch = scenes["game_batch"]),
    'HP Counter' : pyglet.text.Label(str(player['HP']) + " % ",
                                font_name = SETTINGS['Font'],
                                font_size = 30,
                                x = 250, y = Y(len(dungeon)) - 80,
                                anchor_x='right', anchor_y='baseline',
                                color = (255, 255, 255, 255),
                                batch = scenes["game_batch"])
}
#Map Wrapper
dr = [X(len(dungeon[0])), Y(len(dungeon))]
dl = [16, Y(len(dungeon))]
ur = [X(len(dungeon[0])), Y(0) + 16]
ul = [16, Y(0) + 16]
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

Map = []

def generateMap():
    for i in range(len(dungeon)):
        for j in range(len(dungeon[i])):
            tile = None
            aux = dungeon[i][j]
            if aux != " ":
                tile = Tiles[aux].copy()
                tile['Sprite'] = pyglet.sprite.Sprite(tile['Texture'], X(j), Y(i), batch = scenes["game_batch"])
                tile['Sprite'].visible = False
            Map.append(tile)

    for i in enemies.keys():
        enemies[i]['Sprite'] =  pyglet.sprite.Sprite(enemies[i]['Texture'], X(enemies[i]['X']), Y(enemies[i]['Y']), batch = scenes["enemies"])
        enemies[i]['Sprite'].visible = False

generateMap()

def update():
    player['Sprite'].x = X(player['X'])
    player['Sprite'].y = Y(player['Y'])
    tx = player['X']
    ty = player['Y']
    visit(tx, ty)
    visit(tx, ty - 1)
    visit(tx, ty + 1)
    visit(tx - 1, ty)
    visit(tx - 1, ty - 1)
    visit(tx - 1, ty + 1)
    visit(tx + 1, ty)
    visit(tx + 1, ty - 1)
    visit(tx + 1, ty + 1)
    if player['HP'] < 0:
        player['HP'] = 0
        game_over()
    if(player['HP'] < 25):
        ui_items['HP Counter'].color  = (255, 0, 0, 255)
    ui_items['HP Counter'].text = str(player['HP']) + " % "
    for i in enemies.keys():
        if enemies[i]['Alive']:
            enemies[i]['X'], enemies[i]['Y'] = enemyMove(i)
            enemies[i]['Sprite'].x = X(enemies[i]['X'])
            enemies[i]['Sprite'].y = Y(enemies[i]['Y'])
            if Map[convertIndex(enemies[i]['X'], enemies[i]['Y'])]['Visited']:
                enemies[i]['Sprite'].visible = True
            else:
                enemies[i]['Sprite'].visible = False

def game_on_draw():
    window.clear()
    scenes['game_batch'].draw()
    player['Sprite'].draw()
    scenes['enemies'].draw()
    #HP Bar
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
    [0, 1, 2, 0, 2, 3],
    ('v2i', (250, Y(len(dungeon)) - 80,                                               #DOWN-LEFT
             max(0, 250 + 500 - 5 * (100 - player['HP'])), Y(len(dungeon)) - 80,      #DOWN rIGHT
             max(0, 250 + 500 - 5 * (100 - player['HP'])), Y(len(dungeon)) - 50,      #UP RIGHT
             250, Y(len(dungeon)) - 50)))                                             #UP LEFT
    vertex_list.draw(pyglet.gl.GL_TRIANGLES)

def game_on_key_press(symbol, modifiers):
    pass

def game_on_key_release(symbol, modifiers):
    newY = player['Y']
    newX = player['X']
    x_mov = 0
    if symbol == pyglet.window.key.UP:
        newY -= 1
    elif symbol == pyglet.window.key.RIGHT:
        newX += 1
    elif symbol == pyglet.window.key.DOWN:
        newY += 1
    elif symbol == pyglet.window.key.LEFT:
        newX -= 1
    newIndex = convertIndex(newX, newY)
    if checkExist(newX, newY) and Map[newIndex]['Char'] != '|' and Map[newIndex]['Char'] != '-':
        if Map[newIndex]['Char'] == '+':
            if not Map[newIndex]['Opened']:
                Map[newIndex]['Opened'] = True
                Map[newIndex]['Texture'] = res.dungeon_texture[4]
                Map[newIndex]['Sprite'] = pyglet.sprite.Sprite(res.dungeon_texture[4], X(newX), Y(newY), batch = scenes['game_batch'])
            else:
                player['X'] = newX
                player['Y'] = newY
        else:
            for i in enemies.keys():
                if newX == enemies[i]['X'] and newY == enemies[i]['Y']:
                    makeDamage(i)
                    if enemies[i]['Alive']:
                        newX = player['X']
                        newY = player['Y']
            player['X'] = newX
            player['Y'] = newY
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
