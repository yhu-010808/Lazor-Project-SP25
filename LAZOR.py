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