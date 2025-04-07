# Lazor-Project-SP25
Solver for the Lazor game as part of EN.540.635 course project

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

The laser's path is simulated step-by-step, updating position and direction based on the block it encounters. A valid solution is defined as a configuration in which all target points are hit by at least one laser beam. A maximum number of iterations is specified to prevent the algorithm from running indefinitely in cases where a solution is difficult to find or does not exist.

Note: Due to the random nature of the algorithm, multiple valid solutions may exist for the same input. However, the solver returns only the first valid solution it finds.

  ## 2.6 Output
The only criterion for the program to achieve its goal is to make the laser hit all the target points, not the specific placement of the blocks. So in theory, the program can get different solutions through different arrangements and combinations of different blocks. However, it is assumed that the program will exit the loop after finding a solution and output the results to the .bff file in a grid format, clearly shows the final board with all the blocks and their positions.
  
# 3. Code Logic
## 3.1 Game

### Game Class

The `Game` class is responsible for parsing the `.bff` file input, which defines the Lazor puzzle setup. It extracts the board layout, lazor configuration, goal points, and block inventory.

#### Class Purpose

To preprocess and provide structured data from the puzzle input file for further simulation and solving by other modules.

#### Class Methods

##### `__init__(filename: str)`

- Loads and cleans the input file by removing comments (`#`) and blank lines.
- Stores relevant data in a list called `self.raw_data`.

##### `database()`

Parses the cleaned data into structured components:

- **Grid** (`self.grid`)  
  A 2D list of strings representing the board layout between `'GRID START'` and `'GRID STOP'`.

- **Lazors** (`self.lazor_start`, `self.lazor_path`)  
  Lazor starting points and direction vectors, defined by lines starting with `L`.

- **Targets** (`self.pointer`)  
  Points that lazors must pass through, defined by lines starting with `P`.

- **Block Inventory** (`self.blocks`)  
  A dictionary storing the available number of blocks: `'A'`, `'B'`, and `'C'`.

## 3.2 Board

### Board Class

The `Board` class is responsible for preparing playable laser puzzle boards. It supports identifying valid block placement positions, randomly placing blocks, and converting the board to a fine-resolution meshgrid for laser tracing.

#### Algorithm Steps

1. **Identify Valid Positions**
   - The method `get_placeable_positions()` scans the input grid and returns all coordinates marked as `'o'`, which are valid positions for block placement.

2. **Random Block Placement**
   - The method `place_blocks_randomly()` randomly selects positions from the valid space and places blocks according to the given dictionary, such as `{'A': 2, 'B': 1, 'C': 1}`.
   - Blocks are placed in a fixed order (`C`, `A`, then `B`) to ensure consistent placement logic.
   - A deep copy of the original grid is used to avoid mutation.

3. **Grid to Meshgrid Conversion**
   - The method `create_meshgrid()` expands the original grid to a higher-resolution mesh (size \(2i+1 \times 2j+1\)) that supports laser beam tracing between cells.
   - Blocks are positioned in the mesh such that paths can be traced around and through them.

4. **One-click Board Generation**
   - `generate_full_board()` combines all above steps to return both a new playable board with blocks placed and its corresponding meshgrid.

#### Output

The final output includes:
- A board with blocks placed
- A meshgrid that can be used for laser path simulation

## 3.3 Block
The Block section of the code is designed to handle the properties of different types of blocks in the laser maze. Each block has two fundamental attributes: reflect and transmit. The types of blocks include reflective blocks (A), opaque blocks (B), refractive blocks (C), and empty spaces (o). The main function of the Block module is to determine whether a block (or an empty space) at a given position can reflect or transmit a laser beam.
Ultimately, this module answers a key question:
At a specific position in the meshgrid, does the laser encounter something that is reflective or transparent? The output is a pair of Boolean values: reflect and transmit.

## 3.4 Laser
The LaserBeam class is the core simulation engine in this project, responsible for modeling how lasers propagate through the board and interact with different block types — reflective (A), opaque (B), and refractive (C).
At each step, the laser checks surrounding cells. When it encounters:
*	a reflective block (A), it reflects based on the incident side;
*	an opaque block (B), it stops;
*	a refractive block (C), it splits into two beams — one continues and one reflects.
The class tracks all the paths and intersection points, determining whether the laser hits all required targets. The logic is modularized using helper methods for each block behavior and a boundary checker to ensure a valid simulation.
Key Method：
1.	__init _: Initializes the laser's starting points and directions.
2.	is_valid_position： Static method to check if a coordinate is within the board boundary.
3.	laser_strikes： Core method for handling laser interactions with blocks.
*	Detects nearby blocks;
*	Determines new directions based on block types (A/B/C);
*	Manages reflection and beam splitting.
4.	trajectory: Computes the complete path of each laser.
*	Starts from each origin;
*	Iteratively updates directions and intersections;
*	Aggregates all positions for validation.

## 3.5 Outputter

### Outputter Function

The `outputter()` function is responsible for converting the laser puzzle solution (stored as a fine meshgrid) into a clean and readable output format. It saves the result to a `.bff` file that shows the final layout of the game board with blocks.

#### Purpose

- Extracts the actual block positions from the fine-resolution meshgrid.
- Converts the 2D mesh into a standard board format by ignoring laser path nodes.
- Outputs the result as a human-readable file (`solution.bff`).

#### Parameters

- `mesh` (list[list[str]]): A 2D meshgrid representing the board and laser path, generated from the game's block layout.

#### Output

- `solution.bff` (file): A formatted `.bff` file showing the final solution grid using characters like `'A'`, `'B'`, `'C'`, `'x'`, `'o'`.

#### Algorithm Steps

1. Traverse through the meshgrid, picking only block coordinates (odd rows and columns).
2. Store characters representing the placed blocks into a 2D list.
3. Write this list to a file in tab-separated format.
4. Display success messages to the user.


## 3.6 Solution Generator

### Solution Generator

The `solution_generator()` function is the main engine that drives the entire laser puzzle solver. It iteratively generates possible solutions and verifies whether each candidate satisfies the constraints of the puzzle.

#### Purpose

To find a valid arrangement of blocks that allows lasers to reach all target points. The function randomly places blocks in allowed positions, simulates laser paths, and checks if all required points are intercepted.

#### Parameters

- `game_file` *(str)*: The path to the `.bff` input file containing the puzzle setup.
- `max_iter` *(int)*: The maximum number of iterations to attempt before stopping. The program will exit early if a valid solution is found.

#### Output

- If a valid solution is found, it writes a file named `solution.bff` using the `outputter()` function.

#### Algorithm Steps

1. The function runs a loop for a maximum of max_iter times.
2. For each iteration (up to `max_iter`):
   - Load the game configuration.
   - Initialize the board and determine valid positions for blocks.
   - Randomly place available blocks on the board.
   - Simulate the laser trajectory using the current block layout.
   - If all required points are intersected by laser paths:
     * Output the solution to `solution.bff`.
     * Exit the loop.

This function uses randomized search, so solutions may vary between runs unless a fixed seed is applied.


# 4. Project Files

This project uses a series of .bff (Block File Format) files to define the game levels and stores the solution in a .bff file as well. We provide 8 input files, each representing a different Lazor puzzle: dark_1.bff, mad_1.bff, mad_4.bff, mad_7.bff, numbered_6.bff, showstopper_4.bff, tiny_5.bff, yarn_5.bff. Upon successfully solving a puzzle, the solution is written to: solution.bff: This file contains the final layout of the puzzle grid, with all movable blocks correctly placed to allow the laser(s) to hit all the required target points.


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
- **File Extension**: `.bff`
- **Purpose**: Store solved configurations
- **Contains**:
  - Final block placements
- **Example**: `solution.bff`

## 4.2 .py Files (Source Code)

### Core Program Files
- **File Extension**: `.py`
- **Example**: `Lazor_Final.py`


# 5. Authors
Maxine Wang: https://github.com/Maxine-wang-7

Yinan Hu: https://github.com/yhu-010808
