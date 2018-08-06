from character import Character
from pickup import Pickup

class Pacman(Character):
    pacman = 9
    
    def __init__(self, x, y, images, speed = 1, direction = 'Left'):
        Character.__init__(self, x, y, speed, direction)
        self.score = 0
        self.lives = 3
        self.level = 1
        self.lastDirection = 'Left'
        self.nextDirection = None
        self.directionImage(images)

        # https://stackoverflow.com/questions/28518072/play-animations-in-gif-with-tkinter

    # Game Progression Functions #
    def updateScore(self, gameObj):
        ''' Updates Pacman's score when he obtains a pickup.
            Regular Pickup are worth 10, while the boost are worth 50.
            Enemies while in boost mode are worth 100. '''
        if type(gameObj) == Pickup:
            if gameObj.boost:
                self.score += 50
                self.invulnerability()
            else:
                self.score += 10
            
        elif type(gameObj) == Character:
            self.score += 100
    
    def levelUp(self, score, lives, level) -> None:
        self.score = score
        self.lives = lives
        self.level = level

    def invulnerability(self):
        pass

    # Direction Functions #
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

    # Display Functions #
    def displayScore(self) -> str:
        return f'Score: {self.score}'

    def displayLives(self) -> str:
        return f'Lives: {self.lives}'

    def displayLevel(self) -> str:
        return f'Level: {self.level}'
    
    def directionImage(self, images):
        if self.direction == 'Left':
            self._image = images.return_image('pacmanL')

        elif self.direction == 'Right':
            self._image = images.return_image('pacmanR')

        elif self.direction == 'Down':
            self._image = images.return_image('pacmanD')

        elif self.direction == 'Up':
            self._image = images.return_image('pacmanU')

