from character import Character
from enemy import Enemy
from pickup import Pickup

class Pacman(Character):
    pacman = 9
    ticks = 50
    
    def __init__(self, x, y, images, speed = 1, direction = 'Left'):
        Character.__init__(self, x, y, speed, direction)
        self.score, self.lives, self.level = 0, 3, 1
        self.last_direction, self.next_direction = 'Left', None
        self.is_respawning = False
        self.direction_image(images)

        self.invulnerable_ticks = Pacman.ticks
        # https://stackoverflow.com/questions/28518072/play-animations-in-gif-with-tkinter

    def restart_level(self):
        ''' On death, original values are restored. '''
        self.initial_position()
        self.change_direction('Left')
        self.next_direction = None
        self.is_respawning = True
    
    # Game Progression Functions #
    def contact(self, gameObj):
        ''' Updates Pacman's score when he comes into contact with another
            game object, but also handles the two special cases if it's a
            boost pickup, and if it's an enemy. '''

        if type(gameObj) == Pickup:
            if gameObj.boost:
                self.score += 50
                self.boost_picked_up()
        
            else:
                self.score += 10

        # bottom half is never happening anymore #
        elif type(gameObj) == Enemy:
            if self.invulnerable:
                self.score += 100

            else:
                self.death = True
    
    def level_up(self, score, lives, level) -> None:
        self.score, self.lives, self.level = score, lives, level

    def respawn(self, images):
        self.restart_level()
        self.direction_image( images )
        self.death = False

    def lose_life(self):
        self.lives -= 1
        
    def out_of_lives(self):
        return self.lives == 0

    def boost_picked_up(self):
        ''' This function checks if Pacman is invulnerable when he picks up
            a boost. If he is then the counter is refreshed and he remains
            invulnerable for a longer time. Otherwise, he becomes invulnerable
            if he wasn't previously. '''
        if not self.invulnerable:
            self.invulnerability()
        else:
            self.invulnerable_ticks = Pacman.ticks - 1
    
    def boost_running_out(self):
        self.invulnerable_ticks -= 1
    
    def normal_state(self):
        self.invulnerable_ticks = Pacman.ticks
        self.invulnerability()
        
    # Direction Functions #
    def change_direction(self, direction):
        self.last_direction = self.direction
        self.direction = direction
    
    def has_upcoming_direction(self):
        return self.next_direction is not None
        
    def crossed_boundary(self):
        if self.direction == 'Left':
            self.change_location(27, 14)
        else:
            self.change_location(0, 14)

    # Display Functions #
    def display_score(self) -> str:
        return f'Score: {self.score}'

    def display_lives(self) -> str:
        return f'Lives: {self.lives}'

    def display_level(self) -> str:
        return f'Level: {self.level}'
    
    def direction_image(self, images):
        if self.direction == 'Left':
            self._image = images.return_image('pacmanL')

        elif self.direction == 'Right':
            self._image = images.return_image('pacmanR')

        elif self.direction == 'Down':
            self._image = images.return_image('pacmanD')

        elif self.direction == 'Up':
            self._image = images.return_image('pacmanU')

