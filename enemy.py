from character import Character
from wall import Wall
import pacman
from collections import deque
from random import random

class Enemy(Character):
    inky   = 5
    blinky = 6
    pinky  = 7
    clyde  = 8
    
    def __init__(self, x, y, enemy_type, images, direction = None):
        Character.__init__(self, x, y, direction)
        self.enemy_type = enemy_type
        self.invulnerable = True
        self.determine_image(enemy_type, images)
        self.pickup_memory = None

        if enemy_type == Enemy.inky:
            self.movement_turns = 10
            self.last_choice = None

        
    def discard_pickup(self):
        self.on_pickup = False
        self.pickup_memory = None
        
    def determine_image(self, enemy_type, images):
        if self.invulnerable:
            if enemy_type == Enemy.inky:
                self._image = images.return_image('inky')

            elif enemy_type == Enemy.blinky:
                self._image = images.return_image('blinky')

            elif enemy_type == Enemy.pinky:
                self._image = images.return_image('pinky')

            elif enemy_type == Enemy.clyde:
                self._image = images.return_image('clyde')
                
        else:
            self._image = images.return_image('vulnerable_ghost')

    def determine_path(self, board, start, endpoint_y, endpoint_x):
        ''' Path is towards endpoint destination if the enemy is invulnerable (the normal case).
            Otherwise, the enemy needs to retreat towards the starting location. '''
        if self.invulnerable:
            return self.breadth_first_search(board, start, endpoint_y, endpoint_x)

        else:
            return self.breadth_first_search(board, start, self.starting_point[1], self.starting_point[0])[:-1]


    def determineDirection(self, board, start, pacman_y, pacman_x):
        ''' Direction is determined by the enemy type. Since each enemy type
            has their own unique game movement. '''
        if self.enemy_type == Enemy.blinky:
            self.blinky_movement(board, start, pacman_y, pacman_x)

        elif self.enemy_type == Enemy.inky:
            self.inky_movement(board, start, pacman_y, pacman_x)
        
        elif self.enemy_type == Enemy.pinky:
            self.pinky_movement(board, start, pacman_y, pacman_x)

        elif self.enemy_type == Enemy.clyde:
            self.clyde_movement(board, start)

    # Inky Movement Functions #
    def blinky_movement(self, board, start, pacman_y, pacman_x):
        ''' Blinky's movement is to directly chase Pacman on the board. '''
        path = self.determine_path(board, start, pacman_y, pacman_x)
        self.path_finding_direction(path)

    # Blinky Movement Functions #
    def inky_movement(self, board, start, endpoint_y, endpoint_x):
        ''' Inky's movement differentiates between the other three ghost. So we use
            random() from the random library to determine which movement he will follow,
            and it will constantly be changing as time goes on. '''
        choice = self.inkys_choice()
        self._inky_movement_turns()

        if choice <= .33:
            return self.blinky_movement(board, start, endpoint_y, endpoint_x)

        elif choice <= .75:
            return self.clyde_movement(board, start)

        elif choice <= 1:
            return self.pinky_movement(board, start, endpoint_y, endpoint_x)

    def inkys_choice(self):
        ''' Inky has unstable movement, but the movement choices occur every 10 updates.
            So the last choice is saved to keep it going for 10 updates in a row. '''
        if self.movement_turns == 10:
            self.last_choice = random()

        return self.last_choice
    
    def _inky_movement_turns(self):
        self._decrement_movement_turns()

        if self.movement_turns == 0:
            self.movement_turns = 10
            self.last_choice = None
 
    def _decrement_movement_turns(self):
        ''' Decrements the attribute movement_turns by 1 until it reaches 0,
            but will never stay at 0, or be less than 0. '''
        self.movement_turns -= 1
        
    # Pinky Movement Functions #
    def pinky_movement(self, board, start, pacman_y, pacman_x):
        ''' Pinky's movement is meant to ambush, so we have pacman's location
            points to plot the best path to get in front of him. '''
        # --> endpoints done here

        # endpoints plugged below
        path = self.determine_path(board, start, pacman_y, pacman_x)

        #self.path_finding_direction(path)


    def pinky_endpoints(self):
        pass

    
    # Clyde Movement Functions #
    def clyde_movement(self, board, start):
        ''' Clyde's movement is random, and he does not chase or ambush. That
            is why it is not required for him to have any endpoint arguments. '''
        # --> endpoints done here
        endpoint_y, endpoint_x = 2, 1

        # endpoints plugged below
        path = self.determine_path(board, start, endpoint_y, endpoint_x)

        self.path_finding_direction(path)
    
    # Pathfinding Functions #
    def path_finding_direction(self, path):
        ''' This function is what changes the direction depending on the next location
            the enemy needs to go. Only one case will follow each time and then once that
            direction is set, the location is saved, and movement() is called to move the
            enemy. '''
        if self.not_empty_path( path ):
            distance = self._path_length(path)

            if self.y < path[distance][1]:
                self.direction = 'Down'

            elif self.y > path[distance][1]:
                self.direction = 'Up'

            elif self.x < path[distance][0]:
                self.direction = 'Right'

            elif self.x > path[distance][0]:
                self.direction = 'Left'

            self.last_location = self.return_location()
            self.movement()
    
    def breadth_first_search(self, board, start, endpoint_y, endpoint_x):
        ''' The bfs algorithm is required in order to transverse through the
            2d board and find the quickest path that leads directly to the endpoint
            locations. '''
        queue = deque([[start]])
        seen = set([start])
        gamestate = board.Gamestate


        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (y, x) == (endpoint_y, endpoint_x):
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < board.board_width() and 0 <= y2 < len(board) and \
                   type(gamestate[y2][x2]) != Wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def _path_length(self, path) -> int:
        ''' This function is a helper function to avoid index errors depending on
            how large the path is. '''
        if len(path) > 1:
            return 1
        else:
            return 0


    def not_empty_path(self, path) -> bool:
        ''' Returns a boolean if the path is not empty. '''
        return path is not None and path != []
