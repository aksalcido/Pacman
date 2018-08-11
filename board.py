from pacman import Pacman
from pickup import Pickup
from enemy import Enemy
from wall import Wall


class Board():

    def __init__(self, width, height, images):
        self._window_width = width

        self._window_height = height

        self.Gamestate = None
        self.images = images
        self.game_objects = set()
        self.pacman = None
        self.enemies = set()
        self._game_over = False

    # Level Functions #
    def new_level(self):
        ''' Called when a new level is needed. Alters the Gamestate (which consist of numbers)
            to consist of Pacman game objects. Then update_objects() is called to fill the
            game_ojects set with all the objects that are on the board. And the initial location
            of Pacman is set. '''
        score, lives, level = self.current_stats()
        self.Gamestate = Board.create_board()
        self.Gamestate = self._pacman_board( self.square_height(), self.square_width() )
        self.update_board()
        self.pacman = self.pacman_location()
        self.pacman.level_up(score, lives, level)
        self.enemies = { e for e in self.game_objects if type(e) == Enemy }

    def level_complete(self) -> bool:
        ''' Returns true or false if the total pickups on the board is 0.
            If 0 the level is complete, otherwise the game is still going. '''
        total_pickups = { p for p in self.game_objects if type(p) == Pickup }

        return len(total_pickups) == 0

    def current_stats(self) -> tuple:
        if self.Gamestate is not None: # Game has started and level transitioning #
            score = self.pacman.score
            lives = self.pacman.lives
            level = self.pacman.level + 1
        else:
            score = 0
            lives = 3
            level = 1

        return score, lives, level

    def check_for_gameover(self):
        ''' This function mainly checks for the progress of Pacman. If Pacman
            dies and is out of lives, then the game is over. Otherwise, respawns
            from the original spot. If Pacman is still alive, then the board is
            just updated with his new position. '''
        self.pacman.lose_life()

        if not self.pacman.out_of_lives():
            self.pacman.is_respawning = True
            self.pacman.respawn( self.images )
            self.Gamestate[self.pacman.y][self.pacman.x] = self.pacman

        else:
            self.game_over()

    def game_over(self):
        self._game_over = True
    
    # Game Update Functions #
    def update_board(self):
        ''' Updates the game_objects set to the objects that are inside the current Gamestate.
            Also updates where the current location of Pacman is on the board. '''
        self.game_objects = { objs for rows in self.Gamestate for objs in rows if objs is not None }
        self.pacman = self.pacman_location()
        self.update_gamestate()
    
    def update_gamestate(self):
        y, x = self.pacman.return_location()
        self.validate_movement(y, x)
        self.validate_enemy_movement(y, x)
    
        if not self._game_over:
            self._update_board_square(y, x)
        else:
            self.Gamestate[y][x] = None


    def _update_board_square(self, y, x):
        ''' Updates the last spot that Pacman was in and makes it None, this is specifically
            aimed to assist at updating the board while removing the Pickups when Pacman
            goes over them. Then, the Gamestate is updating with Pacman's new location. '''
        if self.validate_path( self.pacman.direction ):
            if self.pacman.direction == 'Left':
                self.Gamestate[y][x+1] = None

            elif self.pacman.direction == 'Right':
                self.Gamestate[y][x-1] = None

            elif self.pacman.direction == 'Down':
                self.Gamestate[y-1][x] = None

            elif self.pacman.direction == 'Up':
                self.Gamestate[y+1][x] = None

            self.Gamestate[y][x] = self.pacman

    def _update_directions(self):
        if self.pacman.has_upcoming_direction():
            if self.validate_path( self.pacman.next_direction ):
                self.pacman.change_direction(self.pacman.next_direction)
                self.pacman.next_direction = None
                self.pacman.direction_image( self.images )

        if self.validate_path( self.pacman.direction ):
            self.pacman.movement()
                
    
    def pacman_location(self) -> Pacman:
        ''' Returns the Pacman object on the board. '''
        for game_obj in self.game_objects:
            if type(game_obj) == Pacman:
                return game_obj

    # Direction Validation Functions #
    def validate_path(self, direction) -> bool:
        ''' Ensures that the direction Pacman is attempting to go is not a
            Wall object. If there is no wall in the next spot, returns True,
            else returns False. '''
        pacman = self.pacman_location()
        
        if direction == 'Left':
            return type(self.Gamestate[pacman.y][pacman.x - 1]) != Wall

        elif direction == 'Right':
            return type(self.Gamestate[pacman.y][pacman.x + 1]) != Wall

        elif direction == 'Down':
            return type(self.Gamestate[pacman.y + 1][pacman.x]) != Wall

        elif direction == 'Up':
            return type(self.Gamestate[pacman.y - 1][pacman.x]) != Wall

    def validate_movement(self, y, x):
        '''
        Checks for the case that Pacman crosses to the other side via one side,
        which are when x == 14 and y == 0 or 27. If this is the case, the pacman
        object changes it's x and y with the crossed_boundary method. Otherwise the
        Gamestate is updated regularly.
        '''
    
        if (y == 14 and x == 0) or (y == 14 and x == 27):
            self.pacman.crossed_boundary()
            self.Gamestate[self.pacman.y][self.pacman.x] = self.pacman

        else:
            self.pacman.contact( self.Gamestate[y][x] )

    def validate_enemy_movement(self, pacman_y, pacman_x):
        for enemy in self.enemies:
            enemy.determineDirection(self, (enemy.x, enemy.y), pacman_y, pacman_x)
            self._validate_enemy_position(enemy, pacman_y, pacman_x)

    def _validate_enemy_position(self, enemy, pacman_y, pacman_x):
        ''' Checks if the position of the enemy is the same position as Pacman, if so then
            calls the function check_for_gameover(). Else it's just going to update the
            board with the enemy. '''
        if (e.y, e.x) == (pacman_y, pacman_x):
            self.check_for_gameover()
        else:
            self.Gamestate[e.y][e.x] = enemy
    
    # Individual Game Object Size Settings #
    def square_height(self) -> float:
        ''' Returns the height of each individual square in the level. '''
        return self._window_height / len(self)

    def square_width(self) -> float:
        '' 'Returns the width of each individual square in the level. '''
        return self._window_width / self.board_width()

    def board_width(self) -> int:
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
    def _pacman_board(self, height, width) -> [list]:
        ''' Takes the board of numbers, and easily sets up the coordinates of each object,
            as manually typing each object with their coordinates would take way too long. '''
        game_board = []
        
        for i in range(len(self)):
            game_row = []
            for j in range(len(self[i])):
                # 0
                if self[i][j] == Wall.wall:
                    game_row.append( Wall(j, i, self.images) )

                # 1
                elif self[i][j] == Pickup.pickup:
                    game_row.append( Pickup(j, i, self.images) )

                # 3
                elif self[i][j] == Pickup.boostUp:
                    game_row.append( Pickup(j, i, self.images, True) )

                # 5, 6, 7, 8
                elif self[i][j] == Enemy.inky or self[i][j] == Enemy.blinky or self[i][j] == Enemy.pinky or self[i][j] == Enemy.clyde:
                    game_row.append( Enemy(j, i, self[i][j], self.images) )

                # 9
                elif self[i][j] == Pacman.pacman:
                    game_row.append( Pacman(j, i, self.images) )

                else:
                    game_row.append( None )

            game_board.append(game_row)

        return game_board

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
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, 0, None, 0, 0, None, 0, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, None, None, None, None, None, None, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [None, None, None, None, None, None, 1, 0, 0, None, 0, None, None, None, None, None, None, 0, None, 0, 0, 1, None, None, None, None, None, None],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, None, 5, 0, 0, 0, None, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0], #          [0, 0, 0, 0, 0, 0, 1, 0, 0, None, 0, None, 5, 6, 7, 8, None, 0, None, 0, 0, 1, 0, 0, 0, 0, 0, 0],
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

    ### USED PRIMARILY FOR TESTING PURPOSES ###
'''
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
