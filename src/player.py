import json

#Это класс игрока
class Player():
    def __init__(self, name = ' ', life = 5, power = 5, position = 0,
                 last_position = [], move_state = True, have_key = False,
                 win = False, die = False, player = [["N", "o", " "],
                                                     ["/", "|", "\\"],
                                                     ["/", " ", "\\"],
                                                     ["L", " ", "P"]]):
        self.name = name
        self.life = life
        self.power = power
        self.position = position
        self.last_position = last_position
        self.move_state = move_state
        self.have_key = have_key
        self.win = win
        self.die = die
        self.player = player

    # Это метод конвертации данных из файла сохранения.
    @classmethod
    def convert_from_json(cls, json_str):
        json_str = json.dumps(json_str)
        json_dict = json.loads(json_str)
        return cls(**json_dict)
