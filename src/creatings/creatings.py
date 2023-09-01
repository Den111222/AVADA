import logging
import numpy

from src.cheks.chek import check_all_players_die
from src.map import Map
from src.moves.moves import move, show_map
from src.player import Player


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