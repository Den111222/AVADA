import json
import logging
from pathlib import Path
from src.cheks.chek import check_all_players_die, check_all_players_power_off
from src.convertation.convertation import convert_json_to_class
from src.creatings.creatings import create_players_move, create_flame_blocks, create_map, create_plaeyrs


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