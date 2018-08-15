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
        self.determine_image(enemy_type, images)

        
    def determine_image(self, enemy_type, images):
        if enemy_type == Enemy.inky:
            self._image = images.return_image('inky')

        elif enemy_type == Enemy.blinky:
            self._image = images.return_image('blinky')

        elif enemy_type == Enemy.pinky:
            self._image = images.return_image('pinky')

        elif enemy_type == Enemy.clyde:
            self._image = images.return_image('clyde')
        
    
    def determineDirection(self, board, start, pacman_y, pacman_x):
        path = self.breadth_first_search(board, start, pacman_y, pacman_x)
        
        if path is not None:
            distance = self._path_length(path)

            if self.y < path[distance][1]:
                self.direction = 'Down'

            elif self.y > path[distance][1]:
                self.direction = 'Up'

            elif self.x < path[distance][0]:
                self.direction = 'Right'

            elif self.x > path[distance][0]:
                self.direction = 'Left'

            self.movement()
        
    def _path_length(self, path) -> int:
        if len(path) > 1:
            return 1
        else:
            return 0
    
    def breadth_first_search(self, board, start, pacman_y, pacman_x):
        queue = deque([[start]])
        seen = set([start])
        gamestate = board.Gamestate


        while queue:
            path = queue.popleft()
            x, y = path[-1]
            
            #if type(gamestate[y][x]) == pacman.Pacman:
                #return path

            if (y, x) == (pacman_y, pacman_x):
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < board.board_width() and 0 <= y2 < len(board) and \
                   type(gamestate[y2][x2]) != Wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))




            
