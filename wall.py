class Wall:
    wall = 0
    
    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.images = images
        self.configureImage()

    def configureImage(self): # not working, just for testing atm
        ''' Will configure the image for the walla depending on the position. '''
        if self.x == 0 and self.y == 0:
            self._image = self.images.return_image('cornerLeftEdge')

        elif self.x == 0 and self.y == 1:
            self._image = self.images.return_image('horizontal')

        else:
            self._image = None
    
# I dunno if I really want to use this, but more of just to have
# an object place holder that represents a Wall
