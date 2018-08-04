import tkinter as tk
from board import Board
from pacman import Pacman
from enemy import Enemy
from pickup import Pickup
from wall import Wall

class Window():

    def __init__(self, master):
        self._master = master
        self._width = 1000
        self._height = 750
        self._border = 50       # Will be used for a border to display Score, Level, Lives, etc.
        
        self.board = Board(self._width, self._height, self._border) # board now takes window arguments
        self.board.new_level()
        
        self._canvas = tk.Canvas(self._master, width = self._width, height = self._height, background="black")
        self._canvas.grid(row=0,column=0, sticky=tk.N)
        self._scoreLabel = tk.Label(self._master, text = '0', font = ('Arial', 20))
        self._scoreLabel.grid(row=1,column=0,sticky=tk.W)
    
        self._tkPacman = None # Not used
        # Arrow Keys Binded
        self._master.bind('<Left>', self.pacmanDirection)
        self._master.bind('<Right>', self.pacmanDirection)
        self._master.bind('<Up>', self.pacmanDirection)
        self._master.bind('<Down>', self.pacmanDirection)
        
        self._master.resizable(width=False, height=False)
        self._master.title('Pacman')
        
    def draw_board(self) -> None:
        ''' Draws the board given the gameObjs in the board's set. '''
        total_height = self.board.square_height() # 24.193548387096776
        total_width = self.board.square_width()   # 35.714285714285715
        
        for gameObj in self.board.gameObjects:
            if type(gameObj) == Wall:
                if gameObj._image == None:
                    self._canvas.create_rectangle(gameObj.x * total_width,
                                                  gameObj.y * total_height,
                                                 (gameObj.x * total_width / total_width + 1) * total_width,
                                                 (gameObj.y * total_height / total_height + 1) * total_height,
                                                 fill = 'blue', width = 0)

                else: # testing else
                    self._canvas.create_image( gameObj.x * total_width, gameObj.y * total_height, image = gameObj._image)
        
            elif type(gameObj) == Pickup or type(gameObj) == Pacman or type(gameObj) == Enemy:
                self._canvas.create_image( gameObj.x * total_width + (total_width / 2),
                                           gameObj.y * total_height + (total_height / 2), image = gameObj._image)


    def _drawInterface(self) -> None:
        self._scoreLabel['text'] = self.board.pacman.displayScore()
    
    def _draw_pacman(self): # not used yet
        self._canvas.move(self._pacman, 1, 0)

    def gameloop(self):
        self._master.after(125, self.gameloop) # delays before being called again
        self.update()                        # function that updates the board object
        
    def update(self):
        self._adjust_board()
        self._updateDirections()
        self.board._updateObjects()

    def _updateDirections(self):
        if self.board.pacman.hasUpcomingDirection():
            if self.board.validatePath( self.board.pacman.nextDirection ):
                self.board.pacman.change_direction(self.board.pacman.nextDirection)
                self.board.pacman.nextDirection = None
                self.board.pacman.directionImage()
        
        if self.board.validatePath( self.board.pacman.direction ):
            self.board.pacman.change_coords()

        
    def _adjust_board(self):
        ''' Deletes the board and then redraws to prevent animation overlapping. '''
        self._canvas.delete(tk.ALL)
        self.draw_board()
        self._drawInterface()


    def pacmanDirection(self, event: tk.Event) -> None:
        ''' Will eventually change this to return the event and it leads to Pacman's direction. '''
        self.board.pacman.change_direction(event.keysym)

        if self.board.validatePath( event.keysym ) == False:
            self.board.pacman.nextDirection = event.keysym
            self.board.pacman.direction = self.board.pacman.lastDirection

        else:
            self.board.pacman.directionImage()
            self.board.pacman.nextDirection = None
            
    def run(self):
        self._master.after(100, self.gameloop) # put again here to allow mainloop() to still occur and also call gameloop
        self._master.mainloop()

