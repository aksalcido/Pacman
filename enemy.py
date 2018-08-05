from character import Character

class Enemy(Character):
    inky   = 5
    blinky = 6
    pinky  = 7
    clyde  = 8
    
    def __init__(self, x, y, enemyType, images, speed = 1, direction = None):
        Character.__init__(self, x, y, speed, direction)

        self.enemyType = enemyType
        self.determineImage(enemyType, images)
        self.determineDirection(enemyType)

    def determineImage(self, enemyType, images):
        if enemyType == Enemy.inky:
            self._image = images.return_image('inky')

        elif enemyType == Enemy.blinky:
            self._image = images.return_image('blinky')

        elif enemyType == Enemy.pinky:
            self._image = images.return_image('pinky')

        elif enemyType == Enemy.clyde:
            self._image = images.return_image('clyde')
        
    
    def determineDirection(self, enemyType):
        pass
    
