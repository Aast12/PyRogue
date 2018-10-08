import pyglet

pyglet.font.add_directory('resources/fonts')
pyglet.font.load('Source Code Pro Light')

dungeon_image = pyglet.image.load('resources/world.png')
dungeon_grid = pyglet.image.ImageGrid(dungeon_image, 3, 3, item_width = 16, item_height = 16)
dungeon_texture = pyglet.image.TextureGrid(dungeon_grid)

entities_image = pyglet.image.load('resources/entities.png')
entities_grid = pyglet.image.ImageGrid(entities_image, 3, 3, item_width = 16, item_height = 16)
entities_texture = pyglet.image.TextureGrid(entities_grid)

stairs = pyglet.image.load('resources/stairs.png')
