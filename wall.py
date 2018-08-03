from PIL.ImageTk import PhotoImage

class Wall:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.configureImage()

    def configureImage(self): # not working, just for testing atm
        ''' Will configure the image for the walla depending on the position. '''
        if self.x == 0 and self.y == 0:
            self._image = PhotoImage(file='cornerLeftEdge.png')

        elif self.x == 0 and self.y == 1:
            self._image = PhotoImage(file='horizontal.png')

        else:
            self._image = None
    
# I dunno if I really want to use this, but more of just to have
# an object place holder that represents a Wall

