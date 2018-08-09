from character import Character
from wall import Wall
import pacman
from collections import deque

class Enemy(Character):
    inky   = 5
    blinky = 6
    pinky  = 7
    clyde  = 8
    
    def __init__(self, x, y, enemyType, images, speed = 1, direction = None):
        Character.__init__(self, x, y, speed, direction)
        self.enemyType = enemyType
        self.determineImage(enemyType, images)


    def determineImage(self, enemyType, images):
        if enemyType == Enemy.inky:
            self._image = images.return_image('inky')

        elif enemyType == Enemy.blinky:
            self._image = images.return_image('blinky')

        elif enemyType == Enemy.pinky:
            self._image = images.return_image('pinky')

        elif enemyType == Enemy.clyde:
            self._image = images.return_image('clyde')
        
    
    def determineDirection(self, board, start):
        path = self.breadth_first_search(board, start)

        if path is not None:
            
            if self.y < path[1][1]:
                self.direction = 'Down'

            elif self.y > path[1][1]:
                self.direction = 'Up'

            elif self.x < path[1][0]:
                self.direction = 'Right'

            elif self.x > path[1][0]:
                self.direction = 'Left'


        
    def breadth_first_search(self, board, start):
        queue = deque([[start]])
        seen = set([start])

        while queue:
            path = queue.popleft()
            x, y = path[-1]
            
            if type(board[y][x]) == pacman.Pacman:
                return path

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < board.board_width() and 0 <= y2 < len(board) and \
                   type(board[y2][x2]) != Wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))




            
