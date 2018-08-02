from character import Character

class Pacman(Character):

    def __init__(self, x, y, speed = 1, color = "Yellow", direction = 'Left'):
        Character.__init__(self, x, y, speed, color, direction)
        self.score = 0
        self.lives = 3
        self.lastDirection = 'Left'
        self.nextDirection = None

    def increaseScore():
        score += 10

    def displayScore():
        return score

    def change_direction(self, direction):
        self.lastDirection = self.direction
        self.direction = direction
    
    def hasUpcomingDirection(self):
        return self.nextDirection is not None
        
    def crossedBoundary(self):
        if self.direction == 'Left':
            self.x = 27
            self.y = 14

        else:
            self.y = 14
            self.x = 0
            
