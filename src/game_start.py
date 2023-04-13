import logging
import random

import numpy as numpy

from src.map import Map, Block
from src.player import Player

# logging

def start_game():
    game_over = False
    my_map = create_map()
    players = create_plaeyrs()
    for round in range(1, 10):
        if game_over is True or check_all_players_die(players):
            print("GAME OVER")
            break
        else: print(f"ROUND {round}!!!")
        create_flame_blocks(my_map, players)
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

def create_flame_blocks(my_map, players):
    flame_blocks = numpy.random.choice([1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 14], size=4, replace=False)
    for i in flame_blocks:
        key_in_flame = False
        player_in_flame = False
        print(f"{i}: {my_map.blocks[i].koord}")
        my_map.blocks[i].flame_block = True
        if my_map.blocks[i].key_block is True: key_in_flame = True
        for player in players:
            if player.position == i:
                player.life -= 1
                player_in_flame = True
                print(f"player {player.name} in fire.\n life: {player.life}")
                if player.life == 0:
                    player.die = True
        flame_block = my_map.blocks[i]
        my_map.add_flame(flame_block, key_in_flame, player_in_flame)
    show_map(my_map, "")

def create_players_move(players, my_map):
    for player in players:
        blocks = my_map.blocks
        my_map.add_player(blocks, blocks[0], player)
        my_map.add_bloks()
        show_map(my_map, "")
        player.power = 5 # магия)))
        while player.power > 0 and player.life > 0 and player.move_state is True and player.win is False:
            move(my_map, blocks, player, players)
        game_over = check_all_players_die(players)
        if player.win is True or game_over is True:
            game_over = True
            break
    return game_over

def check_all_players_die(players):
    players_die = 0
    for player in players:
        if player.die is True:
            players_die += 1
    if players_die == len(players):
        print("ALL DIE!!")
        return True
    return False

def show_map(my_map, simbol):
    for row in my_map.my_map:
        print(simbol.join(row))

def check_players_positions(players, player):
    for each_player in players:
        if player.position == each_player.position and player is not each_player:
            return each_player
    return False

def move(my_map, blocks, player, players):
    direction = input("нажмите w,a,s,d для движения, e - поднятия ключа, f - атаки: \n")
    if direction == "e" and blocks[player.position].key_block is True:
        player.have_key = True
        player.power -= 1
        blocks[player.position].key_block = False
        print(f"player {player.name} have key")
        my_map.delete_player(blocks, blocks[player.position], player)
        my_map.add_player(blocks, blocks[player.position], player)
        my_map.add_bloks()
        show_map(my_map, "")
    elif direction == "e" and blocks[player.position].key_block is False:
        print("No Key here")
    elif direction in blocks[player.position].valid_move:
        if blocks[player.position].key_block is True:
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.position])
        elif blocks[player.position].hart_block is True:
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_hart(my_map.blocks[player.position])
        else:
            block_have_player = check_players_positions(players, player)
            if block_have_player is not False:
                my_map.add_player(blocks, blocks[block_have_player.position], block_have_player)
            else: my_map.delete_player(blocks, blocks[player.position], player)

        player.last_position.append(player.position)
        next_num_block = blocks[player.position].valid_move[direction]
        for each_player in players:
            if next_num_block == each_player.position:
                chose = input(f"You wont to kill? {each_player.name}, if yes print 'y' else print 'n'")
                if chose == "y":
                    each_player.life -= 1
                    print(f"player {each_player.name} wos bin attack by player {player.name}\n"
                          f"player {each_player.name} life: {each_player.life}")
                    if each_player.life == 0:
                        print(f"player {each_player.name} wos bin kill by player {player.name}")
                        each_player.move_state = False
                        each_player.die = True
                        each_player.position = -1
                        # my_map.delete_player(blocks, blocks[player.position], player)
                    player.power -= 2
                elif chose == "n":
                    player.power -= 3
        player.position = next_num_block
        conditions(blocks, next_num_block, player, my_map, players)
        my_map.add_player(blocks, blocks[next_num_block], player)
        my_map.add_bloks()
        show_map(my_map, "")
    elif player.life > 0:
        print("wrong direction loose yor life")
        player.life -= 1
    else:
        print("die")
        player.die = True

def conditions(blocks, next_num_block, player, my_map, players):
    if blocks[next_num_block].prize_block is False:
        player.power -= 1
    if blocks[next_num_block].hart_block is True:
        player.life = 5
        print(f"yor life is {player.life}")
    if blocks[next_num_block].flame_block is True:
        player.life -= 1
        print(f"you lose 1 life, you have {player.life} life")
        blocks[next_num_block].flame_block = False
        if player.life == 0 and player.have_key is True:
            player.have_key = False
            player.die = True
            my_map.blocks[player.position].key_block = True
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.position])
            player.position = -1
        elif player.life == 0 and player.have_key is False:
            my_map.delete_player(blocks, blocks[player.position], player)
            player.die = True
            player.position = -1
    if player.position in player.last_position and blocks[player.last_position[-1]].prize_block is False:
        print(f"PLAYER {player.name} scary and die.")
        player.move_state = False
        player.life = 0
        print(f"player {player.name} life: {player.life}")
        player.die = True
        player.position = -1
        if player.have_key is True:
            player.have_key = False
            my_map.blocks[player.last_position[-1]].key_block = True
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.last_position[-1]])
        return player.move_state
    if blocks[next_num_block].end_block is True and player.have_key is True:
        print(f"PLAYER {player.name} WIN!")
        player.move_state = False
        player.win = True
        return player.move_state
    elif blocks[next_num_block].end_block is True and player.have_key is False:
        player.move_state = False
        player.life = 0
        player.die = True
        player.position = -1
        print(f"PLAYER {player.name} KILL! \n player {player.name} life: {player.life}")
        my_map.delete_player(blocks, blocks[player.position], player)
        return player.move_state
