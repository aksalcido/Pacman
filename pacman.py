from character import Character
from pickup import Pickup
from PIL.ImageTk import PhotoImage

class Pacman(Character):
    pacman = 9

    def __init__(self, x, y, speed = 1, direction = 'Left'):
        Character.__init__(self, x, y, speed, direction)
        self.score = 0
        self.lives = 3
        self.lastDirection = 'Left'
        self.nextDirection = None
        self._image = PhotoImage(file='pacmanL.png')

    def directionImage(self):
        if self.direction == 'Left':
            self._image = PhotoImage(file='pacmanL.png')

        elif self.direction == 'Right':
            self._image = PhotoImage(file='pacmanR.png')

        elif self.direction == 'Down':
            self._image = PhotoImage(file='pacmanD.png')

        elif self.direction == 'Up':
            self._image = PhotoImage(file='pacmanU.png')

        # https://stackoverflow.com/questions/28518072/play-animations-in-gif-with-tkinter

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

    def invulnerability(self):
        pass

    def displayScore(self) -> str:
        return f'Score: {self.score}'

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
            
