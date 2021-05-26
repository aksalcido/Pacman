from PIL.ImageTk import PhotoImage
import os

class GameImage():

    def __init__(self):
        ''' Initializes a game image object that holds all the of the images for the game.
            The os library is used to get the current directory, and then iterates
            through all of the images inside the 'images' directory. This makes all of the
            images available from different directories. '''
        self.start_directory = os.getcwd()

        # Ran from src directory
        if self.start_directory.split('\\')[-1] == "src":
            self.image_directory = f'..\\static\\images'
        # Ran from Pacman directory
        else:
            self.image_directory = f'{self.start_directory}\\static\\images'

        self.game_images = dict()

        for image in os.listdir( self.image_directory ):
            self.game_images[ image[:-4] ] = PhotoImage(file= f'{self.image_directory}\\{image}')

    def return_image(self, image) -> PhotoImage:
        ''' Returns the image from the image_directory given the image argument. '''
        return self.game_images[image]

    
