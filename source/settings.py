import source.resources as res


SETTINGS = {
    'Title' : 'PyRogue',
    'Font' : 'Source Code Pro Light',
    'Width' : 1400,
    'Height' : 680
}

player = {
    'Name' : 'ROGUE',
    'HP' : 100,
    'Atk': 35,
    'Texture' : res.entities_texture[6],
    'Sprite' : None,
    'X' : 2,
    'Y' : 2
}

Tiles = {
    '+' : {
        'Visited' : False,
        'Opened' : False,
        'Char' : '+',
        'Texture' : res.dungeon_texture[3],
        'Sprite' : None
        },
    '|' : {
        'Visited' : False,
        'Char' : '|',
        'Texture' : res.dungeon_texture[5],
        'Sprite' : None
        },
    '-' : {
        'Visited' : False,
        'Char' : '-',
        'Texture' : res.dungeon_texture[8],
        'Sprite' : None
        },
    '.' : {
        'Visited' : False,
        'Active' : False,
        'Char' : '.',
        'Texture' : res.dungeon_texture[6],
        'Sprite' : None
        },
    '#' : {
        'Visited' : False,
        'Char' : '#',
        'Texture' : res.dungeon_texture[7],
        'Sprite' : None
        },
    'S' : {
        'Visited' : False,
        'Char' : 'S',
        'Texture' : res.stairs,
        'Sprite' : None
        }
}
enemies = { # 3 23
    'A' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'A',
        'Texture' : res.entities_texture[7],
        'Sprite' : None,
        'X': 3,
        'Y': 3
        },
    'B' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'B',
        'Texture' : res.entities_texture[8],
        'Sprite' : None,
        'X': 15,
        'Y': 24
        },
    'C' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'C',
        'Texture' : res.entities_texture[3],
        'Sprite' : None,
        'X': 18,
        'Y': 26
        },
    'D' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'D',
        'Texture' : res.entities_texture[4],
        'Sprite' : None,
        'X': 29,
        'Y': 10
        },
    'E' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'E',
        'Texture' : res.entities_texture[5],
        'Sprite' : None,
        'X': 29,
        'Y': 15
        },
    'F' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'F',
        'Texture' : res.entities_texture[0],
        'Sprite' : None,
        'X': 29,
        'Y': 20
        },
    'G' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'G',
        'Texture' : res.entities_texture[1],
        'Sprite' : None,
        'X': 46,
        'Y': 13
        },
    'H' : {
        'HP' : 100,
        'Atk' : 5,
        'Alive' : True,
        'Char' : 'H',
        'Texture' : res.entities_texture[2],
        'Sprite' : None,
        'X': 47,
        'Y': 22
        },
}
