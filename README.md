# Lazor-Project-SP25
Solver for the Lazor game as part of EN.540.635 course project

Let's begin the project 

# 1. Introduction
This project aims to solve the "Lazors" puzzle game by automatically placing blocks to direct lasers to specified targets. It reads board configurations from .bff files, supports reflect, opaque, and refract blocks, and outputs solutions.

Key requirements:

* Parse .bff files and validate inputs.
* Model block interactions using classes.
* Solve boards within 2 minutes.
* Output clear solutions.

# 2. Methodology 
  ## 2.1 Overview
The aim of Lazors game follows a modular and object-oriented approach. Below is a breakdown of the methodology we used:
  ## 2.2 Input Parsing
The input files are eight .bff files, representing different levels. The files contain following components:

a. The overall layout of the board grid (from GRID START to GRID STOP)

b. Types and number of blocks
* x = no block allowed for placing blocks
* o = blockes allowd for placing blocks
* A = fixed reflect block
* B = fixed opaque block
* C = fixed refract block

c. Laser origin points 

d. Laser directions

  __ __ __ __\ +x<br/>
 |          
 |<br/>
 |<br/>
\|/ +y<br/>

e. Target points to be hit by lasers (lazer intersect points)

The .bff file is parsed into internal data structures that represent the board, lasers, and block availability.
  
  ## 2.3 Class Objects
Different Python classes are used to appropriately represent core game components:
* Board: Holds the grid structure and handles block placement and laser simulation.
* Block: Represents basic classification for all block types, with subclasses ReflectBlock, OpaqueBlock, and RefractBlock.
* Lazor: Represents the position and direction of a lazor beam.

  ## 2.4 Laser Simulation
A laser trajectory simulator is implemented to decide what to do next based on the interaction of the laser with different 
blocks:
* Reflection at a 90° angle after meeting reflect block (A)
* Absorption (stop) after meeting opaque block (B): 
* Refraction (split into two paths) after meeting refract block (C)
* Termination of the path if the laser goes out of bounds

All laser paths will be fully simulated and recorded.

  ## 2.5 Solving Algorism
The solver applies a randomized iterative algorithm to place the movable blocks (A: Reflective, B: Absorbing, C: Refractive) on the board to direct laser beams toward all required target points. In each iteration: The algorithm randomly selects positions on the board marked with o as possible block locations. It prioritizes placing refractive blocks (C) first, then reflective blocks (A), and finally absorbing blocks (B). This strategy increases the probability of successfully completing the laser path, as refractive blocks allow both transmission and reflection, effectively splitting the beam into two paths and expanding coverage.

The laser's path is simulated step-by-step, updating position and direction based on the block it encounters. A valid solution is defined as a configuration in which all target points are hit by at least one laser beam.

A maximum number of iterations is specified to prevent the algorithm from running indefinitely in cases where a solution is difficult to find or does not exist.

Note: Due to the random nature of the algorithm, multiple valid solutions may exist for the same input. However, the solver returns only the first valid solution it finds.

  ## 2.6 Output
The only criterion for the program to achieve its goal is to make the laser hit all the target points, not the specific placement of the blocks. So in theory, the program can get different solutions through different arrangements and combinations of different blocks. However, it is assumed that the program will exit the loop after finding a solution and output the results to the .bff file in a grid format, clearly shows the final board with all the blocks and their positions.
  
# 3. Code Logic (Algorism)
## 3.1 Game

This puzzle game is based on block placement and laser beam simulation. Players are given a fixed grid, a laser source, and a set of blocks that can reflect or redirect the beam. The goal is to determine a valid placement of blocks such that the laser hits all target points.

### How It Works

- A coarse grid represents valid block positions (`'o'`).
- A set of blocks (types A, B, C) is available to be placed.
- After placement, a laser is fired and travels based on the properties of blocks in its path.
- The laser path is traced on a fine meshgrid that helps detect intersections with targets.

### Block Types

| Block Type | Behavior                      |
|------------|-------------------------------|
| A          | Reflects laser 90°            |
| B          | Transmits and reflects part   |
| C          | Fully transmits and redirects |

### Project Structure

- `board.py`: Logic for generating playable boards and meshgrid
- `lazor_solver.py`: Simulates laser behavior
- `main.py`: Game entry point
- `resources/`: Game maps and block settings

## 3.2 Board

The `Board` class is responsible for generating a random, valid configuration of the game grid and converting it into a grid suitable for the laser simulation.

### Main Functions

#### `get_placeable_positions()`
Finds all grid positions where blocks can be placed (marked as `'o'`).

#### `place_blocks_randomly(sample_space, block_dict, seed=None)`
Randomly selects positions and places a specific number of blocks of each type.

#### `create_meshgrid(grid)`
Converts a coarse grid (i x j) into a fine meshgrid (2i+1 x 2j+1) to allow laser traversal between and through blocks.

#### `generate_full_board(seed=None)`
High-level wrapper that performs the full process:
1. Samples valid block positions
2. Randomly places blocks
3. Builds the meshgrid

## 3.3 Block


## 3.4 Laser


## 3.5 Solution Output

The `generate_solution_output.py` provides functions to display and save Lazor game grid solutions in a readable format.

### Main Functions

#### `print_grid(grid: List[List[str]]) -> None`

Prints the game grid to the console in a formatted layout.

- **Parameters**:
  - `grid`: A 2D list of strings representing the Lazor game board.

#### `save_solution_to_file(grid: List[List[str]], filename: str = "output.txt") -> None`

Saves the formatted grid to a text file for documentation or analysis.

- **Parameters**:
  - `grid`: A 2D list of strings representing the Lazor game board.
  - `filename`: Name of the output file (default: `"output.txt"`)

## 3.6 Solution
The `generate_solution.py` implements a random trial-based algorithm to find a valid solution to a Lazor puzzle.

### Main Functions

#### `generate_solution(grid, origin, path, pointers, blocks, max_attempts=10000, verbose=True)`

Attempts to generate a valid solution grid by randomly placing blocks and simulating Lazor trajectories.

# 4. Project Files
## 4.1 .bff Files (Board File Format)

### Input Files
- **File Extension**: `.bff`
- **Purpose**: Define puzzle configurations
- **Contains**:
  - Grid layout with allowed/fixed block positions
  - Laser starting positions and directions
  - Target points that must be intersected
- **Example**: `mad_1.bff`

### Output Files
- **File Extension**: `.bff` (or other formats like `.txt`)
- **Purpose**: Store solved configurations
- **Contains**:
  - Final block placements
- **Example**: `solution.bff`

## 4.2 .py Files (Source Code)

### Core Program Files
- **File Extension**: `.py`
- **Example**: `output/level1_solution.py`

# 5. Contributions
Maxine Wang:
Yinan Hu:
