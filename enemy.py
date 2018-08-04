from character import Character
from PIL.ImageTk import PhotoImage

class Enemy(Character):
    inky   = 5
    blinky = 6
    pinky  = 7
    clyde  = 8

    def __init__(self, x, y, enemyType, speed = 1, direction = None):
        Character.__init__(self, x, y, speed, direction)
        self.enemyType = enemyType
        self.determineImage(enemyType)
        self.determineDirection(enemyType)

    def determineImage(self, enemyType):
        if enemyType == Enemy.inky:
            self._image = PhotoImage(file='inky.png')

        elif enemyType == Enemy.blinky:
            self._image = PhotoImage(file='blinky.png')

        elif enemyType == Enemy.pinky:
            self._image = PhotoImage(file='pinky.png')

        elif enemyType == Enemy.clyde:
            self._image = PhotoImage(file='clyde.png')
        
    
    def determineDirection(self, enemyType):
        pass
    
