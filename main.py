import numpy as np
import copy
import pickle


# rot_t: Input Tile instance t and int r, output Tile instance tr. Rotates tile t counterclockwise r times.
# r should be an int between 0 and 3.
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


# off_board_tiles: Input list b and int timestep, output list off_board. off_board is the list of tile IDs not in b.
def off_board_tiles(b, timestep):
    off_board = []
    tid = [b[ii][0] for ii in range(timestep)]
    for ii in range(24):
        if ii not in tid:
            off_board.append(ii)
    return off_board


# check_new_tile: Input list b, int m, and int tstep, ourput boolean value. This function checks to see if the
# addition of the tile at b[tstep] is valid. Returns 1 if yes, 0 if no.
def check_new_tile(b, m, tstep):
    [new_tileid, new_rots] = b[tstep]
    [ii, jj] = m
    new_tile = rot_t(T[new_tileid], new_rots)
    if ii == 0 or (ii == 3 and jj == 2):
        [last_tileid, last_rots] = b[tstep-1]
        last_tile = rot_t(T[last_tileid], last_rots)
        if new_tile.c[1] != last_tile.c[0] or new_tile.c[2] != last_tile.c[3]:
            return 0
    elif jj == 0 or (ii == 2 and jj == 3):
        [up_tileid, up_rots] = b[tstep-5]
        up_tile = rot_t(T[up_tileid], up_rots)
        if new_tile.c[1] != up_tile.c[2] or new_tile.c[0] != up_tile.c[3]:
            return 0
    else:
        [last_tileid, last_rots] = b[tstep - 1]
        last_tile = rot_t(T[last_tileid], last_rots)
        [up_tileid, up_rots] = b[tstep - 5]
        up_tile = rot_t(T[up_tileid], up_rots)
        if (new_tile.c[1] != last_tile.c[0] or new_tile.c[2] != last_tile.c[3] or
                new_tile.c[1] != up_tile.c[2] or new_tile.c[0] != up_tile.c[3]):
            return 0
    return 1


# Performs an update of chain instance c by taking every list of tiles and checking every possible tile that could
# be appended to each list.
def update_chain(c):
    prev_elements = copy.deepcopy(c.elements)
    c.timestep += 1
    timestep_accountblack = copy.deepcopy(c.timestep)
    if c.timestep >= 12:
        timestep_accountblack += 1
    m = [0, 0]
    m[0] = int(np.floor(timestep_accountblack / 5))
    m[1] = timestep_accountblack % 5
    c.elements = []
    num_seg_in_chain = 0
    for ii in range(len(prev_elements)):
        offboard = off_board_tiles(prev_elements[ii], timestep_accountblack)
        for jj in range(24 - c.timestep):
            next_tile_unrot = T[offboard[jj]]
            for k in range(next_tile_unrot.r + 1):
                next_board_list = copy.deepcopy(prev_elements[ii])
                next_board_list.append((next_tile_unrot.n, k))
                if check_new_tile(next_board_list, m, timestep_accountblack) == 1:
                    c.elements.append(copy.deepcopy(next_board_list))
                    num_seg_in_chain += 1
    print(c.timestep, ', ', num_seg_in_chain)
    return c


# The Tile class consists of four colors (t1,t2,t3,t4) represented as char types, an int between 0 and 3 inclusive
# for the rotation of the tile, and an ID number.
class Tile:
    def __init__(self, t1, t2, t3, t4, rots, ID):
        self.c = t1 + t2 + t3 + t4
        self.r = rots
        self.n = ID


# The Chain class has attributes elements, timestep, and black. elements is every list of valid board
# configurations made thus far, timestep is the current time step of the chain, and black indicates if the
# middle black tile has been included yet.
class Chain:
    def __init__(self, t_start):
        self.elements = [[t_start]]
        self.timestep = 0
        self.black = 0

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, newvalue):
        self.elements[key] = newvalue


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

# First entry is tileID, second is rotation; 14 total starting tiles to try
c_start = [(21, 0),
           (22, 0),
           (22, 1),
           (22, 2),
           (22, 3),
           (23, 0),
           (17, 0),
           (17, 1),
           (16, 0),
           (16, 1),
           (16, 2),
           (16, 3),
           (18, 0),
           (18, 1)]

# c_final records the final valid chain to be written to the save file.
c_final = []
total_time_steps = 24
numsolutions = 0
time_step_to_split = 10
num_subchain = 7
for j in range(14):
    not_first_step = 0
    print('Starting Chain ' + str(j + 1) + ' of 14')
    chain = Chain(c_start[j])
    for i in range(time_step_to_split):
        if len(chain.elements) != 0:
            if chain.timestep != 11 or chain.black == 1:
                chain = update_chain(chain)
            else:
                for k in range(len(chain.elements)):
                    chain.elements[k].append([-1, 0])
                chain.black = 1
    chain_length = len(chain.elements)
    # Once the timestep has reached time_step_to_split, the chain is divided into num_subchain different chains. Each
    # of these subchains is then evaluated serially. This is done to decrease demands on memory.
    for k in range(num_subchain):
        chain_subset = copy.deepcopy(chain)
        chain_subset.elements = chain_subset.elements[k*chain_length//num_subchain+not_first_step:
                                                      (k+1)*chain_length//num_subchain]
        with open("NittyGrittyChainStorage/subchain_storage" + str(k+1) + ".pickle", "wb") as handle:
            pickle.dump(chain_subset, handle, protocol=pickle.HIGHEST_PROTOCOL)
        not_first_step = 1
    del chain
    for k in range(num_subchain):
        print('Starting Subchain ' + str(k + 1) + ' of ' + str(num_subchain) + ' for Chain ' + str(j + 1))
        with open("NittyGrittyChainStorage/subchain_storage" + str(k + 1) + ".pickle", "rb") as handle:
            chain_subset = pickle.load(handle)
        for i in [time_step_to_split + ii for ii in range(total_time_steps - time_step_to_split)]:
            if len(chain_subset.elements) != 0:
                if chain_subset.timestep != 11 or chain_subset.black == 1:
                    chain_subset = update_chain(chain_subset)
                else:
                    for ell in range(len(chain_subset.elements)):
                        chain_subset.elements[ell].append([-1, 0])
                    chain_subset.black = 1
        if k == 0:
            chain = chain_subset
        else:
            for i in range(len(chain_subset.elements)):
                chain.elements.append(chain_subset.elements[i])
    if len(chain.elements) != 0:
        c_final.append(copy.deepcopy(chain))
    if len(c_final[j].elements) != 0:
        textfile = open("NittyGrittySolutionFiles/tID" + str(j) + "solutions.txt", "w")
        for i in range(len(c_final[j].elements)):
            numsolutions += 1
            textfile.write(str(c_final[j].elements[i]) + "\n")
        textfile.close()


