class Character():

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1
        self.start_location = x, y
        self.last_location = None
        self.invulnerable = False
        self._image = None
        
    def movement(self):
        if self.direction == 'Up':
            self.y -= self.speed

        elif self.direction == 'Right':
            self.x += self.speed
            
        elif self.direction == 'Down':
            self.y += self.speed
            
        elif self.direction == 'Left':
            self.x -= self.speed

    def invulnerability(self):
        self.invulnerable = not self.invulnerable

    def initial_position(self):
        self.change_location(self.start_location[0], self.start_location[1])
        
    def change_speed(self):
        pass

    def change_direction(self, direction):
        self.direction = direction
        
    def change_location(self, x, y):
        ''' Changes the location of the character's x and y values to the x and y arguments. '''
        self.x, self.y = x, y

    def return_location(self):
        ''' This function returns y first since the board is a 2D-List. '''
        return self.y, self.x
