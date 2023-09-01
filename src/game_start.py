import json
import logging
import os
from pathlib import Path
import numpy as numpy
from src.map import Map, Block
from src.player import Player

# Поскольку в ТЗ было сказано выводить в консоль, то оставил эту строку, но это только мешает игре.
#Since the ToR said to output to the console, I left this line, but it only interferes with the game.
# logging.basicConfig(level=logging.INFO, filemode="w",
#                     format="%(asctime)s %(levelname)s %(message)s")

# Сделал сохранение логов в файл, для более удобного их анализа.
#I made saving logs to a file for easier analysis.
logging.basicConfig(level=logging.INFO, filename="src/py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# Это оставил как подсказку, для себя.
# I left that as a clue, for myself.
"""
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")
"""

# Как переменную задал путь сохранения файлов сохранений игры.
# As a variable set the path of saving game save files.
directory = 'src/saves'

# Старт игры
def start_game():
    game_over = False
    # Запрос у пользователя на загрузку сохранения, при согласии выбирается файл загрузки и загружается игра.
    # При отказе создается новая игра.
    # Requests the user to download a save, if he agrees, the download file is selected and the game is loaded.
    # If the user refuses, a new game is created.
    load_game = input("Load game?")
    pathlist = Path(directory).glob('*.json')
    saves = {}
    loaded = False
    if load_game == "y":
        loaded = True
        iter_files = 1
        for path in pathlist:
            saves[iter_files] = path.name
            iter_files += 1
        print(saves)
        chose_save_file = int(input(f"Chose save file: {saves}"))
        file_name = saves[chose_save_file]
        with open(f"{Path(directory).joinpath(file_name)}", "r") as load_file:
            data = json.load(load_file)
            my_map, players = convert_json_to_class(data['my_map'], data['players'])

    else:
        my_map = create_map()
        players = create_plaeyrs()
    # Запуск раундов игры, поскольку в ТЗ ничего не говорилось об их количестве взял 10
    # Running rounds of the game, since the ToR did not say anything about their number took 10
    for round in range(1, 10):
        # В случае если все игроки умерли прерываем цикл и завершаем игру.
        # If all players are dead we interrupt the cycle and end the game.
        if game_over is True or check_all_players_die(players):
            print("GAME OVER")
            break
        else: print(f"ROUND {round}!!!")
        if check_all_players_power_off(players) is True:
            # При каждом новом раунде создаем блоки с огнем и передаем ход игрокам.
            # В условии ТЗ ничего не сказано про удаление огня из мест где небыл игрок, следовательно
            # количество огней будет увеличиваться пока не заполнит все доступные клетки.
            # Each new round, create blocks of fire and pass the turn to the players. The TK condition says nothing
            # about removing fire from places where no player has been, so the number of fires will increase until
            # it fills all available cells.
            create_flame_blocks(my_map, players)
        game_over, loaded = create_players_move(players, my_map, loaded)

# Создание новой карты игры.
# Creating a new map of the game.
def create_map():
    my_map = Map()
    my_map.generate()
    my_map.add_bloks()
    for block in my_map.blocks:
        if block.key_block is True:
            my_map.add_key(my_map.blocks[block.number])
        if block.hart_block is True:
            my_map.add_hart(my_map.blocks[block.number])
    return my_map

# Запрос о количестве игроков, присвоении им имен и создание оных.
# Requesting the number of players, naming them and creating them.
def create_plaeyrs():
    players = []
    try:
        num_players = int(input(f"Enter players number: \n"))
        logging.info(f"start game with {num_players} players")
        for i in range(0, num_players):
            name_player = input(f"Enter {i} player name: \n")
            player = Player(name=name_player, last_position=[])
            players.append(player)
            logging.info(f"start game with player: {player.name}")
        return players
    except Exception as e:
        logging.exception(e)
        return 0

# Создание блоков с огнем в начале каждого раунда. Также задается допустимые блоки для огня и запускается их отрисовка.
# Выбор блоков происходит произвольно. Если в блоке находится герой то происходит запуск отрисовки игрока в огне.
# Creating blocks with fire at the beginning of each round. It also sets the allowed blocks for fire and starts
# their rendering.
# The selection of blocks is arbitrary. If there is a hero in a block, the player is drawn in the fire.
def create_flame_blocks(my_map, players):
    flame_blocks = numpy.random.choice([1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 14], size=4, replace=False)
    logging.info("Created flame bloks: ")
    for i in flame_blocks:
        key_in_flame = False
        player_in_flame = False
        logging.info(f"{i}: {my_map.blocks[i].koord}")
        my_map.blocks[i].flame_block = True
        if my_map.blocks[i].key_block is True: key_in_flame = True
        for player in players:
            if player.position == i:
                player.life -= 1
                player_in_flame = True
                logging.info(f"player {player.name} in fire.\n life: {player.life}")
                if player.life == 0:
                    player.die = True
        flame_block = my_map.blocks[i]
        my_map.add_flame(flame_block, key_in_flame, player_in_flame)
    show_map(my_map, "")

# Создание ходов для игроков при каждом раунде обновляется power (действие) взял 5. В ТЗ вообще не понятно
# что такое действие и как оно должно быть реализовано, реализовал так.
# Пока у игрока есть power и жизни он может ходить.
# Creating moves for players at each round is updated power (action) took 5. In the ToR it is not clear at all
# what the action is and how it should be realized, I realized it this way.
# As long as the player has power and lives he can walk.
def create_players_move(players, my_map, loaded):
    for player in players:
        blocks = my_map.blocks
        my_map.add_player(blocks, blocks[0], player)
        my_map.add_bloks()
        show_map(my_map, "")
        if not loaded:
            player.power = Player.power_restart(player)
            my_map.add_player(blocks, blocks[player.position], player)
            my_map.add_bloks()
            show_map(my_map, "")
        while player.power > 0 and player.life > 0 and player.move_state is True and player.win is False:
            move(my_map, blocks, player, players)
        game_over = check_all_players_die(players)
        if player.win is True or game_over is True:
            game_over = True
            break
    if loaded: loaded = False
    return game_over, loaded

# Проверка на условия что все игроки использовали всю power, для завершения игры.
# Checking for conditions that all players have used all power, to complete the game.
def check_all_players_power_off(players):
    players_zero_power = 0
    for player in players:
        if player.power <= 0:
            players_zero_power += 1
    if players_zero_power == len(players):
        logging.info("ALL Player power off!!")
        return True
    return False

# Проверка на условия что все игроки умерли, для завершения игры.
# Check for the condition that all players are dead, to end the game.
def check_all_players_die(players):
    players_die = 0
    for player in players:
        if player.die is True:
            players_die += 1
    if players_die == len(players):
        logging.info("ALL DIE!!")
        return True
    return False

# Запуск отрисовки карты
# Start map drawing
def show_map(my_map, simbol):
    if (os.name == 'posix'):
        os.system('clear')
    # else screen will be cleared for windows
    else:
        os.system('cls')
    for row in my_map.my_map:
        print(simbol.join(row))

# Проверка позиций игроков, в случае если в одном блоке стоит более одного игрока.
# Check players' positions in case there is more than one player in one block.
def check_players_positions(players, player):
    for each_player in players:
        if player.position == each_player.position and player is not each_player:
            return each_player
    return False

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

# Прочие условия игры не связанные с перемещением.
# Other non-movement related game conditions.
def conditions(blocks, next_num_block, player, my_map, players):
    # Если не призовой блок, то перемещение к нему стоит 1 power
    # If not a prize block, moving to it costs 1 power
    if blocks[next_num_block].prize_block is False:
        player.power -= 1
    # Если блок сердца, то пополняет жизни
    # If a heart block, it replenishes lives
    if blocks[next_num_block].hart_block is True:
        player.life = 5
        logging.info(f"player {player.name} in on 'heart' block his life is {player.life}")
    # Если блок с огнем то отнимает жизнь и в случае если у игрока есть ключ, то выподает ключ в блок.
    # If the block with fire, it takes away life and if the player has a key, the key comes out in the block.
    if blocks[next_num_block].flame_block is True:
        player.life -= 1
        logging.info(f"player {player.name} in on 'flame' block, lose 1 life and have {player.life} life")
        blocks[next_num_block].flame_block = False
        if player.life == 0 and player.have_key is True:
            player.have_key = False
            player.die = True
            logging.info(f"player {player.name} has key, and key is dropped in block {player.position}")
            my_map.blocks[player.position].key_block = True
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.position])
            player.position = -1
        elif player.life == 0 and player.have_key is False:
            my_map.delete_player(blocks, blocks[player.position], player)
            player.die = True
            player.position = -1
    # Если вернулся к уже пройденым блокам, то гирой умирает от страха. Также если у героя был ключ то ключ
    # выпадет в блок
    # If you return to the already passed blocks, the gyro dies of fear. Also, if the hero had a key, the key
    # will fall into the block
    if player.position in player.last_position and blocks[player.last_position[-1]].prize_block is False:
        logging.info(f"PLAYER {player.name} scary and die.")
        player.move_state = False
        player.life = 0
        logging.info(f"player {player.name} life: {player.life}")
        player.die = True
        player.position = -1
        if player.have_key is True:
            player.have_key = False
            my_map.blocks[player.last_position[-1]].key_block = True
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.last_position[-1]])
        return player.move_state
    # Если игрок дошел до последнего блока с ключем то вигрышь и завершение игры. Иначе игрок погибает.
    # If the player reaches the last block with the key, the player wins and the game ends. Otherwise the player dies.
    if blocks[next_num_block].end_block is True and player.have_key is True:
        logging.info(f"PLAYER {player.name} WIN!")
        player.move_state = False
        player.win = True
        return player.move_state
    elif blocks[next_num_block].end_block is True and player.have_key is False:
        player.move_state = False
        player.life = 0
        player.die = True
        player.position = -1
        logging.info(f"PLAYER {player.name} KILL! \n player {player.name} life: {player.life}")
        my_map.delete_player(blocks, blocks[player.position], player)
        return player.move_state

# Конвертация данных в json для файла сохранения.
# Convert data to json for the save file.
def convert_data_to_json(my_map, players):
    new_bloks = []
    new_players = []
    for block in my_map.blocks:
        block = block.__dict__
        new_bloks.append(block)
    my_map.blocks = new_bloks
    for player in players:
        player = player.__dict__
        new_players.append(player)
    return my_map, new_players

# Конвертация json в классы используемые в игре, для корректной загрузки и работы игры.
# Conversion of json to classes used in the game, for correct loading and operation of the game.
def convert_json_to_class(my_map, players):
    new_blocks = []
    for block in my_map['blocks']:
        block = Block().convert_from_json(block)
        new_blocks.append(block)
    my_map = Map().convert_from_json(my_map)
    my_map.blocks = new_blocks
    new_players = []
    for player in players:
        player = Player().convert_from_json(player)
        new_players.append(player)
    return my_map, new_players