class Character():

    def __init__(self, x, y, direction):
        ''' Initializes a character object with x and y coordinates and a direction.
            The character class is for Pacman and all the Enemies on the board. '''
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1
        self.start_location = x, y
        self.last_location = None
        self.invulnerable = False
        self._image = None
        
    def movement(self) -> None:
        ''' This function is what operates the movement for the character objects on
            the board. Coordinates are adjusted with each update depending on which
            direction the character is going. '''
        if self.direction == 'Up':
            self.y -= self.speed

        elif self.direction == 'Right':
            self.x += self.speed
            
        elif self.direction == 'Down':
            self.y += self.speed
            
        elif self.direction == 'Left':
            self.x -= self.speed

    def invulnerability(self) -> None:
        ''' Makes the invulnerable attribute the opposite of what it currently is.
            Called twice, when a boost is eaten, and then after certain amount of
            time has passed, it is called again to change back to default. '''
        self.invulnerable = not self.invulnerable

    def initial_position(self) -> None:
        ''' Changes the location to the initial spawn location. '''
        self.change_location(self.start_location[0], self.start_location[1])

    def change_direction(self, direction) -> None:
        ''' Makes the attribute direction equal to the direction argument given in the parameters. '''
        self.direction = direction
        
    def change_location(self, x, y) -> None:
        ''' Changes the location of the character's x and y values to the x and y arguments. '''
        self.x, self.y = x, y

    def return_location(self) -> tuple:
        ''' This function returns y first since the board is a 2D-List. '''
        return self.y, self.x
