from PIL.ImageTk import PhotoImage


class Pickup():
    pickup = 1
    boostUp = 3
    
    def __init__(self, x, y, boost = False):
        self.x = x
        self.y = y
        self.boost = boost # default = false since only 4 boost and much more food

        if self.boost:
            self._image = PhotoImage(file='boost.png')
        else:
            self._image = PhotoImage(file='pickup.png')


## We can use this class to represent the Pickups like the little dots, and
## the invulnerability boost

## Thinking of making the list contain a ton of class objects (pacman, enemies, and the pickups) rather than
## just numbers, that way we can update the game by saying:

## if the direction of pacman is left
## if the object on the left of pacman, inside the board list's coordinates are the same as pacman's, then pacman will be inside that index of
## the board

## pacman.x == object.x --> pacman is inside that new index, once he leaves to the next one, maybe replaced with 'None'
## pacman.x == enemy.x --> pacman is dead
## etc, let me know what you think
