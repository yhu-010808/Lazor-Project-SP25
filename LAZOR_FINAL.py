import os
import random
import unittest
import copy


class Game:
    """
    Lazor Game class for reading and parsing the board configuration file.
    """

    import os

class Game:
    def __init__(self, filename: str):
        base_path = os.path.dirname(__file__)
        full_path = os.path.join(base_path, filename)

        try:
            with open(full_path, 'r') as f:
                self.raw_data = [line.strip() for line in f if '#' not in line and line.strip() != '']
        except FileNotFoundError:
            raise FileNotFoundError(f"Cannot find the file: {filename}. Check that it exists in the same folder.")


    def database(self):
        """
        Parses the input data into board grid, lazor paths, targets, and block counts.

        Returns:
        - self.grid: List[List[str]]
        - self.lazor_start: List[Tuple[int, int]]
        - self.lazor_path: List[Tuple[int, int]]
        - self.pointer: List[Tuple[int, int]]
        - self.blocks: Dict[str, int]
        """

        # Process grid
        grid_start = self.raw_data.index('GRID START') + 1
        grid_stop = self.raw_data.index('GRID STOP')
        self.grid = [list(line.replace(' ', '')) for line in self.raw_data[grid_start:grid_stop]]

        # Remove processed grid lines
        content = self.raw_data[:grid_start - 1] + self.raw_data[grid_stop + 1:]

        # Lazor paths
        self.lazor_start = []
        self.lazor_path = []

        for line in content:
            if line.startswith('L'):
                parts = list(map(int, line[1:].split()))
                if len(parts) == 4:
                    self.lazor_start.append(tuple(parts[:2]))
                    self.lazor_path.append(tuple(parts[2:]))
                else:
                    raise ValueError("Invalid Lazor format.")

        # Target points
        self.pointer = [
            tuple(map(int, line[1:].split()))
            for line in content if line.startswith('P')
        ]

        # Block types
        self.blocks = {'A': 0, 'B': 0, 'C': 0}
        for line in content:
            if line[0] in self.blocks:
                key, val = line.split()
                self.blocks[key] = int(val)

        return self.grid, self.lazor_start, self.lazor_path, self.pointer, self.blocks


class Board:
    """
    Board class generates indiviual arrangements of how the game can be played.
    """

    def sampler(self, grid):
        return self.get_placeable_positions()

    def sample_board(self, sample_space, blocks, grid):
        return self.place_blocks_randomly(sample_space, blocks)

    def make_board(self, grid):
        return self.create_meshgrid(grid)

    def __init__(self, grid, origin, path, sets):
        self.grid = grid
        self.origin = origin
        self.path = path
        self.sets = sets

    def get_placeable_positions(self):
        """
        Identify all positions on the board where a block can be placed ('o').

        Returns:
            list[tuple[int, int]]: List of coordinates available for block placement.
        """
        return [
            (i, j)
            for j, row in enumerate(self.grid)
            for i, cell in enumerate(row)
            if cell == 'o'
        ]

    def place_blocks_randomly(self, sample_space, block_dict, seed=None):
        """
        Randomly place blocks on a copy of the grid.

        Parameters:
            sample_space (list[tuple]): Coordinates available for placement.
            block_dict (dict): Dictionary of block counts, e.g., {'A': 2, 'B': 1, 'C': 1}.
            seed (int, optional): Random seed for reproducibility.

        Returns:
            list[list[str]]: A new grid with blocks placed.
        """
        if seed is not None:
            random.seed(seed)

        total_blocks = sum(block_dict.values())
        if total_blocks > len(sample_space):
            raise ValueError("Not enough space on the grid to place all blocks.")

        placement_positions = random.sample(sample_space, total_blocks)
        grid_copy = copy.deepcopy(self.grid)

        block_order = ['C', 'A', 'B']  # Place blocks in this order
        pos_index = 0


        for block_type in block_order:
            count = block_dict.get(block_type, 0)
            for _ in range(count):
                i, j = placement_positions[pos_index]
                grid_copy[j][i] = block_type
                pos_index += 1

        return grid_copy

    def create_meshgrid(self, grid):
        """
        Expand the grid to a fine mesh where laser paths can be traced.
        Converts an (i x j) grid to a (2i+1 x 2j+1) meshgrid.

        Parameters:
            grid (list[list[str]]): Grid with placed blocks.

        Returns:
            list[list[str]]: Fine meshgrid representation.
        """
        mesh_rows = 2 * len(grid) + 1
        mesh_cols = 2 * len(grid[0]) + 1
        meshgrid = [['o' for _ in range(mesh_cols)] for _ in range(mesh_rows)]

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                meshgrid[2*i + 1][2*j + 1] = grid[i][j]

        return meshgrid

    def generate_full_board(self, seed=None):
        """
        One-click method to generate a complete playable board with meshgrid.

        Returns:
            tuple: (grid_with_blocks, meshgrid)
        """
        positions = self.get_placeable_positions()
        placed_grid = self.place_blocks_randomly(positions, self.sets, seed)
        meshgrid = self.create_meshgrid(placed_grid)
        return placed_grid, meshgrid


class Blocks:
    """
    This class defines the 'reflect' and 'transmit' properties for each position in the game board.
    """

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def prop(self, meshgrid):
        '''
        This function specifies the 'reflect' and 'transmit' properties as booleans
        **Parameter**
            self.x: *int* - position row coordinate
            self.y: *int* - position column coordinate

        **Returns**
            self.reflect: *boolean* - whether the position reflects the laser
            self.transmit: *boolean* - whether the position allows laser to transmit through
        '''

        if meshgrid[self.y][self.x] == 'A':
            self.reflect = True
            self.transmit = False
        elif meshgrid[self.y][self.x] == 'B':
            self.reflect = False
            self.transmit = False
        elif meshgrid[self.y][self.x] == 'C':
            self.reflect = True
            self.transmit = True
        else:
            self.reflect = False
            self.transmit = True
        return self.reflect, self.transmit


class Laser:
    """
    The laser class stores the laser's starting point and orientation.
    It also includes capabilities that enable the laser beam to navigate the board
    and identify certain blocks.
    """

    def __init__(self, start_point, path):
        self.source = start_point
        self.direction = path

    def pos_chk(x, y, nBlocks):
        """
        To determine whether the coordinates are within the grid or not.

        **Parameters**

            x : *int*
                Denotes the x-coordinate
            y : *int*
                Denotes the y-coordinate
            nBlocks : *int*
                Denotes the length of the box.
        """
        return x >= 0 and x < nBlocks and y >= 0 and y < nBlocks

    def laser_strikes(self, path, intercepts, grid, meshgrid, path_1, intercept_new):
        """
        The function for predicting where a lazor beam will strike.
        This function analyzes each point of the laser beam.
        The algorithm will identify block neighbors, analyze their features, and conduct appropriate operations on them.

        **Parameters**
            path : *list, list, tuple*
                A nested list of tuples containing the direction of the lazor.
            intercepts : *list, list, tuple*
                A nested list of tuples containing the intercepts through which the lazor beam passes through.
            grid : *list,list,str*
                A nested list of strings that denotes the positioning of the blocks in the game. Subset of meshgrid
            meshgrid : *list,list,str*
                A nested list of strings derived from the grid, indicating all the positions of the blocks as well as the
                positions/points, through which the lazor can pass through.

        **Returns**
            path : *list,list,tuples*
                A nested list of tuples with all the directions at each intercept.
            intercepts : *list,list,tuples*
                A nested list of tuples with all the intercepts that the laser beam traversed through.
            path_1 : *list,tuples*
                A list of tuples indicating the directions after laser splits at the refract blocks.
            intercept_new : *list,tuples*
                A list of tuples indicating the intercepts that the laser parses through after being split.

        """

        (dx, dy) = path[-1]

        # The last position of the laser
        (nx, ny) = intercepts[-1]


        # Directions to perform a check
        n_direct = [(0, 1),(0, -1),(-1, 0),(1, 0)]


        # Creating a buffer to check the surrounding positions
        nlist = []
        transmit_list = []

        # Exploring the neighbours of the new point to modify directions

        if (dx,dy) != (0,0):

        #This will allow the loop to proceed only if there is a viable direction to proceed

            for i in range(len(n_direct)):

                ex = nx + n_direct[i][0]
                ey = ny + n_direct[i][1]

                if ex > 0 and ex < 2*len(grid[0])+1 and ey > 0 and ey < 2*len(grid)+1:
                    #Just to perform a check that we are still within the grid
                    delta_x = ex-nx
                    delta_y = ey-ny



                    if meshgrid[ey][ex] == 'A':

                        if delta_x == 0:
                            new_dx = dx * 1
                        else:
                            new_dx = dx * -1
                        if delta_y == 0:
                            new_dy = dy * 1
                        else:
                            new_dy = dy * -1
                        nlist.append((new_dx,new_dy))


                    elif Blocks(ex,ey).prop(meshgrid) == (False,False) :


                        if delta_x == dx or delta_y == dy:
                            new_dx = dx * 0
                            new_dy = dy * 0
                        else :
                            new_dx = dx * 1
                            new_dy = dy * 1
                        nlist.append((new_dx,new_dy))


                    elif Blocks(ex,ey).prop(meshgrid) == (True,True) :


                        if delta_x == dx or delta_y == dy:

                            if delta_x == 0:
                                new_dx = dx * 1
                            else:
                                new_dx = dx * -1
                            if delta_y == 0:
                                new_dy = dy * 1
                            else:
                                new_dy = dy * -1
                            old_dx = dx
                            old_dy = dy
                            transmit_list.append((old_dx,old_dy))
                            nlist.append((new_dx,new_dy))

                        else:

                            new_dx = dx * 1
                            new_dy = dy * 1
                            nlist.append((new_dx,new_dy))


            if len(nlist) > 0:

                path.append(nlist[-1])

            else :
                path.append((dx,dy))

            if len(transmit_list) > 0 :
                path_1.append(transmit_list[-1])
                intercept_new.append((nx,ny))

            nx += path[-1][0]
            ny += path[-1][1]

            intercepts.append((nx,ny))


        return path,intercepts, path_1, intercept_new


    def trajectory(self, path, grid, meshgrid):
        """
        This function invokes the laser_strikes function and then attempts to determine the trajectory,
        assuming the laser has feasible directions.

        **Parameters**

            path : *list, list, tuple*
                A nested list of tuples containing the direction of the lazor.
            grid : *list,list,str*
                A nested list of strings that denotes the positioning of the blocks in the game. Subset of meshgrid
            meshgrid : *list,list,str*
                A nested list of strings derived from the grid, indicating all the positions of the blocks as well as the
                positions/points, through which the lazor can pass through.

        **Returns**

            final_intercept_list : *list,tuples*
                A list of tuples containing the intercepts through which the laser/s pass/es. Doesn't include the intercepts
                cause by the laser after split.
            path : *list,tuples*
                A nested list of path for all the laser beams.
            intercept_new : *list,tuples*
                A list of tuples containing the intercepts through which the laser beam passes after being split at a refract block.
        """

        intercepts = []
        path = []

        for i in range(len(self.source)):
            intercepts.append([self.source[i]])
            path.append([self.direction[i]])


        n_direct = [(0, 1),(0, -1),(-1, 0),(1, 0)]

        path_1 = []
        intercept_new = []


        for k in range(len(path)) :

            # Perform an initial check at the input location to verify that if there is a block in the neighbour domain
            # of the origin source, the laser's direction changes immediately.

            if len(intercepts[k]) == 1:

                path[k], intercepts[k], path_1, intercept_new = self.laser_strikes(path[k], intercepts[k], grid, meshgrid, path_1, intercept_new)

            # To continue the loop till the laser reaches the boundary of the grid.

            while intercepts[k][-1][0] != 0 and intercepts[k][-1][0] < len(meshgrid[0])-1 and intercepts[k][
            -1][1] != 0 and intercepts[k][-1][1] < len(meshgrid)-1:


                if path[k][-1] != (0,0) :

                    path[k], intercepts[k], path_1, intercept_new = self.laser_strikes(path[k], intercepts[k], grid, meshgrid, path_1, intercept_new)

                else :

                    break

            # Check to see whether the Laser hits any refract blocks, as it will split on impact and take two courses later on.
            # The next 'if' conditional will allow you to explore an extra path using the laser's origin at the split point.
            # It uses the function laser_strikes to investigate the transmit path, given that the split interface is now the origin.

            if len(path_1) != 0:

                path_0 = []
                intercept_0 = []

                (dx,dy) = path_1[-1]
                (cx, cy) = intercept_new[-1]

                nx = cx + dx
                ny = cy + dy

                intercept_new.append((nx,ny))

                while intercept_new[-1][0] != 0 and intercept_new[-1][0] < len(meshgrid[0])-1 and intercept_new[
                -1][1] != 0 and intercept_new[-1][1] < len(meshgrid)-1:


                    if path_1[-1] != (0,0) :

                        path_1, intercept_new, path_0, intercept_0 = self.laser_strikes(path_1, intercept_new, grid, meshgrid, path_0, intercept_0)

                    else:
                        break

        final_intercept_list = []
        for sublist in intercepts:
            for item in sublist:
                final_intercept_list.append(item)

        return final_intercept_list, path, intercept_new


## Defining 2 global functions

def outputter(mesh):
    """
    The result of this function is packaged in an attractive, legible, and intuitive manner.
    It produces a file called "Solution.bff" that includes a grid that shows how the answer should appear.

    **Parameters**

        mesh : *list,list,tuples*
            A nested list of strings derived from the grid, indicating all the positions of the blocks as well as the
            positions/points, through which the lazor can pass through.

    **Returns**

        None

    **Output**

        solution.bff : *file*
            A .bff file that contains the solution to the input.
    """

    print("Analyzing and preparing files for output...")

    solution = []

    for j in range(1,len(mesh), 2):
        for i in range(1, len(mesh[0]), 2):
            solution.append(mesh[j][i])

    width = int((len(mesh[0])-1) * 0.5)

    solution = [solution[x:x+width] for x in range(0, len(solution), width)]

    file = open('solution.bff', 'w')

    for i in solution:
        for j in i:
            file.write(j)
            file.write('\t')
        file.write('\n')
    file.close()

    print("Solution found")


def solution_generator(game_file, max_iter):
    """
    This is a function aiming at generating the solution and running the entire program.

    **Parameters**
        game : *file*
            The input file which contains the lazor problem to be solved.
        maxiter : *int*
            the maximum number of steps of iteration that you want the program to go through.
            A suitable number is provided below. It breaks if it finds a solution, so the program doesn't run continuously
            for prolonged times.
    """

def solution_generator(game_file, max_iter):


  for i in range(max_iter):
      G = Game(game_file)
      G.database()

      B = Board(G.grid, G.lazor_start, G.lazor_path, G.blocks)

      sample_space = B.get_placeable_positions()
      placed_grid = B.place_blocks_randomly(sample_space, G.blocks)
      mesh = B.create_meshgrid(placed_grid)

      L = Laser(G.lazor_start, G.lazor_path)
      intcp, pth, intercept_new = L.trajectory(G.lazor_path, G.grid, mesh)

      final_set = G.pointer
      total_intcp = intcp + intercept_new

      if all(x in total_intcp for x in final_set):
        outputter(mesh)
        break


class MyTest(unittest.TestCase):
    """
    A class with all the unit tests
    """

    def test_game1(self):
        '''
        A function to test the game output and whether the use of functions in the game class
        is as required.
        '''
        G1 = Game('dark_1.bff')
        G1.database()
        self.assertEqual(G1.grid, [['x', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'x']])
        self.assertEqual(G1.lazor_path, [(-1, 1), (1, -1), (-1, -1), (1, -1)])

    def test_game2(self):
        '''
        A function to test the game output and whether the use of functions in the game class
        is as required.
        '''
        G2 = Game('tiny_5.bff')
        G2.database()
        self.assertEqual(G2.blocks, {'A': 3, 'C': 1, 'B': 0})
        self.assertEqual(G2.pointer, [(1, 2), (6, 3)])

    def test_game3(self):
        '''
        A function to test the game output and whether the use of functions in the game class
        is as required.
        '''
        G3 = Game('yarn_5.bff')
        G3.database()
        self.assertEqual(G3.lazor_start, [(4, 1)])
        self.assertEqual(G3.grid, [['o', 'B', 'x', 'o', 'o'], [
            'o', 'o', 'o', 'o', 'o'], ['o', 'x', 'o', 'o', 'o'], ['o', 'x', 'o', 'o', 'x'], ['o', 'o', 'x', 'x', 'o'], [
            'B', 'o', 'x', 'o', 'o']])

    def test_sampler(self):
        '''
        A function to check if the sampler samples the right set of vacant positions or not.
        '''
        G = Game('mad_4.bff')
        G.database()
        B = Board(G.grid,G.lazor_start, G.lazor_path,G.pointer)
        self.assertEqual(B.sampler(G.grid), [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1),
            (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3), (2, 3), (3, 3), (0, 4), (1, 4), (2, 4), (3, 4)])

    def test_blocks_1(self):
        '''
        A function to check if the Blocks class can distinguish between the Blocks correctly and output apt booleans.
        '''
        G = Game('tiny_5.bff')
        G.database()
        B = Board(G.grid,G.lazor_start, G.lazor_path,G.pointer)
        mesh_board = B.sample_board(B.sampler(G.grid), G.blocks, G.grid)
        mesh = B.make_board(mesh_board)
        (a,b) = Blocks(3,1).prop(mesh)
        self.assertFalse(a)
        self.assertFalse(b)

    def test_blocks_2(self):
        '''
        A function to check if the Blocks class can distinguish between the Blocks correctly and output apt booleans.
        '''
        G = Game('yarn_5.bff')
        G.database()
        B = Board(G.grid,G.lazor_start, G.lazor_path,G.pointer)
        mesh_board = B.sample_board(B.sampler(G.grid), G.blocks, G.grid)
        mesh = B.make_board(mesh_board)
        (a,b) = Blocks(1,11).prop(mesh)
        self.assertFalse(a)
        self.assertFalse(b)

    def test_lazer1(self):
        """
        A function with a sample test file that checks if the laser class performs the trajectory accurately.
        """
        G = Game('unit_test_sample.bff')
        G.database()
        B = Board(G.grid,G.lazor_start, G.lazor_path,G.pointer)
        mesh_board = B.sample_board(B.sampler(G.grid), G.blocks, G.grid)
        mesh = B.make_board(mesh_board)
        L = Laser(G.lazor_start,G.lazor_path)
        intcp, pth, intercept_new = L.trajectory(G.lazor_path,G.grid, mesh)
        self.assertEqual(intcp, [(7, 2), (6, 1), (5, 0)])
        self.assertEqual(intercept_new, [(7, 2), (6, 3), (5, 4), (4, 3), (3, 2), (2, 1), (1, 0)])
        self.assertEqual(pth, [[(-1, 1), (-1, -1), (-1, -1)]])

    def test_lazer2(self):
        '''
        A function with a sample test file that checks if the laser class performs the trajectory and laser_strikes
        operations accurately.
        This function additionally checks if the output is right or not.
        '''
        G = Game('unit_test_sample.bff')
        G.database()
        B = Board(G.grid,G.lazor_start, G.lazor_path,G.pointer)
        mesh_board = B.sample_board(B.sampler(G.grid), G.blocks, G.grid)
        mesh = B.make_board(mesh_board)
        L = Laser(G.lazor_start,G.lazor_path)
        intcp, pth, intercept_new = L.trajectory(G.lazor_path,G.grid, mesh)
        total_intcp = intcp + intercept_new
        final_set = G.pointer
        self.assertTrue(all(x in total_intcp for x in final_set))

if __name__ == '__main__':

  solution_generator('yarn_5.bff', 500000)




    # The following line performs unit tests
  unittest.main()
