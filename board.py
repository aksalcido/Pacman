from pacman import Pacman
from pickup import Pickup
from enemy import Enemy
from wall import Wall


class Board():

    def __init__(self, width, height, images):
        self._window_width = width
        self._window_height = height

        self.Gamestate = None
        self.gameObjects = set()
        self.images = images
        self.pacman = None

    # Level Functions #
    def new_level(self):
        ''' Called when a new level is needed. Alters the Gamestate (which consist of numbers)
            to consist of Pacman game objects. Then updateObjects() is called to fill the
            gameObjects set with all the objects that are on the board. And the initial location
            of Pacman is set. '''
        score, lives, level = self.currentStats()
        self.Gamestate = Board.create_board()
        self.Gamestate = self._pacmanBoard( self.square_height(), self.square_width() )
        self._updateObjects()
        self.pacman = self.pacmanLocation()
        self.pacman.levelUp(score, lives, level)

    def level_complete(self) -> bool:
        ''' Returns true or false if the total pickups on the board is 0.
            If 0 the level is complete, otherwise the game is still going. '''
        total_pickups = { p for p in self.gameObjects if type(p) == Pickup }

        return len(total_pickups) == 0

    def currentStats(self) -> tuple:
        if self.Gamestate is not None:
            score = self.pacman.score
            lives = self.pacman.lives
            level = self.pacman.level + 1
        else:
            score = 0
            lives = 3
            level = 1

        return score, lives, level

    # Game Update Functions #
    def updateGamestate(self, x, y):
        #self.validateScore(x, y)
        self.validateMovement(x, y)
        
        if self.validatePath( self.pacman.direction ):
            if self.pacman.direction == 'Left':
                self.Gamestate[x][y+1] = None

            elif self.pacman.direction == 'Right':
                self.Gamestate[x][y-1] = None

            elif self.pacman.direction == 'Down':
                self.Gamestate[x-1][y] = None

            elif self.pacman.direction == 'Up':
                self.Gamestate[x+1][y] = None

    def _updateObjects(self):
        ''' Updates the gameObjects set to the objects that are inside the current Gamestate.
            Also updates where the current location of Pacman is on the board. '''
        self.gameObjects = { objs for rows in self.Gamestate for objs in rows if objs is not None }
        self.pacman = self.pacmanLocation()
        self.updateGamestate(self.pacman.y, self.pacman.x)

    def pacmanLocation(self) -> Pacman:
        ''' Returns the Pacman object on the board. '''
        for rows in self.Gamestate:
            for gameObj in rows:
                if type(gameObj) == Pacman:
                    return gameObj

    # Direction Validation Functions #
    def validatePath(self, direction) -> bool:
        pacman = self.pacmanLocation()
        
        if direction == 'Left':
            return type(self.Gamestate[pacman.y][pacman.x - 1]) != Wall

        elif direction == 'Right':
            return type(self.Gamestate[pacman.y][pacman.x + 1]) != Wall

        elif direction == 'Down':
            return type(self.Gamestate[pacman.y + 1][pacman.x]) != Wall

        elif direction == 'Up':
            return type(self.Gamestate[pacman.y - 1][pacman.x]) != Wall

    def validateMovement(self, x, y):
        '''
        Checks for the case that Pacman crosses to the other side via one side,
        which are when x == 14 and y == 0 or 27. If this is the case, the pacman
        object changes it's x and y with the crossedBoundary method. Otherwise the
        Gamestate is updated regularly.
        '''
        if (x == 14 and y == 0) or (x == 14 and y == 27):
            self.pacman.crossedBoundary()
            self.Gamestate[self.pacman.y][self.pacman.x] = self.pacman

        else:
            self.pacman.updateScore( self.Gamestate[x][y] )
            self.Gamestate[x][y] = self.pacman

    # Individual Game Object Size Settings #
    def square_height(self) -> float:
        ''' Returns the height of each individual square in the level. '''
        return self._window_height / len(self)

    def square_width(self) -> float:
        '' 'Returns the width of each individual square in the level. '''
        return self._window_width / self._board_width()

    def _board_width(self) -> int:
        ''' Returns the width of the board, [0] as an index since all list inside are same length. '''
        return len(self.Gamestate[0])

    # Overriding Functions #
    def __len__(self) -> int:
        ''' Overrides len() function, and also returns the height of the board. '''
        return len(self.Gamestate)

    def __getitem__(self, key):
        ''' Overrides the __getitem__() so that we can return an index of the Gamestate list. '''
        return self.Gamestate[key]
    
    def __iter__(self):
        ''' Overrides the iter() method so that we can use a for loop on the board object. '''
        for row in self.Gamestate:
            yield row

    # Board Creation Functions #
    def _pacmanBoard(self, height, width) -> [list]:
        ''' Takes the board of numbers, and easily sets up the coordinates of each object,
            as manually typing each object with their coordinates would take way too long. '''
        gameBoard = []
        
        for i in range(len(self)):
            gameRow = []
            for j in range(len(self[i])):
                # 0
                if self[i][j] == Wall.wall:
                    gameRow.append( Wall(j, i, self.images) )

                # 1
                elif self[i][j] == Pickup.pickup:
                    gameRow.append( Pickup(j, i, self.images) )

                # 3
                elif self[i][j] == Pickup.boostUp:
                    gameRow.append( Pickup(j, i, self.images, True) )

                # 5, 6, 7, 8
                elif self[i][j] == Enemy.inky or self[i][j] == Enemy.blinky or self[i][j] == Enemy.pinky or self[i][j] == Enemy.clyde:
                    gameRow.append( Enemy(j, i, self[i][j], self.images) )

                # 9
                elif self[i][j] == Pacman.pacman:
                    gameRow.append( Pacman(j, i, self.images) )

                else:
                    gameRow.append( None )

            gameBoard.append(gameRow)

        return gameBoard

    @classmethod
    def create_board(self):
        #Sets up the board with the numbers, that will represent the objects
        new_board = \
        [ [0 for i in range(28)],
          ([0] + [1 for i in range(12)] + [0]) * 2,
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0],
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], # replace 9 with 1
          [0] + [1 for i in range(26)] + [0],
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, None, 0, 0, None, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, None, 0, 0, None, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, None, None, None, None, None, None, None, None, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, None, None, None, None, None, None, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [None, None, None, None, None, None, 1, 0, 0, None, 0, None, None, None, None, None, None, 0, None, 0, 0, 1, None, None, None, None, None, None],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, None, 5, 6, 7, 8, None, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [None, None, None, None, None, 0, 1, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 1, 0, None, None, None, None],
          [None, None, None, None, None, 0, 1, 0, 0, None, None, None, None, None, None, None, None, None, None, 0, 0, 1, 0, None, None, None, None, None],
          [None, None, None, None, None, 0, 1, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 1, 0, None, None, None, None, None],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, 0, 0, 0, 0, 0, 0, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          ([0] + [1 for i in range(12)] + [0]) * 2,
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
          [0, 3, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 9, None, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 3, 0, 0],
          [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
          [0] + [1 for i in range(26)] + [0],
          [0 for i in range(28)]]
        
        
        return new_board

    '''
    ### USED PRIMARILY FOR TESTING PURPOSES ###
    @classmethod
    def create_board(self):
        # Sets up the board with the numbers, that will represent the objects
        new_board = \
        [[0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
          [0 for i in range(28)],
         [0 for i in range(28)],
         [0 for i in range(28)],
         [0 for i in range(28)],
          [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 9, None, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0 for i in range(28)],
          [0 for i in range(28)],
         [0 for i in range(28)],
         [0 for i in range(28)],
         [0 for i in range(28)]]
        
        
        return new_board

'''
    
