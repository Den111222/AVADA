import json
import logging
import os
from pathlib import Path

from src.cheks.chek import check_players_positions
from src.convertation.convertation import convert_data_to_json
from src.moves.conditions import conditions

# Как переменную задал путь сохранения файлов сохранений игры.
# As a variable set the path of saving game save files.
directory = 'src/saves'

# Реализация ходов в игре игроками
# Realization of moves in the game by players
def move(my_map, blocks, player, players):
    directions = ["w", "a", "s", "d", "e", "f", "H", "S", "q"]
    direction = input("tap w,a,s,d for moove, e - take up key, f - atack,"
                      "H  - to hill, S - save game, q - quit: \n")
    # при выборе "е" происходит подьем ключа в блоке если он там есть, при этом power у
    # игрока отнимается
    # When selecting "e", the key in the block is lifted if it is there, and the player's
    # power is taken away.
    if direction == "e" and blocks[player.position].key_block is True:
        player.have_key = True
        player.power -= 1
        blocks[player.position].key_block = False
        logging.info(f"player {player.name} chose 'e' \n"
                     f"player {player.name} have key")
        my_map.delete_player(blocks, blocks[player.position], player)
        my_map.add_player(blocks, blocks[player.position], player)
        my_map.add_bloks()
        show_map(my_map, "")
    # Уведомление что ключа в данном блоке нет.
    # Notification that the key is not in this unit.
    elif direction == "e" and blocks[player.position].key_block is False:
        logging.info(f"player {player.name} chose 'e' \n"
                     f"No Key here")
    # Запуск сохранения игры в файл json. При этом есть возможность задать имя
    # файла сохронения игры.
    # Start saving the game to a json file. It is possible to set the name of the
    # game save file.
    elif direction == 'S':
        save_file_name = input(f"Input save file name: \n")
        save_file_name = Path(directory).joinpath(save_file_name)
        my_map_to_save, players_to_save = convert_data_to_json(my_map, players)
        save_data = {'my_map': my_map_to_save.__dict__,
                     'players': players_to_save
                     }
        with open(f'{save_file_name}.json', 'w') as write_file:
            json.dump(save_data, write_file)
            logging.info(f"The game is saved by file: {save_file_name}.json")
    elif direction == 'H':
        player.power -= 3
        player.life += 1
        my_map.add_player(blocks, blocks[player.position], player)
        my_map.add_bloks()
        show_map(my_map, "")
    # Проверка на валидность хода игрока. А также запуск соответствующих отрисовок при перемещении игрока по блокам.
    # Checking for validity of the player's move. And also launching of corresponding drawings when the player
    # moves on blocks.
    elif direction in blocks[player.position].valid_move:
        logging.info(f"player {player.name} chose {direction} \n")
        # Если игрок покинул клетку и не взял ключ
        # If a player has left the cage and has not picked up the key
        if blocks[player.position].key_block is True:
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.position])
        # Если игрок встал блок с сердцем
        # If a player got up a block with a heart
        elif blocks[player.position].hart_block is True:
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_hart(my_map.blocks[player.position])
        # Если игрок покинул клетку и в клетки остался другой игрок.
        # If a player has left the cage and another player remains in the cage.
        else:
            block_have_player = check_players_positions(players, player)
            if block_have_player is not False:
                my_map.add_player(blocks, blocks[block_have_player.position], block_have_player)
            else: my_map.delete_player(blocks, blocks[player.position], player)
        # Добавление последних позиций игрока, чтобы не смог сбежать.
        # Adding the player's last positions so he can't run away.
        player.last_position.append(player.position)
        next_num_block = blocks[player.position].valid_move[direction]
        # Реализация возможности атаки других игроков.
        # Implementing the ability to attack other players.
        for each_player in players:
            if next_num_block == each_player.position:
                chose = input(f"You wont to kill? {each_player.name}, if yes print 'y' else print 'n'")
                if chose == "y" and player.power > 2:
                    each_player.life -= 1
                    logging.info(f"player {player.name} chose 'y' to attack player {each_player.name}\n" 
                                 f"player {each_player.name} wos bin attack by player {player.name}\n"
                                 f"player {each_player.name} life: {each_player.life}")
                    if each_player.life == 0:
                        logging.info(f"player {each_player.name} wos bin kill by player {player.name}")
                        each_player.move_state = False
                        each_player.die = True
                        each_player.position = -1
                    player.power -= 1
                elif (chose == "y" and player.power <= 2) or (chose == "n" and player.power <= 2):
                    print("Not enough power to attack")
                    player.power = 1
                elif chose == "n" and player.power > 2:
                    player.power -= 2
        player.position = next_num_block
        # Запуск прочих условий, не связанных с перемещением.
        # Triggering other non-movement related conditions.
        conditions(blocks, next_num_block, player, my_map, players)
        my_map.add_player(blocks, blocks[next_num_block], player)
        my_map.add_bloks()
        show_map(my_map, "")

    # Должен быть выход, но в ТЗ об этом ничего не говориться.
    # There should be a way out, but the ToR doesn't say anything about it.
    elif direction == 'q':
        print("TOR doesn't have an exit clause, it's so lame!")

    # Если герой бьется о стену теряет 1 жизнь.
    # If the hero hits a wall he loses 1 life.
    elif direction in directions and player.life > 0 and direction not in blocks[player.position].valid_move:
        logging.info(f"player {player.name} chose {direction}"
                     f"it is wrong direction and loose 1 life")
        player.power -= 1
        player.life -= 1
        if player.life == 0:
            player.die = True
        my_map.add_player(blocks, blocks[player.position], player)
        my_map.add_bloks()
        show_map(my_map, "")

    # Если нажал что-то совсем не то, при выборе хода
    # If you press something completely wrong, when you select a move.
    elif direction not in directions:
        logging.info(f"wrong chose, input {directions}")
    # Все остальные случаи хода, хотя их быть не должно)))
    # All other cases of stroke, although there shouldn't be any.))))
    else:
        logging.info(f"die")
        player.die = True

def show_map(my_map, simbol):
    if (os.name == 'posix'):
        os.system('clear')
    # else screen will be cleared for windows
    else:
        os.system('cls')
    for row in my_map.my_map:
        print(simbol.join(row))