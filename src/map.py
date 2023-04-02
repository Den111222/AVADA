class Block():
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.block = []
        self.start_block = False
        self.end_block = False
        self.number = 0
        self.prize_block = False
        self.koord = []
        self.valid_move = []

    def generate(self):
        for i in range(1, self.height+1):
            self.block.append([])
            for j in range(1, self.width+1):
                self.block[i-1].append(' ')
        return self.block


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
                 [25, 19], [37, 19], [31, 19], [43, 19]]
        if len(self.blocks) == 0:
            for number in range(0, len(koord)):  #16 блоков в лабиринте
                block = Block()
                block.generate()
                block.number = number
                if block.number == 0:
                    block.start_block = True
                    block.valid_move = {"d": 1}
                elif block.number == 4 or block.number == 11 or block.number == 13:
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
                if block.number == 5:
                    block.valid_move = {"a": 3, "s": 6}
                if block.number == 6:
                    block.valid_move = {"w": 5, "d": 7}
                if block.number == 7:
                    block.valid_move = {"a": 6, "d": 8}
                if block.number == 8:
                    block.valid_move = {"a": 7, "w": 9}
                if block.number == 9:
                    block.valid_move = {"s": 8, "w": 10, "d": 11}
                if block.number == 10:
                    block.valid_move = {"w": 12, "s": 9}
                if block.number == 11:
                    block.valid_move = {"a": 9}
                if block.number == 12:
                    block.valid_move = {"a": 13, "s": 10, "d": 14}
                if block.number == 13:
                    block.valid_move = {"d": 12}
                if block.number == 14:
                    block.valid_move = {"a": 12, "d": 15}

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
                    if i == 0: continue
                    block.block[row][i] = player.player[row-1][iter_player_index]
                    if iter_player_index == 2:
                        break
                    iter_player_index += 1
        blocks[block.number] = block
        return blocks, block

    def delete_player(self, blocks, block, player):
        if player.position == block.number:
            for row in range(0, len(block.block)):
                iter_player_index = 0
                for i in range(0, len(block.block[row])):
                    if row == 0 or row == len(player.player) + 1: break
                    if i == 0: continue
                    block.block[row][i] = ' '
                    if iter_player_index == 2:
                        break
                    iter_player_index += 1
        blocks[block.number] = block
        return blocks, block
