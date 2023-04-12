class Player():
    def __init__(self):
        self.name = ''
        self.life = 5
        self.power = 5
        self.position = 0
        self.last_position = []
        self.move_state = True
        self.have_key = False
        self.win = False
        self.die = False
        self.player = [[" ", "o", " "],
                       ["/", "|", "\\"],
                       ["/", " ", "\\"],
                       ["L", " ", "P"]]
