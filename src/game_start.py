import json
import logging
from pathlib import Path
import numpy as numpy
from src.map import Map, Block
from src.player import Player

# Поскольку в ТЗ было сказано выводить в консоль, то оставил эту строку, но это только мешает игре.
# logging.basicConfig(level=logging.INFO, filemode="w",
#                     format="%(asctime)s %(levelname)s %(message)s")

# Сделал сохранение логов в файл, для более удобного их анализа.
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# Это оставил как подсказку, для себя.
# logging.debug("A DEBUG Message")
# logging.info("An INFO")
# logging.warning("A WARNING")
# logging.error("An ERROR")
# logging.critical("A message of CRITICAL severity")

# Как переменную задал путь сохранения файлов сохранений игры.
directory = 'src/saves'

# Старт игры
def start_game():
    game_over = False
    # Запрос у пользователя на загрузку сохранения, при согласии выбирается файл загрузки и загружается игра.
    # При отказе создается новая игра.
    load_game = input("Load game?")
    pathlist = Path(directory).glob('*.json')
    saves = {}
    if load_game == "y":
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
    for round in range(1, 10):
        # В случае если все игроки умерли прерываем цикл и завершаем игру.
        if game_over is True or check_all_players_die(players):
            print("GAME OVER")
            break
        else: print(f"ROUND {round}!!!")
        # При каждом новом раунде создаем блоки с огнем и передаем ход игрокам.
        # В условии ТЗ ничего не сказано про удаление огня из мест где небыл игрок, следовательно
        # количество огней будет увеличиваться пока не заполнит все доступные клетки.
        create_flame_blocks(my_map, players)
        game_over = create_players_move(players, my_map)

# Создание новой карты игры.
def create_map():
    my_map = Map()
    my_map.generate()
    my_map.add_bloks()
    my_map.add_key(my_map.blocks[4])
    my_map.add_hart(my_map.blocks[10])
    my_map.add_hart(my_map.blocks[12])
    return my_map

# Запрос о количестве игроков, присвоении им имен и создание оных.
def create_plaeyrs():
    players = []
    try:
        num_players = int(input(f"Enter players number: \n"))
        logging.info(f"start game with {num_players} players")
        for i in range(0, num_players):
            player = Player()
            player.name = input(f"Enter {i} player name: \n")
            players.append(player)
            logging.info(f"start game with player: {player.name}")
        return players
    except Exception as e:
        logging.exception(e)
        return 0

# Создание блоков с огнем в начале каждого раунда. Также задается допустимые блоки для огня и запускается их отрисовка.
# Выбор блоков происходит произвольно. Если в блоке находится герой то происходит запуск отрисовки игрока в огне.
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

# Проверка на условия что все игроки умерли, для завершения игры.
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
def show_map(my_map, simbol):
    for row in my_map.my_map:
        print(simbol.join(row))

# Проверка позиций игроков, в случае если в одном блоке стоит более одного игрока.
def check_players_positions(players, player):
    for each_player in players:
        if player.position == each_player.position and player is not each_player:
            return each_player
    return False

# Реализация ходов в игре игроками
def move(my_map, blocks, player, players):
    directions = ["w", "a", "s", "d", "e", "f", "S", "q"]
    direction = input("нажмите w,a,s,d для движения, e - поднятия ключа, f - атаки, S - сохранить игру"
                      "q - если надумаете выйти: \n")
    # при выборе "е" происходит подьем ключа в блоке если он там есть, при этом power у игрока отнимается
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
    elif direction == "e" and blocks[player.position].key_block is False:
        logging.info(f"player {player.name} chose 'e' \n"
                     f"No Key here")
    # Запуск сохранения игры в файл json. При этом есть возможность задать имя файла сохронения игры.
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
    # Проверка на валидность хода игрока. А также запуск соответствующих отрисовок при перемещении игрока по блокам.
    elif direction in blocks[player.position].valid_move:
        logging.info(f"player {player.name} chose {direction} \n")
        # Если игрок покинул клетку и не взял ключ
        if blocks[player.position].key_block is True:
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_key(my_map.blocks[player.position])
        # Если игрок встал блок с сердцем
        elif blocks[player.position].hart_block is True:
            my_map.delete_player(blocks, blocks[player.position], player)
            my_map.add_hart(my_map.blocks[player.position])
        # Если игрок покинул клетку и в клетки остался другой игрок.
        else:
            block_have_player = check_players_positions(players, player)
            if block_have_player is not False:
                my_map.add_player(blocks, blocks[block_have_player.position], block_have_player)
            else: my_map.delete_player(blocks, blocks[player.position], player)
        # Добавление последних позиций игрока, чтобы не смог сбежать.
        player.last_position.append(player.position)
        next_num_block = blocks[player.position].valid_move[direction]
        # Реализация возможности атаки других игроков.
        for each_player in players:
            if next_num_block == each_player.position:
                chose = input(f"You wont to kill? {each_player.name}, if yes print 'y' else print 'n'")
                if chose == "y":
                    each_player.life -= 1
                    logging.info(f"player {player.name} chose 'y' to attack player {each_player.name}\n" 
                                 f"player {each_player.name} wos bin attack by player {player.name}\n"
                                 f"player {each_player.name} life: {each_player.life}")
                    if each_player.life == 0:
                        logging.info(f"player {each_player.name} wos bin kill by player {player.name}")
                        each_player.move_state = False
                        each_player.die = True
                        each_player.position = -1
                    player.power -= 2
                elif chose == "n":
                    player.power -= 3
        player.position = next_num_block
        # Запуск прочих условий, не связанных с перемещением.
        conditions(blocks, next_num_block, player, my_map, players)
        my_map.add_player(blocks, blocks[next_num_block], player)
        my_map.add_bloks()
        show_map(my_map, "")
    # Если герой бьется о стену теряет 1 жизнь.
    elif direction in directions and player.life > 0:
        logging.info(f"player {player.name} chose {direction}"
                     f"it is wrong direction and loose 1 life")
        player.life -= 1
    # Должен быть выход, но в ТЗ об этом ничего не говориться.
    elif direction == "q":
        print("В ТЗ не предусмотрен выход из игры, вот такая лажа!")
    # Если нажал что-то совсем не то, при выборе хода
    elif direction not in directions:
        logging.info(f"wrong chose, input {directions}")
    # Все остальные случаи хода, хотя их быть не должно)))
    else:
        logging.info(f"die")
        player.die = True

# Прочие условия игры не связанные с перемещением.
def conditions(blocks, next_num_block, player, my_map, players):
    # Если не призовой блок, то перемещение к нему стоит 1 power
    if blocks[next_num_block].prize_block is False:
        player.power -= 1
    # Если блок сердца, то пополняет жизни
    if blocks[next_num_block].hart_block is True:
        player.life = 5
        logging.info(f"player {player.name} in on 'heart' block his life is {player.life}")
    # Если блок с огнем то отнимает жизнь и в случае если у игрока есть ключ, то выподает ключ в блок.
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
    # выподет в блок
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

# Конвертация json в классы ипользуемые в игре, для корректной загрузки и работы игры.
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