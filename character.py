class Character():

    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self._image = None


    def change_speed(self):
        pass

    def change_direction(self, direction):
        self.direction = direction

    def change_coords(self):
        if self.direction == 'Up':
            self.y -= self.speed

        elif self.direction == 'Right':
            self.x += self.speed
            
        elif self.direction == 'Down':
            self.y += self.speed
            
        elif self.direction == 'Left':
            self.x -= self.speed

    