import tkinter as tk
from board import Board
from gameImage import GameImage
from pacman import Pacman
from enemy import Enemy
from pickup import Pickup
from wall import Wall

class Window():

    def __init__(self, master):
        '''
        Initializes a Window Object that is the GUI for Pacman. The Window updates
        the GUI accordingly to the progression of the game, by the use of the Board
        object attribute initialized here. '''
        self._master = master
        self._width = 1000
        self._height = 850
        self._images = GameImage()      # All images used for Pacman are stored as a GameImage() object

        # All Tkinter Settings Initialized #
        self._canvas = tk.Canvas(self._master, width = self._width, height = self._height, background="black")
        self._canvas.grid(row=0,column=0, sticky=tk.N)
        self._scoreLabel = tk.Label(self._master, text = '0', font = ('Arial', 20))
        self._scoreLabel.grid(row=1,column=0,sticky=tk.W)
        self._master.resizable(width=False, height=False)
        self._master.title('Pacman')

        # Arrow Keys Binded #
        self._bindingsEnabled( True )

        # Pacman Board Initialized #
        self.board = Board(self._width, self._height, self._images)
        self.board.new_level()          # Initializes a new level for Pacman
    
    def _draw_board(self) -> None:
        ''' Draws the board given the gameObjs in the board's set. '''
        total_height = self.board.square_height() # Approximately ~24
        total_width = self.board.square_width()   # Approximately ~36
        
        for gameObj in self.board.gameObjects:
            if type(gameObj) == Wall:
                self._canvas.create_rectangle(gameObj.x * total_width,
                                              gameObj.y * total_height,
                                              (gameObj.x * total_width / total_width + 1) * total_width,
                                              (gameObj.y * total_height / total_height + 1) * total_height,
                                              fill = 'blue', width = 0)
        
            elif type(gameObj) == Pickup or type(gameObj) == Pacman or type(gameObj) == Enemy:
                self._canvas.create_image( gameObj.x * total_width + (total_width / 2),
                                           gameObj.y * total_height + (total_height / 2), image = gameObj._image)


    def _drawInterface(self) -> None:
        self._scoreLabel['text'] = self.board.pacman.displayScore()
    
    def _draw_pacman(self): # not used yet
        self._canvas.move(self._pacman, 1, 0)

    def _updateDirections(self):
        if self.board.pacman.hasUpcomingDirection():
            if self.board.validatePath( self.board.pacman.nextDirection ):
                self.board.pacman.change_direction(self.board.pacman.nextDirection)
                self.board.pacman.nextDirection = None
                self.board.pacman.directionImage( self._images )
        
        if self.board.validatePath( self.board.pacman.direction ):
            self.board.pacman.change_coords()

    
    def _adjust_board(self):
        ''' Deletes the board and then redraws to prevent animation overlapping. '''
        self._canvas.delete(tk.ALL)
        self._draw_board()
        self._drawInterface()
    
    def pacmanDirection(self, event: tk.Event) -> None:
        ''' Function that allows the player to move Pacman. Directions have
            to be validated in order to avoid stopped movement. nextDirection
            and lastDirection allow smoother control of Pacman. '''
        self.board.pacman.change_direction(event.keysym)

        if self.board.validatePath( event.keysym ) == False:
            self.board.pacman.nextDirection = event.keysym
            self.board.pacman.direction = self.board.pacman.lastDirection

        else:
            self.board.pacman.directionImage( self._images )
            self.board.pacman.nextDirection = None

    def update(self):
        '''
        Updates the game consistently throughout the game. Also, updates the
        directions of the player, and the objects that are on the board as objects
        are removed from the board by the player.
        '''
        self._adjust_board()
        self._updateDirections()
        self.board._updateObjects()

        if self.board.level_complete():
            self.displayCompleted()
            self._canvas.after(5000, self.update)
        
        else:
            self._canvas.after(125, self.update)
    
    def displayCompleted(self):
        ''' This functions is to add a properly transition between the completed
            level and the loading screen. Mainly for visual purposes to appear nicer. '''
        self.board.pacman.direction = None
        self._bindingsEnabled(False)
        self._canvas.after(750, self.loadingScreen)
    
    def loadingScreen(self):
        self._canvas.delete(tk.ALL)
        self._canvas.create_image( self._width / 2, self._height / 2,
                                   image = self._images.return_image('loading_screen') )
        
        self._master.after(3500, self.levelAdvancement)

    def levelAdvancement(self):
        ''' Board loads up a new level once the previous level is completed. '''
        self.board.new_level()
        self._bindingsEnabled(True)

    def _bindingsEnabled(self, enabled: bool) -> None:
        if enabled:
            self._master.bind('<Left>', self.pacmanDirection)
            self._master.bind('<Right>', self.pacmanDirection)
            self._master.bind('<Up>', self.pacmanDirection)
            self._master.bind('<Down>', self.pacmanDirection)

        else:
            self._master.unbind('<Left>')
            self._master.unbind('<Right>')
            self._master.unbind('<Up>')
            self._master.unbind('<Down>')
    
    def run(self):
        self._master.after(100, self.update) # put again here to allow mainloop() to still occur and also call gameloop
        self._master.mainloop()

