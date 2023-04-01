class Player():
    def __init__(self):
        self.life = 5
        self.player = [[" ", "o", " "],
                       ["/", "|", "\\"],
                       ["/", " ", "\\"]]
        self.power = 5

player = Player()
for row in player.player:
    print("".join(row))
