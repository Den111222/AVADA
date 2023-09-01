import json

# Это класс необходим для создания условного лабиринта и задания возможности блочной отрисовки.
# This class is needed to create a conditional maze and set the possibility of block drawing.
class Block():
    def __init__(self, width=5, height=5, block_schema=[], start_block=False, end_block=False,
                 number=0, prize_block = False, flame_block=False, hart_block=False,
                 key_block=False, koord=[], valid_move=[]):
        self.width = width
        self.height = height
        self.block_schema = self.generate()
        self.start_block = start_block
        self.end_block = end_block
        self.number = number
        self.prize_block = prize_block
        self.flame_block = flame_block
        self.hart_block = hart_block
        self.key_block = key_block
        self.koord = koord
        self.valid_move = valid_move

    # Создание изначально пустого блока, для дальнейшего управления.
    # Creating an initially empty block, for further management.
    def generate(self):
        block_schema = []
        for i in range(1, self.height+1):
            block_schema.append([])
            for j in range(1, self.width+1):
                block_schema[i-1].append(' ')
        return block_schema

    # Конвертация данных из json файла в объект класса.
    # Convert data from a json file to a class object.
    @classmethod
    def convert_from_json(cls, json_str):
        json_str = json.dumps(json_str)
        json_dict = json.loads(json_str)
        klass = cls(**json_dict)
        if klass.__class__ is Block:
            klass.block_schema = json_dict['block_schema']
        return klass

# Этот класс для отрисовки плюшек, в виде ключа, огня, ключа в огне и игрока в огне
# This class is for rendering plushies, in the form of key, fire, key on fire and
# player on fire
class Plushki():
    def __init__(self):
        self.key = [[" ", " ", " "],
                    ["O", "T", "T"],
                    [" ", " ", " "]]
        self.hart = [[" ", " ", " ", " ", " "],
                    ["h", "a", "r", "t", " "],
                    [" ", " ", " ", " ", " "]]
        self.flame = [["|", "\\", "/", "\\", " "],
                      ["|", " ", " ", " ", "|"],
                      ["|", "_", "_", "_", "|"]]
        self.key_in_flame = [["|", "\\", "/", "\\", " "],
                      ["|", "O", "T", "T", "|"],
                      ["|", "_", "_", "_", "|"]]
        self.player_in_flame = [["|", "\\", "/", "\\", " "],
                      ["|", " ", "o", " ", "|"],
                      ["|", "_", "_", "_", "|"]]

# Этот класс основной карты, на которой происходит вся отрисовка игры.
# This class is the main map class on which all of the game's rendering takes place.
class Map():
    def __init__(self, width=49, height=25, my_map=[], blocks=[]):
        self.width = width
        self.height = height
        self.my_map = my_map
        self.blocks = blocks

    # Прорисовка заднего фона карты
    # Drawing the background of the map
    def generate(self):
        for i in range(1, self.height+1):
            self.my_map.append([])
            for j in range(1, self.width+1):
                self.my_map[i-1].append('x')
        return self.my_map

    # Добавление блоков в лабиринт, поскольку в каждом блоке должен находится игрок
    # Adding blocks to the maze, as each block must contain a player
    def add_bloks(self):
        # Добавление координат блоков вручную, в задании был задан лабиринт
        # Adding block coordinates manually, a maze was specified in the task
        koord = [[1, 1], [7, 1], [7, 7], [13, 7], [13, 13], [19, 7],
                 [19, 1], [25, 1], [31, 1], [31, 7], [37, 7], [31, 13],
                 [25, 19], [31, 19], [37, 19], [43, 19]]
        # Добавление условия при создании лабиринта изначально, если лабиринт создан, то
        # перезагружаются уже созданные блоки. Каждому блоку задаются допустимые пределы хода,
        # а также атрибуты плюшек, в виде сердца, ключа и т.д.
        # Adding a condition when the maze is initially created, if the maze is created, the
        # already created blocks are reloaded. Each block is given allowable move limits, as
        # well as attributes of plushies, in the form of heart, key, etc.
        prize_blocks = [4, 10, 12]
        if len(self.blocks) == 0:
            for number in range(0, len(koord)):
                block_obj = Block(number=number)
                if number == 0:
                    block_obj.start_block = True
                    block_obj.valid_move = {"d": 1}
                elif number in prize_blocks:
                    block_obj.prize_block = True
                elif number == 15:
                    block_obj.end_block = True
                if number == 1:
                    block_obj.valid_move = {"a": 0, "w": 2}
                if number == 2:
                    block_obj.valid_move = {"s": 1, "d": 3}
                if number == 3:
                    block_obj.valid_move = {"a": 2, "w": 4, "d": 5}
                if number == 4:
                    block_obj.valid_move = {"s": 3}
                    block_obj.key_block = True
                if number == 5:
                    block_obj.valid_move = {"a": 3, "s": 6}
                if number == 6:
                    block_obj.valid_move = {"w": 5, "d": 7}
                if number == 7:
                    block_obj.valid_move = {"a": 6, "d": 8}
                if number == 8:
                    block_obj.valid_move = {"a": 7, "w": 9}
                if number == 9:
                    block_obj.valid_move = {"s": 8, "w": 11, "d": 10}
                if number == 10:
                    block_obj.valid_move = {"a": 9}
                    block_obj.hart_block = True
                if number == 11:
                    block_obj.valid_move = {"w": 13, "s": 9}
                if number == 12:
                    block_obj.valid_move = {"d": 13}
                    block_obj.hart_block = True
                if number == 13:
                    block_obj.valid_move = {"a": 12, "s": 11, "d": 14}
                if number == 14:
                    block_obj.valid_move = {"a": 13, "d": 15}

                start_horizontal, start_vertikal = koord[number]
                block_obj.koord = [start_horizontal, start_vertikal]
                self.blocks.append(block_obj)
                iter = len(block_obj.block_schema)
                self.add_block(start_horizontal=start_horizontal, start_vertikal=start_vertikal, iter=iter, block_obj=block_obj)
        else:
            for block_obj in self.blocks:
                start_horizontal, start_vertikal = block_obj.koord
                iter = len(block_obj.block_schema)
                self.add_block(start_horizontal=start_horizontal, start_vertikal=start_vertikal, iter=iter, block_obj=block_obj)

    # Отрисовка каждого блока на карте.
    # Drawing each block on the map.
    def add_block(self, start_horizontal, start_vertikal, iter, block_obj):
        for row in block_obj.block_schema:
            start = len(self.my_map) - iter
            iter -= 1
            iter_row = 0
            for i in range(start_horizontal, len(self.my_map[start - start_vertikal])):
                if iter_row < len(row):
                    self.my_map[start - start_vertikal][i] = row[iter_row]
                    iter_row += 1

    # Отрисовка игрока на карте при перемещении по блокам.
    # The rendering of the player on the map when moving through blocks.
    def add_player(self, blocks, block, player):
        if player.position == block.number:
            for row in range(0, len(block.block_schema)):
                iter_player_index = 0
                for i in range(0, len(block.block_schema[row])):
                    if row == 0 or row == len(player.player)+1: break
                    if i == 0:
                        block.block_schema[row][i] = ' '
                        continue
                    if iter_player_index <= len(player.player[0])-1:
                        if i == 1 and row == len(block.block_schema)-1: block.block_schema[row][1] = str(player.life)
                        elif i == 3 and row == len(block.block_schema)-1:
                            block.block_schema[row][i] = str(player.power)
                        elif player.player[row-1][iter_player_index] == "N":
                            block.block_schema[row][i] = str(player.name)
                        else: block.block_schema[row][i] = player.player[row-1][iter_player_index]
                    else:
                        block.block_schema[row][i] = ' '
                    iter_player_index += 1
        blocks[block.number] = block
        return blocks, block

    # Отрисовка пустого блока на карте, когда игрок покинул блок.
    # Draws an empty block on the map when a player has left the block.
    def delete_player(self, blocks, block, player):
        if player.position == block.number:
            for row in range(0, len(block.block_schema)):
                iter_player_index = 0
                for i in range(0, len(block.block_schema[row])):
                    if row == 0 or row == len(player.player) + 1: break
                    block.block_schema[row][i] = ' '
                    iter_player_index += 1
        blocks[block.number] = block
        return blocks, block

    # Отрисовка огня в блоке, на карте.
    # Drawing of fire in a block, on a map.
    def add_flame(self, block, key=False, player=False):
        if player is True:
            flame_case = Plushki().player_in_flame
        elif key is True:
            flame_case = Plushki().key_in_flame
        else:
            flame_case = Plushki().flame
        for row in range(0, len(block.block_schema)):
            iter_flame_index = 0
            for i in range(0, len(block.block_schema[row])):
                if row == 0 or row == len(flame_case)+1: break
                block.block_schema[row][i] = flame_case[row-1][iter_flame_index]
                if iter_flame_index == len(flame_case[0])-1:
                    break
                iter_flame_index += 1
        return block

    # Отрисовка ключа в блоке, на карте.
    # Drawing of the key in the block, on the map.
    def add_key(self, block):
        for row in range(0, len(block.block_schema)):
            iter_key_index = 0
            for i in range(0, len(block.block_schema[row])):
                if row == 0 or row == len(Plushki().key)+1: break
                block.block_schema[row][i] = Plushki().key[row-1][iter_key_index]
                if iter_key_index == len(Plushki().key[0])-1:
                    break
                iter_key_index += 1
        return block

    # Отрисовка сердца в блоке, на карте.
    # Drawing a heart in a block, on a card.
    def add_hart(self, block):
        for row in range(0, len(block.block_schema)):
            iter_hart_index = 0
            for i in range(0, len(block.block_schema[row])):
                if row == 0 or row == len(Plushki().hart)+1: break
                block.block_schema[row][i] = Plushki().hart[row-1][iter_hart_index]
                if iter_hart_index == len(Plushki().hart[0])-1:
                    break
                iter_hart_index += 1
        return block

    # Конвертация данных из json файла в объект класса.
    # Convert data from a json file to a class object.
    @classmethod
    def convert_from_json(cls, json_str):
        json_str = json.dumps(json_str)
        json_dict = json.loads(json_str)
        return cls(**json_dict)