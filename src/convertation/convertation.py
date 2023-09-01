from src.map import Block, Map
from src.player import Player


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