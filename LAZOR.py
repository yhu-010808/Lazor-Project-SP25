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

  solution_generator('mad_4.bff', 500000)




    # The following line performs unit tests
  unittest.main()