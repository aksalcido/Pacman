from character import Character
from wall import Wall
import pacman
from collections import deque

class Enemy(Character):
    inky   = 5
    blinky = 6
    pinky  = 7
    clyde  = 8
    
    def __init__(self, x, y, enemy_type, images, speed = 1, direction = None):
        Character.__init__(self, x, y, speed, direction)
        self.enemy_type = enemy_type
        self.invulnerable = True
        self.determine_image(enemy_type, images)
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
    '''
    def slow_down(self, path):
        new_path = []

        # indexed by 1 to remove the current spot it's in, and stops at half the list because theres no reason to double an already large list
        for spots in path[1:len(path)//2]:
            new_path.extend( [spots, spots] )   # double the amount of time to move

        return new_path
    '''
    
    def determine_path(self, board, start, pacman_y, pacman_x):
        ''' Path is towards Pacman if the enemy is invulnerable (the normal case).
            Otherwise, the enemy needs to retreat towards the starting location. '''
        if self.invulnerable:
            return self.breadth_first_search(board, start, pacman_y, pacman_x)

        else:
            return self.breadth_first_search(board, start, self.starting_point[1], self.starting_point[0])


    def determineDirection(self, board, start, pacman_y, pacman_x):
        ''' Direction is determined by the enemy type. Since each enemy type
            has their own unique game movement. '''
        if self.enemy_type == Enemy.inky:
            self.inky_movement(board, start, pacman_y, pacman_x)

        elif self.enemy_type == Enemy.blinky:
            pass
        
        elif self.enemy_type == Enemy.pinky:
            pass

        elif self.enemy_type == Enemy.clyde:
            pass

    # Inky Movement Functions #
    def inky_movement(self, board, start, pacman_y, pacman_x):
        path = self.determine_path(board, start, pacman_y, pacman_x)
        
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
    
    def breadth_first_search(self, board, start, pacman_y, pacman_x):
        ''' The bfs algorithm is required in order to transverse through the
            2d board and find the quickest path that leads directly to pacman's
            location. '''
        queue = deque([[start]])
        seen = set([start])
        gamestate = board.Gamestate


        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (y, x) == (pacman_y, pacman_x):
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < board.board_width() and 0 <= y2 < len(board) and \
                   type(gamestate[y2][x2]) != Wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
    
    def _path_length(self, path) -> int:
        if len(path) > 1:
            return 1
        else:
            return 0

    # Blinky Movement Functions #
    def blinky_movement(self):
        pass


    
    # Pinky Movement Functions #
    def pinky_movement(self):
        pass


    
    # Clyde Movement Functions #
    def clyde_movement(self):
        pass




    def not_empty_path(self, path) -> bool:
        ''' Returns a boolean if the path is not empty. '''
        return path is not None and path != []
