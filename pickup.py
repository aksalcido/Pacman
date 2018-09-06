class Pickup():
    pickup = 1
    boostUp = 3
    
    def __init__(self, x, y, images, boost = False):
        ''' Initializes a Pickup object that basically functions as a representation on the
            board. There is no methods in the class, because it gets eaten by Pacman as the
            game progresses. Due to this, it requires x and y coordinates, an image, and the
            difference between a boost pick up or a normal one, where boost is False by default.'''
        self.x = x
        self.y = y
        self.images = images
        self.boost = boost # default = false since only 4 boost and much more food
        
        if self.boost:
            self._image = self.images.return_image('boost')
        else:
            self._image = self.images.return_image('pickup')
