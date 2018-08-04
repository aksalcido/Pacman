from PIL.ImageTk import PhotoImage
import os

class GameImage():

    def __init__(self):
        self.start_directory = os.getcwd()
        self.image_directory = f'{self.start_directory}\\images'
        self.game_images = dict()
    
        for image in os.listdir( self.image_directory ):
            self.game_images[ image[:-4] ] = PhotoImage(file= f'{self.image_directory}\\{image}')

    def return_image(self, image):
        return self.game_images[image]

    
