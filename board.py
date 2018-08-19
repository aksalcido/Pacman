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
        if self.Gamestate is not None: # Game has started and level transitioning
            score = self.pacman.score
            lives = self.pacman.lives
            level = self.pacman.level + 1
        else:
            score = 0
            lives = 3
            level = 1

        return score, lives, level

    def game_continuation(self, y, x, previous_y, previous_x) -> None:
        ''' Checks if Pacman is ongoing to an enemy, if so restarts the level due to death.
            Otherwise, checks if the game is not over, and if so updates the board square.
            Otherwise, Pacman's location become's None because the game is done. '''
        if self.validate_upcoming_enemy(y, x):
            if not self.pacman.invulnerable:
                self.check_for_gameover()

        else:
            if not self._game_over:
                self._update_board_square(y, x, previous_y, previous_x)
            else:
                self.Gamestate[y][x] = None
    
    def check_for_gameover(self):
        ''' This function mainly checks for the progress of Pacman. If Pacman
            dies and is out of lives, then the game is over. Otherwise, respawns
            from the original spot. If Pacman is still alive, then the board is
            just updated with his new position. '''
        self.pacman.lose_life() # Pacman loses a life on death

        if not self.pacman.out_of_lives():
            self.update_respawn_board()
        else:
            self.game_over()

    def game_over(self):
        self._game_over = True

    def restore_pickup(self, enemy):
        ''' Restores a pickup that an enemy went over because the way the game is organized,
            requires board updation, and an enemy overwrites a spot. Due to this, the enemy
            must store a boolean if the spot it goes over has a pickup, and once the enemy
            leaves the spot, the pick up is restored. '''
        if enemy.pickup_memory is not None:
            y, x = enemy.last_location
            self.Gamestate[y][x] = enemy.pickup_memory
            enemy.on_pickup = False
            enemy.pickup_memory = None
    
    # Game Update Functions #
    def update_board(self):
        ''' Updates the game_objects set to the objects that are inside the current Gamestate.
            Also updates where the current location of Pacman is on the board. '''
        self.game_objects = { objs for rows in self.Gamestate for objs in rows if objs is not None }
        self.pacman = self.pacman_location()
        self.update_gamestate()

    def update_gamestate(self):
        ''' Updates the entire gamestate each time it is called. This function is in charge of
            all the character object's movement, and game states as the game progresses. '''
        previous_y, previous_x = self.pacman.return_location()      # pacman's previous updated location is stored to validate the next player movement
        self.validate_movement(previous_y, previous_x)              # pacman's movement is validated from current spot, and then pacman has a new location
        
        new_y, new_x = self.pacman.return_location()                # pacman's new updated location is stored
        self.validate_pacman_state()                                # validates if pacman picks up a boost
        
        self.validate_enemy_movement(new_y, new_x)                  # enemies need to determine direction -> pacman's new location
        self.game_continuation(new_y, new_x, previous_y, previous_x)# checks for death, game over, and updates Pacman's previous board square


    def _update_board_square(self, y, x, previous_y, previous_x):
        ''' Updates the last spot that Pacman was in and makes it None, this is specifically
            aimed to assist at updating the board while removing the Pickups when Pacman
            goes over them. Then, the Gamestate is updating with Pacman's new location. '''
        if self.validate_path( self.pacman.direction ):
            self.Gamestate[previous_y][previous_x] = None

        self.Gamestate[y][x] = self.pacman

    def _update_directions(self):
        ''' This function is what allows smoother movement when wanting to change Pacman's
            direction. It checks if Pacman has queue'd another direction that wasn't possible
            at the previous state, and if no other directions are hit in the mean time, then
            that move is executed when a possible path is validated. '''
        if self.pacman.has_upcoming_direction():
            if self.validate_path( self.pacman.next_direction ):
                self.pacman.change_direction(self.pacman.next_direction)
                self.pacman.next_direction = None
                self.pacman.direction_image( self.images )

        if self.validate_path( self.pacman.direction ):
            self.pacman.last_location = self.pacman.return_location()
            self.pacman.movement()
                
    def update_respawn_board(self):
        ''' When pacman is respawning, Pacman and all the enemies are put in their
            original starting position. '''
        self.pacman.respawn( self.images )
        self.Gamestate[self.pacman.y][self.pacman.x] = self.pacman
        self.update_enemy_respawns()


    def update_enemy_respawns(self):
        ''' Updates all of the enemy positions on the board back to their original spot
            when level needs to be restarted. '''
        for enemy in self.enemies:
            enemy.initial_position()
            self.Gamestate[enemy.y][enemy.x] = enemy

    def update_enemy_states(self):
        ''' Flips the enemies invulnerability state depending on if Pacman has
            just eaten a boost. Then once it wears off, the function is called
            again to flip back to normal. '''
        for enemy in self.enemies:
            enemy.invulnerability()
            enemy.determine_image(enemy.enemy_type, self.images)
        
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


    def validate_pacman_state(self):
        ''' Checks if Pacman is invulnerable, if he is then the special case
            where he is able to kill the enemies starts and counts down after
            each update. '''
        if self.pacman.invulnerable:

            if self.pacman.invulnerable_ticks == Pacman.ticks:   # Pacman.ticks (50) indicates Pacman barley became invulnerable
                self.update_enemy_states()
                self.pacman.boost_running_out()

            elif self.pacman.invulnerable_ticks == 0:  # Pacman runs out of his invulnerability so states are returned to normal
                self.update_enemy_states()
                self.pacman.normal_state()
            
            else:                                       # Pacman loses a tick normally when invulnerable
                self.pacman.boost_running_out()         

        
    def validate_upcoming_enemy(self, y, x) -> bool:
        ''' If Pacman is facing a direction, this function returns
            a boolean if there is an enemy directly in front of him,
            which results in a death if True. '''
        if self.within_bounds(x):
            if self.pacman.direction == 'Left':
                return type(self.Gamestate[y][x - 1]) == Enemy

            elif self.pacman.direction == 'Right':
                return type(self.Gamestate[y][x + 1]) == Enemy

            elif self.pacman.direction == 'Down':
                return type(self.Gamestate[y + 1][x]) == Enemy

            elif self.pacman.direction == 'Up':
                return type(self.Gamestate[y - 1][x]) == Enemy

    def validate_movement(self, previous_y, previous_x):
        '''
        Checks for the case that Pacman crosses to the other side via one side,
        which are when x == 14 and y == 0 or 27. If this is the case, the pacman
        object changes it's x and y with the crossed_boundary method. Otherwise the
        Gamestate is updated regularly.
        '''
    
        if self.edge_crossing(previous_y, previous_x):
            self.pacman.crossed_boundary()              # crossed_boundary changes Pacman's y, so must call pacman.y and pacman.x below
            self.Gamestate[self.pacman.y][self.pacman.x] = self.pacman

        else:
            self.pacman.contact( self.Gamestate[previous_y][previous_x] )

    def validate_enemy_movement(self, pacman_y, pacman_x):
        ''' Iterates through all the enemies on the board, determines their direction
            and then validates that direction checking if they have killed Pacman, and
            automatically updates enemy positions. '''
        for enemy in self.enemies:
            enemy.determineDirection(self, (enemy.x, enemy.y), pacman_y, pacman_x)
            self._validate_enemy_position(enemy, pacman_y, pacman_x)

    def _validate_enemy_position(self, enemy, pacman_y, pacman_x):
        ''' Checks if the position of the enemy is the same position as Pacman, if so then
            calls the function check_for_gameover(). Else it's just going to update the
            board with the enemy. '''
        
        if (enemy.y, enemy.x) == (pacman_y, pacman_x):
            self.check_for_gameover()
        else:
            self.restore_pickup(enemy)
            
            if type(self.Gamestate[enemy.y][enemy.x]) == Pickup:
                enemy.pickup_memory = self.Gamestate[enemy.y][enemy.x]

            self.Gamestate[enemy.y][enemy.x] = enemy
    
    # Individual Game Object Size Settings #
    def within_bounds(self, x) -> bool:
        return x != self.board_width() - 1 and x != 0

    def edge_crossing(self, y, x):
        ''' When Pacman is on the 15th row and has a x of 0 or 27,
            then he is at the specific edge of the board that allows
            crossing from one side to another, if so return True. '''
        return (y == 14 and x == 0) or (y == 14 and x == 27)
    
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
