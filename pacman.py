from character import Character

class Pacman(Character):

    def __init__(self, x, y, speed = 1, color = "Yellow", direction = 'Left'):
        Character.__init__(self, x, y, speed, color, direction)
        self.score = 0
        self.lives = 3
