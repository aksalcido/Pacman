from character import Character

class Enemy(Character):
    
    def __init__(self, x, y, speed = 1, color = None):
        Character.__init__(self, x, y, speed, color)
