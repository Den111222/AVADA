class Player():
    def __init__(self):
        self.life = 5
        self.player = [[" ", "o", " "],
                       ["/", "|", "\\"],
                       ["/", " ", "\\"]]
        self.power = 5
        self.position = 0
        self.last_position = ""


# player = Player()
# for row in player.player:
#     print("".join(row))
