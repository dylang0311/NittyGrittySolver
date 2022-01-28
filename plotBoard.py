import matplotlib.pyplot as plt
import random


# char_to_color takes as inputs 'a', 'b', 'c', or 'e', and returns the RGB values for purple, white, orange,
# and black, respectively.
def char_to_color(c):
    if c == 'a':
        return [153, 0, 153]
    if c == 'b':
        return [224, 224, 224]
    if c == 'c':
        return [255, 153, 51]
    if c == 'e':
        return [1, 1, 1]


# lin_to_sub_colors takes as input the linear index of a location on a Tile object and returns the
# associated subscripts.
def lin_to_sub_colors(n):
    if n == 0:
        return [0, 1]
    if n == 1:
        return [0, 0]
    if n == 2:
        return [1, 0]
    if n == 3:
        return [1, 1]


# rot_t rotates the Tile object t counterclockwise a total of r times.
def rot_t(t, r):
    tr = Tile('z', 'z', 'z', 'z', -1, -1)
    tr.r = t.r
    tr.n = t.n
    if r == 1:
        tr.c = [t.c[i] for i in [1, 2, 3, 0]]
    elif r == 2:
        tr.c = [t.c[i] for i in [2, 3, 0, 1]]
    elif r == 3:
        tr.c = [t.c[i] for i in [3, 0, 1, 2]]
    else:
        tr.c = [t.c[i] for i in range(4)]
    return tr


# get_colors_board returns the colors or character values for each pixel on a Board object b.
def get_colors_board(b, char_or_color):
    colors = [[0 for ii in range(10)] for jj in range(10)]
    for ii in range(5):
        for jj in range(5):
            for kk in range(4):
                [m, n] = lin_to_sub_colors(kk)
                if char_or_color == 'color':
                    colors[2 * ii + m][2 * jj + n] = char_to_color(b[ii][jj].c[kk])
                else:
                    colors[2 * ii + m][2 * jj + n] = b[ii][jj].c[kk]
    return colors


# plt_b creates an RGB image of a list of Tile objects b_list. doplot determines if the image is shown, and timestep
# determines how many black squares to append to the end of the board. timestep should be set to 24 for a complete
# board.
def plt_b(b_list, doplot, timestep):
    for j in range(24 - timestep):
        b_list.append([-1, 0])
    board = Board([b_list[p][0] for p in range(25)], [b_list[p][1] for p in range(25)])
    colors = get_colors_board(board, 'color')
    fig = plt.figure()
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.imshow(colors)
    plt.axvline(x=1.5, color='k')
    plt.axvline(x=3.5, color='k')
    plt.axvline(x=5.5, color='k')
    plt.axvline(x=7.5, color='k')
    plt.axhline(y=1.5, color='k')
    plt.axhline(y=3.5, color='k')
    plt.axhline(y=5.5, color='k')
    plt.axhline(y=7.5, color='k')
    if doplot == 1:
        plt.show()
    return fig


# The Tile class consists of four colors (t1,t2,t3,t4) represented as char types, an int between 0 and 3 inclusive
# for the rotation of the tile, and an ID number.
class Tile:
    def __init__(self, t1, t2, t3, t4, rots, ID):
        self.c = t1 + t2 + t3 + t4
        self.r = rots
        self.n = ID


# The Board class consists of attribute b which holds instances of the Tile class and attribute tID which is a list
# of all tile IDs present in b
class Board:
    def __init__(self, tileid, rots):
        self.b = [[rot_t(T[tileid[5 * i + j]], rots[5 * i + j]) for j in range(5)] for i in range(5)]
        self.tID = tileid

    def __getitem__(self, key):
        return self.b[key]

    def __setitem__(self, key, newvalue):
        self.b[key] = newvalue


# T is a list of all unique (up to rotation) Tile instances.
T = [Tile('c', 'a', 'c', 'a', 1, 0), Tile('c', 'c', 'a', 'c', 3, 1), Tile('c', 'c', 'c', 'b', 3, 2),
     Tile('a', 'c', 'c', 'b', 3, 3), Tile('b', 'a', 'b', 'c', 3, 4), Tile('a', 'c', 'b', 'b', 3, 5),
     Tile('c', 'a', 'b', 'c', 3, 6), Tile('c', 'c', 'c', 'c', 0, 7), Tile('b', 'c', 'b', 'c', 1, 8),
     Tile('b', 'b', 'c', 'a', 3, 9), Tile('b', 'b', 'b', 'b', 0, 10), Tile('c', 'b', 'b', 'b', 3, 11),
     Tile('c', 'b', 'b', 'c', 3, 12), Tile('a', 'c', 'c', 'a', 3, 13), Tile('b', 'b', 'a', 'b', 3, 14),
     Tile('b', 'c', 'a', 'c', 3, 15), Tile('b', 'a', 'a', 'c', 3, 16), Tile('b', 'b', 'a', 'a', 3, 17),
     Tile('a', 'c', 'a', 'b', 3, 18), Tile('a', 'a', 'b', 'c', 3, 19), Tile('a', 'a', 'c', 'a', 3, 20),
     Tile('a', 'a', 'a', 'a', 0, 21), Tile('a', 'a', 'a', 'b', 3, 22), Tile('b', 'a', 'b', 'a', 1, 23),
     Tile('e', 'e', 'e', 'e', 0, -1)]


# The following code selects a random found solution and plots it.
solutionFile = open('NittyGrittySolutionFiles/tID' + str(random.randrange(0, 13)) + 'solutions.txt')
solutionLines = solutionFile.readlines()
solutionChosen = list(eval(solutionLines[random.randrange(0, len(solutionLines))]))
plt_b(solutionChosen, 1, 24)
