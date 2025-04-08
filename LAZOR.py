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