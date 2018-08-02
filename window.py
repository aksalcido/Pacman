import tkinter as tk
from board import Board
from pacman import Pacman
from pickup import Pickup
from wall import Wall

class Window():

    def __init__(self, master):
        self._master = master
        self._width = 1000
        self._height = 800
        self._border = 50       # Will be used for a border to display Score, Level, Lives, etc.
        
        self.board = Board(self._width, self._height, self._border) # board now takes window arguments
        self.board.new_level()
        
        self._canvas = tk.Canvas(master, width = self._width, height = self._height, background="black")
        self._canvas.pack()
        
        # Arrow Keys Binded
        self._master.bind('<Left>', self.pacmanDirection)
        self._master.bind('<Right>', self.pacmanDirection)
        self._master.bind('<Up>', self.pacmanDirection)
        self._master.bind('<Down>', self.pacmanDirection)
        
        self._master.resizable(width=False, height=False)
        
    def draw_board(self) -> None:
        ''' Draws the board given the gameObjs in the board's set. '''
        total_height = self.board.square_height() # 24.193548387096776
        total_width = self.board.square_width()   # 35.714285714285715
        
        for gameObj in self.board.gameObjects:
            if type(gameObj) == Wall:
                self._canvas.create_rectangle(gameObj.x * total_width,
                                              gameObj.y * total_height,
                                             (gameObj.x * total_width / total_width + 1) * total_width,
                                             (gameObj.y * total_height / total_height + 1) * total_height,
                                             fill = 'blue')
                
            elif type(gameObj) == Pickup:
                self._canvas.create_oval(gameObj.x * total_width  + (total_width * .45),
                                        gameObj.y  * total_height + (total_height * .45),
                                        gameObj.x  * total_width + (total_width * .55),
                                        gameObj.y  * total_height + (total_height * .55),
                                        fill = 'white')

            elif type(gameObj) == Pacman:
                self._canvas.create_oval(gameObj.x * total_width, gameObj.y * total_height,
                                        ( gameObj.x * total_width / total_width + 1 ) * total_width,
                                         ( gameObj.y * total_height / total_height + 1 ) * total_height,
                                         fill = 'yellow')


    def gameloop(self):
        self._master.after(500, self.gameloop) # delays before being called again
        self.update()                        # function that updates the board object
        
    def update(self):
        self._adjust_board()

        if self.board.validatePath():
            self.board.pacmanLocation.change_coords()
            
        self.board.updateObjects()
    
    def _adjust_board(self):
        ''' Deletes the board and then redraws to prevent animation overlapping. '''
        self._canvas.delete(tk.ALL)
        self.draw_board()
    
    def pacmanDirection(self, event: tk.Event) -> None:
        ''' Will eventually change this to return the event and it leads to Pacman's direction. '''
        self.board.pacmanLocation.change_direction(event.keysym)
    
    def run(self):
        self._master.after(100, self.gameloop) # put again here to allow mainloop() to still occur and also call gameloop
        self._master.mainloop()
