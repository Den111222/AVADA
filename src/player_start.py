from src.map import Map
from src.player import Player

def start_game():
    input(f"Enter players number: \n")

    my_map = Map()
    my_map.generate()
    my_map.add_bloks()

    player = Player()
    blocks = my_map.blocks
    my_map.add_player(blocks, blocks[0], player)
    my_map.add_bloks()
    show_map(my_map, "")
    while player.power > 0:
        move(my_map, blocks, player)

def show_map(my_map, simbol):
    for row in my_map.my_map:
        print(simbol.join(row))

def move(my_map, blocks, player):
    direction = input("нажите w,a,s,d для движения: \n")
    if direction in blocks[player.position].valid_move:
        my_map.delete_player(blocks, blocks[player.position], player)
        next_num_block = blocks[player.position].valid_move[direction]
        player.position = next_num_block
        my_map.add_player(blocks, blocks[next_num_block], player)
        my_map.add_bloks()
        if blocks[next_num_block].prize_block is False:
            player.power -= 1
        show_map(my_map, "")
    else:
        print("die")