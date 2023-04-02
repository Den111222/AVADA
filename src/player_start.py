import random

import numpy as numpy

from src.map import Map, Block
from src.player import Player


def start_game():
    game_over = False
    my_map = create_map()
    players = create_plaeyrs()
    for round in range(1, 3):
        if game_over is True:
            break
        create_flame_blocks(my_map)
        game_over = create_players_move(players, my_map)

def create_map():
    my_map = Map()
    my_map.generate()
    my_map.add_bloks()
    my_map.add_key(my_map.blocks[4])
    my_map.add_hart(my_map.blocks[10])
    my_map.add_hart(my_map.blocks[12])
    return my_map

def create_plaeyrs():
    players = []
    num_players = int(input(f"Enter players number: \n"))
    for i in range(0, num_players):
        player = Player()
        player.name = input(f"Enter {i} player name: \n")
        players.append(player)
    return players

def create_flame_blocks(my_map):
    flame_blocks = numpy.random.choice([1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 14], size=4, replace=False)
    for i in flame_blocks:
        flame_block = my_map.blocks[i]
        my_map.add_flame(flame_block)
    show_map(my_map, "")

def create_players_move(players, my_map):
    for player in players:
        blocks = my_map.blocks
        my_map.add_player(blocks, blocks[0], player)
        my_map.add_bloks()
        show_map(my_map, "")
        while player.power > 0 and player.life > 0 and player.move_state is True and player.win is False:
            move(my_map, blocks, player)
        if player.win is True:
            game_over = True
            break
    return game_over

def show_map(my_map, simbol):
    for row in my_map.my_map:
        print(simbol.join(row))

def move(my_map, blocks, player):
    direction = input("нажмите w,a,s,d для движения, e - поднятия ключа, f - атаки: \n")
    if direction == "e" and blocks[player.position].key_block is True:
        player.have_key = True
        player.power -= 1
        blocks[player.position].key_block = False
        print(f"player {player.name} have key")
    elif direction in blocks[player.position].valid_move:
        if blocks[player.position].key_block is True:
            my_map.add_key(my_map.blocks[player.position])
        else:
            my_map.delete_player(blocks, blocks[player.position], player)
        player.last_position.append(player.position)
        next_num_block = blocks[player.position].valid_move[direction]
        player.position = next_num_block
        my_map.add_player(blocks, blocks[next_num_block], player)
        my_map.add_bloks()
        conditions(blocks, next_num_block, player, my_map)
        show_map(my_map, "")
    elif player.life > 0:
        print("loose yor life")
        player.life -= 1
    else:
        print("die")

def conditions(blocks, next_num_block, player, my_map):
    if blocks[next_num_block].prize_block is False:
        player.power -= 1
    if blocks[next_num_block].hart_block is True:
        player.life = 5
        print(f"yor life is {player.life}")
    if blocks[next_num_block].flame_block is True:
        player.life -= 1
        print(f"you lose 1 life, you have {player.life} life")
    if player.position in player.last_position and blocks[player.last_position[-1]].prize_block is False:
        print(f"PLAYER {player.name} scary and die")
        player.move_state = False
        player.life = 0
        if player.have_key is True:
            player.have_key = False
            my_map.blocks[player.last_position[-1]].key_block = True
            my_map.add_key(my_map.blocks[player.last_position[-1]])
            my_map.delete_player(blocks, blocks[player.position], player)
        return player.move_state
    if blocks[next_num_block].end_block is True and player.have_key is True:
        print(f"PLAYER {player.name} WIN!")
        player.move_state = False
        player.win = True
        return player.move_state
    elif blocks[next_num_block].end_block is True and player.have_key is False:
        player.move_state = False
        player.life = 0
        print(f"PLAYER {player.name} KILL!")
        return player.move_state