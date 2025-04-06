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



  ##### 4. Output
The only criterion for the program to achieve its goal is to make the laser hit all the target points, not the specific placement of the blocks. So in theory, the program can get different solutions through different arrangements and combinations of different blocks. However, it is assumed that the program will exit the loop after finding a solution and output the results to the .bff file in a grid format, clearly shows the final board with all the blocks and their positions.
  
### 3. Code Logic (Algorism)
先不写
### 4. Example Result Output (Maxine)
hypothesis在得到一个解以后会停止，就得到速度最快的那个解；这个代码可以完成8个bff关卡，并分别输出最快得到的解

### 5. Project Files (Yinan)
介绍一下bff
### 6. Contributions
