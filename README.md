# Lazor-Project-SP25
Solver for the Lazor game as part of EN.540.635 course project

Let's begin the project 

### 1. Introduction (Yinan)
概括lazor project是干什么的
### 2. Methodology (Maxine)
  ##### 1. Overview
The aim of Lazors game follows a modular and object-oriented approach. Below is a breakdown of the methodology we used:
  ##### 2. Input Parsing
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
  __________\ +x
 |          /
 |
 |
\|/ +y

e. Target points to be hit by lasers (lazer intersect points)

The .bff file is parsed into internal data structures that represent the board, lasers, and block availability.
  
  ##### 3. Class Objects
Different Python classes are used to appropriately represent core game components:
* Board: Holds the grid structure and handles block placement and laser simulation.
* Block: Represents basic classification for all block types, with subclasses ReflectBlock, OpaqueBlock, and RefractBlock.
* Lazor: Represents the position and direction of a lazor beam.

  ##### 4. Laser Simulation
A laser trajectory simulator is implemented to decide what to do next based on the interaction of the laser with different 
blocks:
* Reflection at a 90° angle after meeting reflect block (A)
* Absorption (stop) after meeting opaque block (B): 
* Refraction (split into two paths) after meeting refract block (C)
* Termination of the path if the laser goes out of bounds

All laser paths will be fully simulated and recorded.

  ##### 5. Solving Algorism
The solver applies a randomized iterative algorithm to place the movable blocks (A: Reflective, B: Absorbing, C: Refractive) on the board to direct laser beams toward all required target points. In each iteration: The algorithm randomly selects positions on the board marked with o as possible block locations. It prioritizes placing refractive blocks (C) first, then reflective blocks (A), and finally absorbing blocks (B). This strategy increases the probability of successfully completing the laser path, as refractive blocks allow both transmission and reflection, effectively splitting the beam into two paths and expanding coverage.

The laser's path is simulated step-by-step, updating position and direction based on the block it encounters. A valid solution is defined as a configuration in which all target points are hit by at least one laser beam.

A maximum number of iterations is specified to prevent the algorithm from running indefinitely in cases where a solution is difficult to find or does not exist.

Note: Due to the random nature of the algorithm, multiple valid solutions may exist for the same input. However, the solver returns only the first valid solution it finds.

  ##### 6. Output
The only criterion for the program to achieve its goal is to make the laser hit all the target points, not the specific placement of the blocks. So in theory, the program can get different solutions through different arrangements and combinations of different blocks. However, it is assumed that the program will exit the loop after finding a solution and output the results to the .bff file in a grid format, clearly shows the final board with all the blocks and their positions.
  
### 3. Code Logic (Algorism)
先不写

### 4. Project Files (Yinan)
介绍一下bff
### 5. Contributions
Maxine Wang:
Yinan Hu:
