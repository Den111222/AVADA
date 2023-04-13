import random


class Block():
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.block = []
        self.start_block = False
        self.end_block = False
        self.number = 0
        self.prize_block = False
        self.flame_block = False
        self.hart_block = False
        self.key_block = False
        self.koord = []
        self.valid_move = []

    def generate(self):
        for i in range(1, self.height+1):
            self.block.append([])
            for j in range(1, self.width+1):
                self.block[i-1].append(' ')
        return self.block

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

class Map():
    def __init__(self, width=49, height=25):
        self.width = width
        self.height = height
        self.my_map = []
        self.blocks = []

    def generate(self):
        for i in range(1, self.height+1):
            self.my_map.append([])
            for j in range(1, self.width+1):
                self.my_map[i-1].append('x')
        return self.my_map

    def add_bloks(self):
        koord = [[1, 1], [7, 1], [7, 7], [13, 7], [13, 13], [19, 7],
                 [19, 1], [25, 1], [31, 1], [31, 7], [37, 7], [31, 13],
                 [25, 19], [31, 19], [37, 19], [43, 19]]
        if len(self.blocks) == 0:
            for number in range(0, len(koord)):  #16 блоков в лабиринте
                block = Block()
                block.generate()
                block.number = number
                if block.number == 0:
                    block.start_block = True
                    block.valid_move = {"d": 1}
                elif block.number == 4 or block.number == 10 or block.number == 12:
                    block.prize_block = True
                elif block.number == 15:
                    block.end_block = True
                if block.number == 1:
                    block.valid_move = {"a": 0, "w": 2}
                if block.number == 2:
                    block.valid_move = {"s": 1, "d": 3}
                if block.number == 3:
                    block.valid_move = {"a": 2, "w": 4, "d": 5}
                if block.number == 4:
                    block.valid_move = {"s": 3}
                    block.key_block = True
                if block.number == 5:
                    block.valid_move = {"a": 3, "s": 6}
                if block.number == 6:
                    block.valid_move = {"w": 5, "d": 7}
                if block.number == 7:
                    block.valid_move = {"a": 6, "d": 8}
                if block.number == 8:
                    block.valid_move = {"a": 7, "w": 9}
                if block.number == 9:
                    block.valid_move = {"s": 8, "w": 11, "d": 10}
                if block.number == 10:
                    block.valid_move = {"a": 9}
                    block.hart_block = True
                if block.number == 11:
                    block.valid_move = {"w": 13, "s": 9}
                if block.number == 12:
                    block.valid_move = {"d": 13}
                    block.hart_block = True
                if block.number == 13:
                    block.valid_move = {"a": 12, "s": 11, "d": 14}
                if block.number == 14:
                    block.valid_move = {"a": 13, "d": 15}

                start_horizontal, start_vertikal = koord[number]
                block.koord = [start_horizontal, start_vertikal]
                self.blocks.append(block)
                iter = len(block.block)
                self.add_block(start_horizontal=start_horizontal, start_vertikal=start_vertikal, iter=iter, block=block)
        else:
            for block in self.blocks:
                start_horizontal, start_vertikal = block.koord
                iter = len(block.block)
                self.add_block(start_horizontal=start_horizontal, start_vertikal=start_vertikal, iter=iter, block=block)

    def add_block(self, start_horizontal, start_vertikal, iter, block):
        for row in block.block:
            start = len(self.my_map) - iter
            iter -= 1
            iter_row = 0
            for i in range(start_horizontal, len(self.my_map[start - start_vertikal])):
                if iter_row < len(row):
                    self.my_map[start - start_vertikal][i] = row[iter_row]
                    iter_row += 1

    def add_player(self, blocks, block, player):
        if player.position == block.number:
            for row in range(0, len(block.block)):
                iter_player_index = 0
                for i in range(0, len(block.block[row])):
                    if row == 0 or row == len(player.player)+1: break
                    if i == 0:
                        block.block[row][i] = ' '
                        continue
                    if iter_player_index <= len(player.player[0])-1:
                        if i == 1 and row == len(block.block)-1: block.block[row][1] = str(player.life)
                        elif i == 3 and row == len(block.block)-1:
                            block.block[row][i] = str(player.power)
                        elif player.player[row-1][iter_player_index] == "N":
                            block.block[row][i] = str(player.name)
                        else: block.block[row][i] = player.player[row-1][iter_player_index]
                    else:
                        block.block[row][i] = ' '
                    iter_player_index += 1
        blocks[block.number] = block
        return blocks, block

    def delete_player(self, blocks, block, player):
        if player.position == block.number:
            for row in range(0, len(block.block)):
                iter_player_index = 0
                for i in range(0, len(block.block[row])):
                    if row == 0 or row == len(player.player) + 1: break
                    block.block[row][i] = ' '
                    iter_player_index += 1
        blocks[block.number] = block
        return blocks, block

    def add_flame(self, block, key=False, player=False):
        if player is True:
            flame_case = Plushki().player_in_flame
        elif key is True:
            flame_case = Plushki().key_in_flame
        else:
            flame_case = Plushki().flame
        for row in range(0, len(block.block)):
            iter_flame_index = 0
            for i in range(0, len(block.block[row])):
                # if row == 0 or row == len(Plushki().flame) + 1: break
                if row == 0 or row == len(flame_case)+1: break
                # block.block[row][i] = Plushki().flame[row - 1][iter_flame_index]
                # if iter_flame_index == len(Plushki().flame[0]) - 1:
                block.block[row][i] = flame_case[row-1][iter_flame_index]
                if iter_flame_index == len(flame_case[0])-1:
                    break
                iter_flame_index += 1
        return block

    def add_key(self, block):
        for row in range(0, len(block.block)):
            iter_key_index = 0
            for i in range(0, len(block.block[row])):
                if row == 0 or row == len(Plushki().key)+1: break
                block.block[row][i] = Plushki().key[row-1][iter_key_index]
                if iter_key_index == len(Plushki().key[0])-1:
                    break
                iter_key_index += 1
        return block

    def add_hart(self, block):
        for row in range(0, len(block.block)):
            iter_hart_index = 0
            for i in range(0, len(block.block[row])):
                if row == 0 or row == len(Plushki().hart)+1: break
                block.block[row][i] = Plushki().hart[row-1][iter_hart_index]
                if iter_hart_index == len(Plushki().hart[0])-1:
                    break
                iter_hart_index += 1
        return block

    # def add_hero_die(self, block):
    #     for row in range(0, len(block.block)):
    #         iter_key_index = 0
    #         for i in range(0, len(block.block[row])):
    #             if row == 0 or row == len(Plushki().key)+1: break
    #             block.block[row][i] = Plushki().key[row-1][iter_key_index]
    #             if iter_key_index == len(Plushki().key[0])-1:
    #                 break
    #             iter_key_index += 1
    #     return block