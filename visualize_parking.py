from time import sleep
from itertools import cycle
import string
import numpy as np
import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN
from pygame.color import THECOLORS
from parking_lot_search import *

other_cars = string.ascii_uppercase

def surface_show(array_img, name=""):
    "Show an array on the screen surface"
    screen = pg.display.set_mode(array_img.shape[:2], 0, 32)
    pg.surfarray.blit_array(screen, array_img)
    pg.display.flip()
    pg.display.set_caption(name)

def wait_for_click():
    '''Wait for either mousebutton click or keypress to go one,
    or quitting signal to exit'''
    while True:
        e = pg.event.wait().type
        if  e == MOUSEBUTTONDOWN or e == KEYDOWN:
            break
        elif e == pg.QUIT:
            import sys
            sys.exit()

def color(name):
    "Return RGB values corresponding to color name"
    return pg.Color(name)[:3]

# Nicer colors than using the first few in THECOLORS
replacement_colors=('yellow', 'magenta', 'cyan', 'orange', 'blue', 'lightblue', 'maroon', 'purple', 'plum', 'coral', 'grey')

def car_paint_shop(star='red', wall='black', goal='green', others=THECOLORS):
    "Return a dictionary holding colors for each car (incl. walls and goal)"
    others = cycle(others)
    p = {}
    for car in other_cars:
        p[car] = color(next(others))

    p['*'] = color(star)
    p['|'] = color(wall)
    p['@'] = color(goal)
    return p

def init_grid(init_color='white', N=N, debug=False):
    "Create the N*N grid"
    grid = np.zeros((N, N, 3), np.int32)
    grid[:]   = color(init_color)
    if debug:
        grid[::2] -= color('blue')
        grid[:, ::2] -= color('red')
    return grid

def scaleup(grid, factor=2):
    "Upscale the grid by factor"
    for _ in xrange(1, factor):
        W = len(grid)
        L = len(grid[0])
        double = np.zeros((2*W, 2*L, 3), np.int32)
        double[ ::2,  ::2] = grid
        double[1::2,  ::2] = grid
        double[ :  , 1::2] = double[:, ::2]
        grid = double
    return grid

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]

def make_array(puzzle, factor=6):
    "Turn given puzzle state into a scaled array"
    g = init_grid()
    c = car_paint_shop(others=replacement_colors)

    for (name, box) in puzzle:
        for b in box:
            g[b%N][b/N] = c[name]

    s = scaleup(g, factor)
    return s

def make_surf(puzzle, factor=6):
    "Create the array from puzzle, and show it"
    surface_show(make_array(puzzle, factor=factor), "Parking Blocks")

def parking_blocks(result, interactive=False, delay=0.5):
    '''Loop over states in result and show it
    interactive=True lets you click to go to the next state
    Otherwise the given delay is slept between states'''
    for item in path_states(result):
        make_surf(item)
        if interactive:
            wait_for_click()
        else:
            sleep(delay)
    wait_for_click()

parking_blocks(solve_parking_puzzle(puzzle1))