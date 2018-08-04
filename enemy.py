from character import Character

class Enemy(Character):
    inky   = 5
    blinky = 6
    pinky  = 7
    clyde  = 8
    
    def __init__(self, x, y, enemyType, images, speed = 1, direction = None):
        Character.__init__(self, x, y, images, speed, direction)
        self.enemyType = enemyType
        self.determineImage(enemyType)
        self.determineDirection(enemyType)

    def determineImage(self, enemyType):
        if enemyType == Enemy.inky:
            self._image = self.images.return_image('inky')

        elif enemyType == Enemy.blinky:
            self._image = self.images.return_image('blinky')

        elif enemyType == Enemy.pinky:
            self._image = self.images.return_image('pinky')

        elif enemyType == Enemy.clyde:
            self._image = self.images.return_image('clyde')
        
    
    def determineDirection(self, enemyType):
        pass
    
