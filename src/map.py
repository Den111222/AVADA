class Block():
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.block = []
        self.start_block = False
        self.number = 0
        self.prize_block = False

    def generate_maze(self):
        for i in range(1, self.height+1):
            self.block.append([])
            for j in range(1, self.width+1):
                self.block[i-1].append(' ')
        return self.block


class Map():
    def __init__(self, width=49, height=25):
        self.width = width
        self.height = height
        self.map = []

    def generate(self):
        for i in range(1, self.height+1):
            self.map.append([])
            for j in range(1, self.width+1):
                self.map[i-1].append('x')
        return map

    def add_bloks(self):
        koord = [[1, 1], [7, 1], [7, 7], [13, 7], [13, 13], [19, 7], [19, 1], [25, 1], [31, 1], [31, 7], [37, 7],
                 [37, 13], [37, 19], [31, 19], [43, 19]]
        for number in range(0, len(koord)):  #16 блоков в лабиринте
            block = Block()
            block.generate_maze()
            block.number = number
            start_horizontal, start_vertikal = koord[number]
            iter = len(block.block)
            self.add_block(start_horizontal=start_horizontal, start_vertikal=start_vertikal, iter=iter, block=block)

    def add_block(self, start_horizontal, start_vertikal, iter, block):
        for row in block.block:
            start = len(self.map) - iter
            iter -= 1
            iter_row = len(row)-1
            for i in range(start_horizontal, len(self.map[start-start_vertikal])):
                if iter_row < len(row) and iter_row != -1:
                    self.map[start-start_vertikal][i] = row[iter_row]
                    iter_row -= 1
