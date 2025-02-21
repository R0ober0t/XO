"""
1. Create grid
2. Detect row and column
3. Update state lists
4. Check state game
5. Prevent overwritting
6. Draw X and 0
7. Crossline
"""

# inports
import pyglet
from screeninfo import get_monitors

# constants
SCREEN_WIDTH, SCREEN_HEIGHT = get_monitors()[0].width, get_monitors()[0].height
WINDOW_SIZE = 1200
SQUARE_SIZE = WINDOW_SIZE/3
SCREEN_X_LOCATION = SCREEN_WIDTH / 2 - WINDOW_SIZE / 4
SCREEN_Y_LOCATION = SCREEN_HEIGHT / 2 - WINDOW_SIZE / 4
COLOR, THICKNESS = (255, 0, 0), 30

# assets
x_image = pyglet.image.load('assets/x.png')
o_image = pyglet.image.load('assets/o.png')

# grid object
grid = pyglet.window.Window(WINDOW_SIZE,WINDOW_SIZE)
grid.set_location(SCREEN_X_LOCATION,SCREEN_Y_LOCATION)

# variables
sprites = []
turn = "X"
visited = [0]*9
game_over = False
rows = [0]*3
columns = [0]*3
diagonals = [0]*2
winner = None

# functions
def draw_grid():
    pyglet.shapes.Line(0,WINDOW_SIZE/3,WINDOW_SIZE,WINDOW_SIZE/3, THICKNESS,COLOR).draw()
    pyglet.shapes.Line(0,(WINDOW_SIZE/3)*2,WINDOW_SIZE,(WINDOW_SIZE/3)*2, THICKNESS,COLOR).draw()
    pyglet.shapes.Line(WINDOW_SIZE/3,0,WINDOW_SIZE/3,WINDOW_SIZE, THICKNESS,COLOR).draw()
    pyglet.shapes.Line((WINDOW_SIZE/3)*2,0,(WINDOW_SIZE/3)*2,WINDOW_SIZE, THICKNESS,COLOR).draw()

def add_sprite(row, column):
    global turn
    sprite_width = SQUARE_SIZE*0.75
    sprite_height = SQUARE_SIZE*0.75

    sprite_x = SQUARE_SIZE/2+SQUARE_SIZE*row - sprite_width/2
    sprite_y = SQUARE_SIZE/2+SQUARE_SIZE*column - sprite_height/2

    image = x_image if turn == "X" else o_image
    turn = "O" if turn == "X" else "X"
    
    sprite = pyglet.sprite.Sprite(image, sprite_x, sprite_y)
    
    sprite.scale_x = sprite_width / image.width
    sprite.scale_y = sprite_height / image.height

    sprites.append(sprite)

def cross_line(row=None, column=None, diagonal=None):
    if row is not None:
        pyglet.shapes.Line(SQUARE_SIZE/2+SQUARE_SIZE*row, 0, SQUARE_SIZE/2+SQUARE_SIZE*row, WINDOW_SIZE, THICKNESS, COLOR).draw()
    if column is not None:
        pyglet.shapes.Line(0, SQUARE_SIZE/2+SQUARE_SIZE*column, WINDOW_SIZE, SQUARE_SIZE/2+SQUARE_SIZE*column, THICKNESS, COLOR).draw()
    if diagonal is not None:
        pyglet.shapes.Line(0, WINDOW_SIZE, WINDOW_SIZE, 0, THICKNESS, COLOR).draw()
        
# events
@grid.event()
def on_mouse_press(x,y,_,__):
    global turn, game_over, winner, rows, columns, diagonals
    row = y//(WINDOW_SIZE//3)
    column = x//(WINDOW_SIZE//3)
    if visited[row*3+column] == 0 and game_over == False:
        add_sprite(column, row)
        visited[row*3+column] = 1
        point = 1 if turn == "X" else -1
        rows[row] += point
        columns[column] += point
        if row == column:
            diagonals[0] += point
        if row+column == 2:
            diagonals[1] += point

        if abs(rows[row]) == 3:
            cross_line(row=row)
            game_over = True
            print("game over")
            winner = turn
        if abs(columns[column]) == 3:
            cross_line(column=column)
            game_over = True
            print("game over")
            winner = turn
        if abs(diagonals[0]) == 3 or abs(diagonals[1]) == 3:
            cross_line(column=column)
            game_over = True
            print("game over")
            winner = turn
        
@grid.event
def on_draw():
    grid.clear()
    draw_grid()
    for sprite in sprites:
        sprite.draw()

# run
pyglet.app.run()